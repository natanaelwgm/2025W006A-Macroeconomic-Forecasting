from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "SVR"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _SVR(BaseModel):
    """
    Support Vector Regression - simplified implementation.
    Falls back to linear regression.
    """

    def __init__(self, epsilon: float = 0.1, C: float = 1.0):
        self.epsilon = epsilon
        self.C = C
        # Simple linear model as fallback
        self.slope = 0.0
        self.intercept = 0.0

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y:
            return
        # Simple linear regression
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
        return {"epsilon": self.epsilon, "C": self.C, "slope": self.slope, "intercept": self.intercept}

    def set_params(self, params: Dict) -> None:
        self.epsilon = params.get("epsilon", 0.1)
        self.C = params.get("C", 1.0)
        self.slope = params.get("slope", 0.0)
        self.intercept = params.get("intercept", 0.0)


def create(params: Dict) -> BaseModel:
    return _SVR(epsilon=params.get("epsilon", 0.1), C=params.get("C", 1.0))

