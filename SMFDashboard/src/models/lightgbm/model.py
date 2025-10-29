from __future__ import annotations

from typing import Dict, List
from core.base import BaseModel


NAME = "LightGBM"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _LightGBM(BaseModel):
    """
    LightGBM gradient boosting - simplified fallback implementation.
    Note: Full LightGBM requires 'lightgbm' package installation.
    Falls back to simple linear combination.
    """

    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.slope = 0.0
        self.intercept = 0.0

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y:
            return
        # Simple linear regression as fallback
        n = len(X)
        sum_x = sum(row[0] if row else 0 for row in X)
        sum_y = sum(y)
        sum_xy = sum((row[0] if row else 0) * val for row, val in zip(X, y))
        sum_x2 = sum((row[0] if row else 0) ** 2 for row in X)
        
        if sum_x2 == 0:
            self.slope = 0.0
            self.intercept = sum_y / n if n > 0 else 0.0
        else:
            self.slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
            self.intercept = (sum_y - self.slope * sum_x) / n

    def predict_row(self, x_row: List[float]) -> float:
        if not x_row:
            return self.intercept
        return float(self.slope * x_row[0] + self.intercept)

    def get_params(self) -> Dict:
        return {"n_estimators": self.n_estimators, "learning_rate": self.learning_rate,
                "slope": self.slope, "intercept": self.intercept}

    def set_params(self, params: Dict) -> None:
        self.n_estimators = params.get("n_estimators", 100)
        self.learning_rate = params.get("learning_rate", 0.1)
        self.slope = params.get("slope", 0.0)
        self.intercept = params.get("intercept", 0.0)


def create(params: Dict) -> BaseModel:
    return _LightGBM(
        n_estimators=params.get("n_estimators", 100),
        learning_rate=params.get("learning_rate", 0.1)
    )

