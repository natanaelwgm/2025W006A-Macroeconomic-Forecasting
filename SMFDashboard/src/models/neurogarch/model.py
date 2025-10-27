"""
NeuroGARCH model implementation for v2.

NeuroGARCH combines GARCH volatility modeling with neural network
corrections for improved variance forecasting.
"""

import numpy as np
from typing import Dict, List
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
import sys
from pathlib import Path

# Fix import path - go up to src directory
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from core.base import BaseModel, ModelSpec

# Define at module level for registry discovery
NAME = "NeuroGARCH"
SPEC = {
    "frequency": "any",
    "input": {
        "target": {"lags": [1, 3, 6, 12]},
        "exog": {"__all__": {"lags": [0, 1, 3]}}
    },
    "strategies": ["frozen"],
    "supports_horizons": "any"
}


class NeuroGARCHModel(BaseModel):
    """
    NeuroGARCH model combining GARCH with neural network corrections.
    
    Parameters:
    - garch_p: GARCH autoregressive order
    - garch_q: GARCH moving average order
    - nn_hidden_layers: Number of hidden layers in neural network
    - nn_hidden_units: Number of units per hidden layer
    """
    def __init__(self, garch_p: int = 1, garch_q: int = 1, 
                 nn_hidden_layers: int = 2, nn_hidden_units: int = 10):
        self.garch_p = garch_p
        self.garch_q = garch_q
        self.nn_hidden_layers = nn_hidden_layers
        self.nn_hidden_units = nn_hidden_units
        
        self.garch_model = None
        self.nn_model = None
        self.fitted = False
        
    def _estimate_garch_volatility(self, y: List[float]) -> List[float]:
        """Estimate GARCH volatility using simplified approach."""
        y_array = np.array(y)
        
        # Calculate returns (first difference)
        returns = np.diff(y_array)
        
        # Simple GARCH(1,1) volatility estimation
        volatility = []
        vol_sq = np.var(returns)  # Initial volatility
        
        for i in range(len(returns)):
            # GARCH(1,1) update: sigma^2 = omega + alpha * r^2 + beta * sigma^2
            omega = 0.01
            alpha = 0.1
            beta = 0.85
            
            vol_sq = omega + alpha * returns[i]**2 + beta * vol_sq
            volatility.append(np.sqrt(vol_sq))
        
        # Pad with initial volatility for first observation
        volatility = [np.sqrt(np.var(returns))] + volatility
        
        return volatility
    
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        """Fit NeuroGARCH model."""
        # Estimate GARCH volatility
        volatility = self._estimate_garch_volatility(y)
        
        # Fit GARCH model (simplified linear model on volatility)
        self.garch_model = LinearRegression()
        
        # Create features for GARCH model (lagged volatility and returns)
        garch_features = []
        garch_targets = []
        
        for i in range(max(self.garch_p, self.garch_q), len(y)):
            # Features: lagged volatilities and returns
            feat = []
            for lag in range(1, self.garch_p + 1):
                if i - lag >= 0:
                    feat.append(volatility[i - lag])
                else:
                    feat.append(volatility[0])
            
            for lag in range(1, self.garch_q + 1):
                if i - lag >= 0:
                    feat.append((y[i - lag] - y[i - lag - 1])**2 if i - lag - 1 >= 0 else 0)
                else:
                    feat.append(0)
            
            garch_features.append(feat)
            garch_targets.append(volatility[i])
        
        if len(garch_features) > 0:
            self.garch_model.fit(garch_features, garch_targets)
        
        # Fit neural network correction model
        self.nn_model = MLPRegressor(
            hidden_layer_sizes=(self.nn_hidden_units,) * self.nn_hidden_layers,
            max_iter=1000,
            random_state=42
        )
        
        # Create features for neural network (original features + volatility)
        nn_features = []
        nn_targets = []
        
        for i in range(len(X)):
            if i < len(volatility):
                # Combine original features with volatility
                combined_feat = X[i] + [volatility[i]]
                nn_features.append(combined_feat)
                nn_targets.append(y[i])
        
        if len(nn_features) > 0:
            self.nn_model.fit(nn_features, nn_targets)
        
        self.fitted = True
        
    def predict_row(self, x_row: List[float]) -> float:
        """Predict next value using NeuroGARCH model."""
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction.")
        
        # Predict using neural network (primary prediction)
        if self.nn_model is not None:
            # Estimate volatility for this prediction
            # This is simplified - in practice would use GARCH forecast
            estimated_vol = np.std(x_row) if len(x_row) > 1 else 1.0
            
            # Combine features with estimated volatility
            combined_feat = x_row + [estimated_vol]
            prediction = self.nn_model.predict([combined_feat])[0]
        else:
            # Fallback to simple linear prediction
            prediction = np.mean(x_row) if len(x_row) > 0 else 0.0
        
        return float(prediction)
    
    def get_params(self) -> Dict:
        """Get model parameters."""
        return {
            "garch_p": self.garch_p,
            "garch_q": self.garch_q,
            "nn_hidden_layers": self.nn_hidden_layers,
            "nn_hidden_units": self.nn_hidden_units,
            "fitted": self.fitted
        }
    
    def set_params(self, params: Dict) -> None:
        """Set model parameters."""
        self.garch_p = params.get("garch_p", 1)
        self.garch_q = params.get("garch_q", 1)
        self.nn_hidden_layers = params.get("nn_hidden_layers", 2)
        self.nn_hidden_units = params.get("nn_hidden_units", 10)
        self.fitted = params.get("fitted", False)


def create(params: Dict) -> NeuroGARCHModel:
    """Create NeuroGARCH model instance."""
    return NeuroGARCHModel(
        garch_p=params.get("garch_p", 1),
        garch_q=params.get("garch_q", 1),
        nn_hidden_layers=params.get("nn_hidden_layers", 2),
        nn_hidden_units=params.get("nn_hidden_units", 10)
    )
