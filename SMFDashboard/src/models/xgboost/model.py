from __future__ import annotations

from typing import Dict, List, Optional
import math
import random

from core.base import BaseModel

NAME = "XGBoost"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [1, 3, 6]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "n_estimators": {"type": "int", "default": 100, "min": 10},
        "max_depth": {"type": "int", "default": 6, "min": 1},
        "learning_rate": {"type": "float", "default": 0.3, "min": 0.01},
        "subsample": {"type": "float", "default": 1.0, "min": 0.1, "max": 1.0},
        "colsample_bytree": {"type": "float", "default": 1.0, "min": 0.1, "max": 1.0},
        "reg_alpha": {"type": "float", "default": 0.0, "min": 0.0},
        "reg_lambda": {"type": "float", "default": 1.0, "min": 0.0},
        "random_state": {"type": "int", "default": 42},
    },
}

class _XGBoostTree:
    """Single tree in XGBoost ensemble with regularization"""
    def __init__(self, max_depth: int = 6, reg_alpha: float = 0.0, reg_lambda: float = 1.0):
        self.max_depth = max_depth
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.feature: Optional[int] = None
        self.threshold: Optional[float] = None
        self.left: Optional['_XGBoostTree'] = None
        self.right: Optional['_XGBoostTree'] = None
        self.value: float = 0.0
        self.depth: int = 0

    def fit(self, X: List[List[float]], gradients: List[float], hessians: List[float], 
            depth: int = 0, indices: Optional[List[int]] = None) -> None:
        """Fit tree using gradients and hessians (Newton's method)"""
        if indices is None:
            indices = list(range(len(X)))
        
        self.depth = depth
        
        if not indices or depth >= self.max_depth:
            # Leaf node - calculate optimal value with regularization
            G = sum(gradients[i] for i in indices)  # Sum of gradients
            H = sum(hessians[i] for i in indices)   # Sum of hessians
            self.value = -G / (H + self.reg_lambda) if H + self.reg_lambda > 0 else 0.0
            return
        
        best_gain = -float('inf')
        best_feature = None
        best_threshold = None
        best_left_indices = []
        best_right_indices = []
        
        n_features = len(X[0]) if X and X[0] else 0
        
        # Try each feature
        for feature_idx in range(n_features):
            # Get unique values for this feature
            values = sorted(set(X[i][feature_idx] for i in indices))
            
            # Try splits between consecutive values
            for i in range(len(values) - 1):
                threshold = (values[i] + values[i + 1]) / 2
                
                left_indices = [idx for idx in indices if X[idx][feature_idx] <= threshold]
                right_indices = [idx for idx in indices if X[idx][feature_idx] > threshold]
                
                if not left_indices or not right_indices:
                    continue
                
                # Calculate gain using XGBoost formula
                gain = self._calculate_gain(gradients, hessians, indices, left_indices, right_indices)
                
                if gain > best_gain:
                    best_gain = gain
                    best_feature = feature_idx
                    best_threshold = threshold
                    best_left_indices = left_indices
                    best_right_indices = right_indices
        
        # If no good split found, make leaf
        if best_feature is None or best_gain <= 0:
            G = sum(gradients[i] for i in indices)
            H = sum(hessians[i] for i in indices)
            self.value = -G / (H + self.reg_lambda) if H + self.reg_lambda > 0 else 0.0
            return
        
        # Create split
        self.feature = best_feature
        self.threshold = best_threshold
        
        self.left = _XGBoostTree(self.max_depth, self.reg_alpha, self.reg_lambda)
        self.right = _XGBoostTree(self.max_depth, self.reg_alpha, self.reg_lambda)
        
        self.left.fit(X, gradients, hessians, depth + 1, best_left_indices)
        self.right.fit(X, gradients, hessians, depth + 1, best_right_indices)
    
    def _calculate_gain(self, gradients: List[float], hessians: List[float], 
                       parent_indices: List[int], left_indices: List[int], 
                       right_indices: List[int]) -> float:
        """Calculate XGBoost gain formula"""
        def score(indices):
            G = sum(gradients[i] for i in indices)
            H = sum(hessians[i] for i in indices)
            return (G * G) / (H + self.reg_lambda) if H + self.reg_lambda > 0 else 0.0
        
        parent_score = score(parent_indices)
        left_score = score(left_indices)
        right_score = score(right_indices)
        
        gain = 0.5 * (left_score + right_score - parent_score) - self.reg_alpha
        return gain
    
    def predict(self, x_row: List[float]) -> float:
        if self.feature is None:  # Leaf node
            return self.value
        
        if x_row[self.feature] <= self.threshold:
            return self.left.predict(x_row) if self.left else 0.0
        else:
            return self.right.predict(x_row) if self.right else 0.0

class _XGBoost(BaseModel):
    """XGBoost implementation with gradient boosting and regularization"""
    
    def __init__(self, n_estimators: int = 100, max_depth: int = 6, learning_rate: float = 0.3,
                 subsample: float = 1.0, colsample_bytree: float = 1.0, 
                 reg_alpha: float = 0.0, reg_lambda: float = 1.0, random_state: int = 42):
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.subsample = subsample
        self.colsample_bytree = colsample_bytree
        self.reg_alpha = reg_alpha
        self.reg_lambda = reg_lambda
        self.random_state = random_state
        
        self.trees: List[_XGBoostTree] = []
        self.base_score: float = 0.0
        
        # Set random seed
        random.seed(random_state)
    
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            return
        
        n = len(X)
        self.base_score = sum(y) / n  # Initial prediction
        
        # Initialize predictions with base score
        predictions = [self.base_score] * n
        
        self.trees = []
        
        for round_num in range(self.n_estimators):
            # Calculate gradients and hessians (for squared loss)
            gradients = [2 * (predictions[i] - y[i]) for i in range(n)]
            hessians = [2.0] * n  # Constant for squared loss
            
            # Subsample data
            if self.subsample < 1.0:
                sample_size = int(n * self.subsample)
                sample_indices = random.sample(range(n), sample_size)
                X_sample = [X[i] for i in sample_indices]
                grad_sample = [gradients[i] for i in sample_indices]
                hess_sample = [hessians[i] for i in sample_indices]
            else:
                X_sample = X
                grad_sample = gradients
                hess_sample = hessians
            
            # Feature subsampling
            n_features = len(X[0]) if X and X[0] else 0
            if self.colsample_bytree < 1.0:
                n_features_sample = max(1, int(n_features * self.colsample_bytree))
                feature_indices = random.sample(range(n_features), n_features_sample)
                X_sample = [[row[i] for i in feature_indices] for row in X_sample]
            
            # Fit tree
            tree = _XGBoostTree(self.max_depth, self.reg_alpha, self.reg_lambda)
            tree.fit(X_sample, grad_sample, hess_sample)
            self.trees.append(tree)
            
            # Update predictions
            for i in range(n):
                if self.colsample_bytree < 1.0:
                    x_sample = [X[i][j] for j in feature_indices]
                else:
                    x_sample = X[i]
                
                tree_pred = tree.predict(x_sample)
                predictions[i] += self.learning_rate * tree_pred
    
    def predict_row(self, x_row: List[float]) -> float:
        prediction = self.base_score
        
        for tree in self.trees:
            tree_pred = tree.predict(x_row)
            prediction += self.learning_rate * tree_pred
        
        return prediction
    
    def get_params(self) -> Dict:
        return {
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "learning_rate": self.learning_rate,
            "base_score": self.base_score,
        }
    
    def set_params(self, params: Dict) -> None:
        self.n_estimators = params.get("n_estimators", self.n_estimators)
        self.max_depth = params.get("max_depth", self.max_depth)
        self.learning_rate = params.get("learning_rate", self.learning_rate)
        self.base_score = params.get("base_score", self.base_score)

def create(params: Dict) -> BaseModel:
    return _XGBoost(**params)
