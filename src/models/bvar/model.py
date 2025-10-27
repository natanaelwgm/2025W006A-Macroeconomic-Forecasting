from __future__ import annotations

from typing import Dict, List
import math
import random

from core.base import BaseModel

NAME = "BVAR"

SPEC = {
    "frequency": "any", 
    "input": {"target": {"lags": [1, 2, 3, 6]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "lags": {"type": "int", "default": 4, "min": 1},
        "prior_strength": {"type": "float", "default": 0.2, "min": 0.01},
        "decay": {"type": "float", "default": 1.0, "min": 0.1},
        "cross_variable_weight": {"type": "float", "default": 0.5, "min": 0.0},
    },
}

class _BVAR(BaseModel):
    """Bayesian Vector Autoregression with Minnesota prior"""
    
    def __init__(self, lags: int = 4, prior_strength: float = 0.2, 
                 decay: float = 1.0, cross_variable_weight: float = 0.5):
        self.lags = lags
        self.prior_strength = prior_strength
        self.decay = decay
        self.cross_variable_weight = cross_variable_weight
        
        self.coef: List[float] = []
        self.intercept: float = 0.0
        self.var_means: List[float] = []
        self.var_stds: List[float] = []
    
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            return
        
        n = len(X)
        p = len(X[0]) if X[0] else 0
        
        if n < self.lags + 1 or p == 0:
            self.coef = [0.0] * p
            self.intercept = sum(y) / len(y) if y else 0.0
            return
        
        # Calculate sample statistics for prior
        mean_y = sum(y) / n
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / max(1, n-1))
        self.var_stds = [max(std_y, 0.01)]  # Avoid division by zero
        
        # Set up Minnesota prior
        # Prior mean: AR(1) coefficient = 0.9, others = 0
        prior_mean = [0.0] * (p + 1)  # +1 for intercept
        prior_precision = [0.0] * (p + 1)
        
        # Intercept gets weak prior
        prior_precision[0] = 0.001
        
        # Features get Minnesota prior
        for i in range(p):
            if i == 0:  # First lag gets higher prior mean
                prior_mean[i + 1] = 0.9
                prior_precision[i + 1] = self.prior_strength
            else:
                # Other lags get shrinkage
                lag_num = (i // (p // max(1, self.lags))) + 1  # Approximate lag number
                prior_precision[i + 1] = self.prior_strength / (lag_num ** self.decay)
        
        # Bayesian linear regression
        self._bayesian_regression(X, y, prior_mean, prior_precision)
    
    def _bayesian_regression(self, X: List[List[float]], y: List[float], 
                           prior_mean: List[float], prior_precision: List[float]) -> None:
        """Bayesian linear regression with normal prior"""
        n = len(X)
        p = len(X[0]) if X else 0
        
        if n == 0 or p == 0:
            self.coef = []
            self.intercept = 0.0
            return
        
        # Build design matrix with intercept
        X_design = [[1.0] + X[i] for i in range(n)]
        k = p + 1  # Number of parameters (including intercept)
        
        # Prior precision matrix (diagonal)
        prior_prec_matrix = [[0.0] * k for _ in range(k)]
        for i in range(k):
            prior_prec_matrix[i][i] = prior_precision[i] if i < len(prior_precision) else 0.001
        
        # Likelihood precision: X^T X
        XTX = [[0.0] * k for _ in range(k)]
        for i in range(n):
            for a in range(k):
                for b in range(k):
                    XTX[a][b] += X_design[i][a] * X_design[i][b]
        
        # Posterior precision: prior_prec + X^T X
        post_prec = [[prior_prec_matrix[i][j] + XTX[i][j] for j in range(k)] for i in range(k)]
        
        # X^T y
        XTy = [sum(X_design[i][j] * y[i] for i in range(n)) for j in range(k)]
        
        # Prior precision * prior mean
        prior_term = [sum(prior_prec_matrix[i][j] * prior_mean[j] for j in range(k)) for i in range(k)]
        
        # Posterior mean vector: inv(post_prec) * (prior_term + X^T y)
        rhs = [prior_term[i] + XTy[i] for i in range(k)]
        
        # Solve linear system
        try:
            solution = self._solve_linear_system(post_prec, rhs)
            self.intercept = solution[0]
            self.coef = solution[1:]
        except:
            # Fallback to prior mean
            self.intercept = prior_mean[0] if prior_mean else 0.0
            self.coef = prior_mean[1:] if len(prior_mean) > 1 else [0.0] * p
    
    def _solve_linear_system(self, A: List[List[float]], b: List[float]) -> List[float]:
        """Simple Gaussian elimination solver"""
        n = len(A)
        if n == 0:
            return []
        
        # Create augmented matrix
        aug = [A[i][:] + [b[i]] for i in range(n)]
        
        # Forward elimination with partial pivoting
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(aug[k][i]) > abs(aug[max_row][i]):
                    max_row = k
            
            # Swap rows
            aug[i], aug[max_row] = aug[max_row], aug[i]
            
            # Check for near-zero pivot
            if abs(aug[i][i]) < 1e-10:
                continue
            
            # Make diagonal 1
            for k in range(i + 1, n + 1):
                aug[i][k] /= aug[i][i]
            
            # Eliminate column
            for k in range(i + 1, n):
                factor = aug[k][i]
                for j in range(i, n + 1):
                    aug[k][j] -= factor * aug[i][j]
        
        # Back substitution
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            x[i] = aug[i][n]
            for j in range(i + 1, n):
                x[i] -= aug[i][j] * x[j]
        
        return x
    
    def predict_row(self, x_row: List[float]) -> float:
        if not self.coef:
            return self.intercept
        
        result = self.intercept
        for i, coef in enumerate(self.coef):
            if i < len(x_row):
                result += coef * x_row[i]
        
        return result
    
    def get_params(self) -> Dict:
        return {
            "coef": self.coef[:],
            "intercept": self.intercept,
            "lags": self.lags,
            "prior_strength": self.prior_strength,
        }
    
    def set_params(self, params: Dict) -> None:
        self.coef = params.get("coef", [])
        self.intercept = params.get("intercept", 0.0)
        self.lags = params.get("lags", self.lags)
        self.prior_strength = params.get("prior_strength", self.prior_strength)

def create(params: Dict) -> BaseModel:
    return _BVAR(**params)
