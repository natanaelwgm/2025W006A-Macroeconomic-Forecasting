"""
DNS (Dynamic Nelson-Siegel) model implementation for v2.

DNS models are specifically designed for yield curve modeling using
three factors: level, slope, and curvature.
"""

import numpy as np
from typing import Dict, List
from sklearn.linear_model import LinearRegression
from ..core.base import BaseModel, ModelSpec


class DNSModel(BaseModel):
    """
    Dynamic Nelson-Siegel model for yield curve modeling.
    
    Parameters:
    - lambda_decay: Decay parameter for the Nelson-Siegel function
    - n_factors: Number of factors (default: 3 for level, slope, curvature)
    """
    
    NAME = "DNS"
    SPEC = ModelSpec({
        "frequency": "any",
        "input": {
            "target": {"lags": [1, 3, 6, 12]},  # Yield lags
            "exog": {"__all__": {"lags": [0, 1, 3]}}  # Macro variables
        },
        "strategies": ["frozen"],
        "supports_horizons": "any"
    })
    
    def __init__(self, lambda_decay: float = 0.0609, n_factors: int = 3):
        self.lambda_decay = lambda_decay
        self.n_factors = n_factors
        self.model = None
        self.fitted = False
        
    def _nelson_siegel_loading(self, maturity: float) -> np.ndarray:
        """Create Nelson-Siegel loading matrix for given maturity."""
        # Level factor (constant)
        level = 1.0
        
        # Slope factor (exponential decay)
        slope = (1 - np.exp(-self.lambda_decay * maturity)) / (self.lambda_decay * maturity)
        
        # Curvature factor (hump-shaped)
        curvature = slope - np.exp(-self.lambda_decay * maturity)
        
        return np.array([level, slope, curvature])
    
    def _extract_factors(self, X: List[List[float]], y: List[float]) -> np.ndarray:
        """Extract DNS factors from yield data."""
        # Simplified factor extraction - in practice would use Kalman filter
        # For now, use principal components as proxy for factors
        
        # Combine target and features for factor extraction
        data_matrix = np.column_stack([y] + [col for col in zip(*X)])
        
        # Use PCA to extract factors
        from sklearn.decomposition import PCA
        pca = PCA(n_components=self.n_factors)
        factors = pca.fit_transform(data_matrix)
        
        return factors
    
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        """Fit DNS model to the data."""
        # Extract factors
        factors = self._extract_factors(X, y)
        
        # Fit linear model on factors
        self.model = LinearRegression()
        self.model.fit(factors, y)
        
        self.fitted = True
        
    def predict_row(self, x_row: List[float]) -> float:
        """Predict next value using DNS model."""
        if not self.fitted:
            raise ValueError("Model must be fitted before prediction.")
        
        # For prediction, we need to estimate factors from current features
        # This is simplified - in practice would use Kalman filter
        
        # Use the last n_factors values as proxy for factors
        if len(x_row) >= self.n_factors:
            factors = np.array(x_row[:self.n_factors]).reshape(1, -1)
        else:
            # Pad with zeros if not enough features
            factors = np.zeros((1, self.n_factors))
            factors[0, :len(x_row)] = x_row
        
        prediction = self.model.predict(factors)[0]
        return float(prediction)
    
    def get_params(self) -> Dict:
        """Get model parameters."""
        return {
            "lambda_decay": self.lambda_decay,
            "n_factors": self.n_factors,
            "fitted": self.fitted
        }
    
    def set_params(self, params: Dict) -> None:
        """Set model parameters."""
        self.lambda_decay = params.get("lambda_decay", 0.0609)
        self.n_factors = params.get("n_factors", 3)
        self.fitted = params.get("fitted", False)


def create(params: Dict) -> DNSModel:
    """Create DNS model instance."""
    return DNSModel(
        lambda_decay=params.get("lambda_decay", 0.0609),
        n_factors=params.get("n_factors", 3)
    )
