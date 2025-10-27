"""
ARIMA(p,d,q) model implementation for v2.

Currently implements ARIMA(p,d,0) - AR terms with differencing.
MA terms (q>0) will be added in future iterations.
"""

import numpy as np
from typing import Dict, List, Optional
from sklearn.linear_model import LinearRegression
from ..core.base import BaseModel, ModelSpec


class ARIMAModel(BaseModel):
    """
    ARIMA(p,d,q) model with differencing support.
    
    Parameters:
    - p: AR order (number of autoregressive terms)
    - d: Differencing order (number of times to difference)
    - q: MA order (currently must be 0, MA terms not yet implemented)
    """
    
    NAME = "ARIMA"
    SPEC = ModelSpec({
        "frequency": "any",
        "input": {
            "target": {"lags": []},  # ARIMA uses its own lag structure
            "exog": {}  # No exogenous variables for baseline ARIMA
        },
        "strategies": ["frozen"],
        "supports_horizons": "any"
    })
    
    def __init__(self, p: int = 1, d: int = 0, q: int = 0):
        if q != 0:
            raise ValueError("MA terms (q>0) not yet implemented. Use q=0.")
        if p < 0 or d < 0:
            raise ValueError("p and d must be non-negative.")
            
        self.p = p
        self.d = d
        self.q = q
        self.ar_model = None
        self.diff_history = []  # Store differenced series for undifferencing
        self.original_mean = None
        self.fitted = False
        
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        """Fit ARIMA model to the data."""
        y_array = np.array(y)
        
        # Store original mean for undifferencing
        self.original_mean = np.mean(y_array)
        
        # Apply differencing d times
        diff_series = y_array.copy()
        self.diff_history = []
        
        for i in range(self.d):
            diff_series = np.diff(diff_series)
            self.diff_history.append(diff_series.copy())
        
        # Create AR features
        if len(diff_series) <= self.p:
            raise ValueError(f"Not enough data for AR({self.p}). Need at least {self.p + 1} observations.")
        
        # Create lagged features for AR(p)
        X_ar = []
        y_ar = []
        
        for i in range(self.p, len(diff_series)):
            # Features: p lagged values
            x_row = diff_series[i-self.p:i].tolist()
            X_ar.append(x_row)
            y_ar.append(diff_series[i])
        
        # Fit AR model using linear regression
        self.ar_model = LinearRegression()
        self.ar_model.fit(X_ar, y_ar)
        
        self.fitted = True
        
    def predict_row(self, x_row: List[float]) -> float:
        """Predict next value using ARIMA model."""
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction.")
        
        # For ARIMA, we predict the differenced series first
        # Then undifference to get the final prediction
        
        # Get the last p values from the fitted series
        # This is a simplified approach - in practice, we'd need to track the series state
        if len(self.diff_history) == 0:
            # No differencing, use AR model directly
            if len(x_row) < self.p:
                # Pad with zeros if not enough lags
                padded_row = [0.0] * (self.p - len(x_row)) + x_row
            else:
                padded_row = x_row[-self.p:]
            
            prediction = self.ar_model.predict([padded_row])[0]
        else:
            # With differencing, we need to reconstruct the prediction
            # This is a simplified implementation
            if len(x_row) < self.p:
                padded_row = [0.0] * (self.p - len(x_row)) + x_row
            else:
                padded_row = x_row[-self.p:]
            
            diff_prediction = self.ar_model.predict([padded_row])[0]
            
            # Undifference: add back the differences
            prediction = diff_prediction
            for i in range(self.d):
                if len(self.diff_history[i]) > 0:
                    prediction += self.diff_history[i][-1]
        
        return float(prediction)
    
    def get_params(self) -> Dict:
        """Get model parameters."""
        return {
            "p": self.p,
            "d": self.d,
            "q": self.q,
            "fitted": self.fitted
        }
    
    def set_params(self, params: Dict) -> None:
        """Set model parameters."""
        self.p = params.get("p", 1)
        self.d = params.get("d", 0)
        self.q = params.get("q", 0)
        self.fitted = params.get("fitted", False)
        
        if self.q != 0:
            raise ValueError("MA terms (q>0) not yet implemented. Use q=0.")


def create(params: Dict) -> ARIMAModel:
    """Create ARIMA model instance."""
    return ARIMAModel(
        p=params.get("p", 1),
        d=params.get("d", 0),
        q=params.get("q", 0)
    )
