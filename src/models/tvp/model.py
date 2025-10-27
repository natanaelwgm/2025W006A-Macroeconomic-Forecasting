"""
TVP (Time-Varying Parameter) model implementation for v2.

TVP models allow regression coefficients to evolve over time using
a state space framework with Kalman filtering.
"""

import numpy as np
from typing import Dict, List
from sklearn.linear_model import LinearRegression
from ..core.base import BaseModel, ModelSpec


class TVPModel(BaseModel):
    """
    Time-Varying Parameter model using simplified Kalman filter.
    
    Parameters:
    - state_variance: Variance of state transition (controls parameter evolution)
    - observation_variance: Variance of observation noise
    """
    
    NAME = "TVP"
    SPEC = ModelSpec({
        "frequency": "any",
        "input": {
            "target": {"lags": [1, 3, 6]},
            "exog": {"__all__": {"lags": [0, 1, 3]}}
        },
        "strategies": ["frozen"],
        "supports_horizons": "any"
    })
    
    def __init__(self, state_variance: float = 0.01, observation_variance: float = 1.0):
        self.state_variance = state_variance
        self.observation_variance = observation_variance
        self.state_mean = None
        self.state_cov = None
        self.fitted = False
        
    def _kalman_update(self, y: float, X: np.ndarray, 
                       state_mean: np.ndarray, state_cov: np.ndarray) -> tuple:
        """Perform Kalman filter update step."""
        # Prediction step
        pred_mean = state_mean
        pred_cov = state_cov + self.state_variance * np.eye(len(state_mean))
        
        # Update step
        innovation = y - np.dot(X, pred_mean)
        innovation_var = np.dot(X, np.dot(pred_cov, X.T)) + self.observation_variance
        
        if innovation_var <= 0:
            innovation_var = 1e-6  # Avoid division by zero
        
        kalman_gain = np.dot(pred_cov, X.T) / innovation_var
        
        updated_mean = pred_mean + kalman_gain * innovation
        updated_cov = pred_cov - np.outer(kalman_gain, np.dot(X, pred_cov))
        
        return updated_mean, updated_cov
    
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        """Fit TVP model using Kalman filter."""
        X_array = np.array(X)
        y_array = np.array(y)
        
        n_features = X_array.shape[1]
        
        # Initialize state
        self.state_mean = np.zeros(n_features)
        self.state_cov = np.eye(n_features) * 10.0  # Large initial uncertainty
        
        # Run Kalman filter through all observations
        for i in range(len(y_array)):
            X_row = X_array[i]
            y_obs = y_array[i]
            
            self.state_mean, self.state_cov = self._kalman_update(
                y_obs, X_row, self.state_mean, self.state_cov
            )
        
        self.fitted = True
        
    def predict_row(self, x_row: List[float]) -> float:
        """Predict next value using TVP model."""
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction.")
        
        X_row = np.array(x_row)
        
        # Prediction using current state estimate
        prediction = np.dot(X_row, self.state_mean)
        
        return float(prediction)
    
    def get_params(self) -> Dict:
        """Get model parameters."""
        return {
            "state_variance": self.state_variance,
            "observation_variance": self.observation_variance,
            "fitted": self.fitted
        }
    
    def set_params(self, params: Dict) -> None:
        """Set model parameters."""
        self.state_variance = params.get("state_variance", 0.01)
        self.observation_variance = params.get("observation_variance", 1.0)
        self.fitted = params.get("fitted", False)


def create(params: Dict) -> TVPModel:
    """Create TVP model instance."""
    return TVPModel(
        state_variance=params.get("state_variance", 0.01),
        observation_variance=params.get("observation_variance", 1.0)
    )
