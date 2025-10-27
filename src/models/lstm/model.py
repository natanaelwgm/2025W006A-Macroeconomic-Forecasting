from __future__ import annotations

from typing import Dict, List
import math
import random

from core.base import BaseModel

NAME = "LSTM"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [1, 2, 3, 6, 12]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "hidden_size": {"type": "int", "default": 32, "min": 8},
        "sequence_length": {"type": "int", "default": 12, "min": 3},
        "learning_rate": {"type": "float", "default": 0.01, "min": 0.001},
        "epochs": {"type": "int", "default": 50, "min": 10},
        "dropout": {"type": "float", "default": 0.1, "min": 0.0, "max": 0.5},
    },
}

class _SimpleLSTM(BaseModel):
    """Simplified LSTM implementation for time series forecasting"""
    
    def __init__(self, hidden_size: int = 32, sequence_length: int = 12, 
                 learning_rate: float = 0.01, epochs: int = 50, dropout: float = 0.1):
        self.hidden_size = hidden_size
        self.sequence_length = sequence_length
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.dropout = dropout
        
        # Simple recurrent weights (simplified LSTM)
        self.Wh = []  # Hidden to hidden weights
        self.Wx = []  # Input to hidden weights
        self.Wo = []  # Hidden to output weights
        self.bh = []  # Hidden bias
        self.bo = 0.0  # Output bias
        
        # Data normalization
        self.mean_x: float = 0.0
        self.std_x: float = 1.0
        self.mean_y: float = 0.0
        self.std_y: float = 1.0
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self) -> None:
        """Initialize weights with small random values"""
        # Xavier initialization
        scale = math.sqrt(2.0 / (self.hidden_size + 1))
        
        # Hidden to hidden weights (simplified - just one matrix)
        self.Wh = [[random.gauss(0, scale) for _ in range(self.hidden_size)] 
                   for _ in range(self.hidden_size)]
        
        # Input to hidden weights (assuming single input feature for simplicity)
        self.Wx = [random.gauss(0, scale) for _ in range(self.hidden_size)]
        
        # Hidden to output weights
        self.Wo = [random.gauss(0, scale) for _ in range(self.hidden_size)]
        
        # Biases
        self.bh = [0.0] * self.hidden_size
        self.bo = 0.0
    
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            return
        
        n = len(X)
        if n < self.sequence_length:
            # Fallback to simple linear model
            self._simple_fit(X, y)
            return
        
        # Normalize data
        all_x = [val for row in X for val in row]
        self.mean_x = sum(all_x) / len(all_x) if all_x else 0.0
        self.std_x = math.sqrt(sum((x - self.mean_x) ** 2 for x in all_x) / len(all_x)) if all_x else 1.0
        self.std_x = max(self.std_x, 1e-8)
        
        self.mean_y = sum(y) / n
        self.std_y = math.sqrt(sum((yi - self.mean_y) ** 2 for yi in y) / n)
        self.std_y = max(self.std_y, 1e-8)
        
        # Normalize inputs
        X_norm = [[(val - self.mean_x) / self.std_x for val in row] for row in X]
        y_norm = [(yi - self.mean_y) / self.std_y for yi in y]
        
        # Simple training loop
        for epoch in range(min(self.epochs, 30)):  # Limit for performance
            total_loss = 0.0
            
            for i in range(len(X_norm)):
                # Forward pass (simplified)
                prediction = self._forward(X_norm[i])
                
                # Loss
                error = prediction - y_norm[i]
                total_loss += error ** 2
                
                # Simple gradient update (very basic)
                lr = self.learning_rate * (0.95 ** epoch)  # Decay learning rate
                
                # Update output weights (simplified backprop)
                for j in range(len(self.Wo)):
                    self.Wo[j] -= lr * error * 0.1  # Simplified gradient
                
                self.bo -= lr * error * 0.1
            
            # Early stopping if loss is very small
            if total_loss / len(X_norm) < 1e-6:
                break
    
    def _simple_fit(self, X: List[List[float]], y: List[float]) -> None:
        """Fallback to simple linear model for small datasets"""
        if not X or not y:
            return
        
        n = len(X)
        p = len(X[0]) if X[0] else 0
        
        self.mean_y = sum(y) / n
        
        if p == 0:
            return
        
        # Simple linear regression on first feature
        x_vals = [row[0] for row in X]
        mean_x = sum(x_vals) / n
        
        num = sum((x_vals[i] - mean_x) * (y[i] - self.mean_y) for i in range(n))
        den = sum((x_vals[i] - mean_x) ** 2 for i in range(n))
        
        if den > 0:
            slope = num / den
            self.Wo = [slope] + [0.0] * (self.hidden_size - 1)
            self.bo = self.mean_y - slope * mean_x
        else:
            self.Wo = [0.0] * self.hidden_size
            self.bo = self.mean_y
    
    def _forward(self, x_row: List[float]) -> float:
        """Simplified forward pass"""
        if not x_row or not self.Wo:
            return 0.0
        
        # Simplified recurrent computation
        hidden = [0.0] * self.hidden_size
        
        # Process sequence (use all input features as sequence)
        for t, x_val in enumerate(x_row[:self.sequence_length]):
            # Update hidden state (simplified LSTM cell)
            new_hidden = []
            for i in range(self.hidden_size):
                # Simplified: h_t = tanh(Wx * x_t + Wh * h_{t-1} + b)
                h_val = self.Wx[i] * x_val + self.bh[i]
                for j in range(self.hidden_size):
                    h_val += self.Wh[i][j] * hidden[j]
                
                new_hidden.append(math.tanh(h_val))
            
            hidden = new_hidden
        
        # Output layer
        output = self.bo
        for i in range(len(self.Wo)):
            if i < len(hidden):
                output += self.Wo[i] * hidden[i]
        
        return output
    
    def predict_row(self, x_row: List[float]) -> float:
        if not x_row:
            return self.mean_y
        
        # Normalize input
        x_norm = [(val - self.mean_x) / self.std_x for val in x_row]
        
        # Forward pass
        pred_norm = self._forward(x_norm)
        
        # Denormalize output
        return pred_norm * self.std_y + self.mean_y
    
    def get_params(self) -> Dict:
        return {
            "Wo": self.Wo[:],
            "bo": self.bo,
            "mean_x": self.mean_x,
            "std_x": self.std_x,
            "mean_y": self.mean_y,
            "std_y": self.std_y,
            "hidden_size": self.hidden_size,
        }
    
    def set_params(self, params: Dict) -> None:
        self.Wo = params.get("Wo", [])
        self.bo = params.get("bo", 0.0)
        self.mean_x = params.get("mean_x", 0.0)
        self.std_x = params.get("std_x", 1.0)
        self.mean_y = params.get("mean_y", 0.0)
        self.std_y = params.get("std_y", 1.0)
        self.hidden_size = params.get("hidden_size", self.hidden_size)

def create(params: Dict) -> BaseModel:
    return _SimpleLSTM(**params)
