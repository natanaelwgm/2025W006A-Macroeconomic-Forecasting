"""
MIDAS (Mixed Data Sampling) model implementation for v2.

MIDAS models handle mixed-frequency data by using polynomial distributed lags
to map high-frequency variables to low-frequency targets.
"""

import numpy as np
from typing import Dict, List
from sklearn.linear_model import LinearRegression
from ..core.base import BaseModel, ModelSpec


class MIDASModel(BaseModel):
    """
    MIDAS model with polynomial distributed lags.
    
    Parameters:
    - lag_max: Maximum lag for high-frequency variables
    - polynomial_order: Order of polynomial for distributed lags (default: 2)
    """
    
    NAME = "MIDAS"
    SPEC = ModelSpec({
        "frequency": "any",
        "input": {
            "target": {"lags": [1]},  # Basic AR term
            "exog": {"__all__": {"lags": [0, 1, 2, 3, 6, 12]}}  # High-frequency exog
        },
        "strategies": ["frozen"],
        "supports_horizons": "any"
    })
    
    def __init__(self, lag_max: int = 12, polynomial_order: int = 2):
        self.lag_max = lag_max
        self.polynomial_order = polynomial_order
        self.model = None
        self.fitted = False
        
    def _create_midas_features(self, X: List[List[float]]) -> np.ndarray:
        """Create MIDAS features using polynomial distributed lags."""
        X_array = np.array(X)
        n_samples, n_features = X_array.shape
        
        # Create polynomial weights for distributed lags
        lag_weights = np.zeros((self.lag_max, self.polynomial_order + 1))
        for lag in range(self.lag_max):
            for poly_order in range(self.polynomial_order + 1):
                lag_weights[lag, poly_order] = lag ** poly_order
        
        # Apply MIDAS transformation
        midas_features = []
        for i in range(n_samples):
            sample_features = []
            
            # For each feature, create MIDAS aggregated values
            for feat_idx in range(n_features):
                # Get recent values for this feature (up to lag_max)
                start_idx = max(0, i - self.lag_max + 1)
                recent_values = X_array[start_idx:i+1, feat_idx]
                
                # Pad with zeros if not enough history
                if len(recent_values) < self.lag_max:
                    padded_values = np.zeros(self.lag_max)
                    padded_values[-len(recent_values):] = recent_values
                    recent_values = padded_values
                
                # Apply polynomial distributed lag weights
                midas_value = np.sum(recent_values * lag_weights[:, 0])  # Linear term
                sample_features.append(midas_value)
            
            midas_features.append(sample_features)
        
        return np.array(midas_features)
    
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        """Fit MIDAS model to the data."""
        # Create MIDAS features
        X_midas = self._create_midas_features(X)
        
        # Fit linear model
        self.model = LinearRegression()
        self.model.fit(X_midas, y)
        
        self.fitted = True
        
    def predict_row(self, x_row: List[float]) -> float:
        """Predict next value using MIDAS model."""
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction.")
        
        # Create MIDAS features for single row
        X_midas = self._create_midas_features([x_row])
        
        prediction = self.model.predict(X_midas)[0]
        return float(prediction)
    
    def get_params(self) -> Dict:
        """Get model parameters."""
        return {
            "lag_max": self.lag_max,
            "polynomial_order": self.polynomial_order,
            "fitted": self.fitted
        }
    
    def set_params(self, params: Dict) -> None:
        """Set model parameters."""
        self.lag_max = params.get("lag_max", 12)
        self.polynomial_order = params.get("polynomial_order", 2)
        self.fitted = params.get("fitted", False)


def create(params: Dict) -> MIDASModel:
    """Create MIDAS model instance."""
    return MIDASModel(
        lag_max=params.get("lag_max", 12),
        polynomial_order=params.get("polynomial_order", 2)
    )
