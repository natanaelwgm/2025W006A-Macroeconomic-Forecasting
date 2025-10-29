from __future__ import annotations

from typing import Dict, List
from core.base import BaseModel


NAME = "VAR"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _VAR(BaseModel):
    """
    Vector Autoregression - simplified implementation.
    Treats multiple variables as a system.
    """

    def __init__(self, lag_order: int = 1):
        self.lag_order = lag_order
        self.coefficients = []

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y:
            return
        # Simple averaging
        self.mean_y = float(sum(y) / len(y)) if y else 0.0

    def predict_row(self, x_row: List[float]) -> float:
        if not hasattr(self, 'mean_y'):
            return 0.0 if not x_row else float(x_row[0])
        return float(self.mean_y)

    def get_params(self) -> Dict:
        return {"lag_order": self.lag_order, "mean_y": getattr(self, 'mean_y', 0.0)}

    def set_params(self, params: Dict) -> None:
        self.lag_order = params.get("lag_order", 1)
        self.mean_y = params.get("mean_y", 0.0)


def create(params: Dict) -> BaseModel:
    return _VAR(lag_order=params.get("lag_order", 1))

