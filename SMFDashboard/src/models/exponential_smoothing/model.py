from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "ExponentialSmoothing"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
}


class _ExponentialSmoothing(BaseModel):
    """
    Simple exponential smoothing: y_{t+1} = alpha * y_t + (1-alpha) * y_{t-1}^smoothed
    """

    def __init__(self, alpha: float = 0.3):
        self.alpha = alpha
        self.last_smoothed = None

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not y:
            return
        # Initialize with first value
        self.last_smoothed = float(y[0])
        # Smooth the series
        for val in y:
            self.last_smoothed = self.alpha * float(val) + (1 - self.alpha) * self.last_smoothed

    def predict_row(self, x_row: List[float]) -> float:
        if self.last_smoothed is None:
            # Fallback if not fitted
            return 0.0 if not x_row else float(x_row[0])
        return float(self.last_smoothed)

    def get_params(self) -> Dict:
        return {"alpha": self.alpha, "last_smoothed": self.last_smoothed}

    def set_params(self, params: Dict) -> None:
        self.alpha = params.get("alpha", 0.3)
        self.last_smoothed = params.get("last_smoothed")


def create(params: Dict) -> BaseModel:
    return _ExponentialSmoothing(alpha=params.get("alpha", 0.3))

