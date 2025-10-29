from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "MovingAverage"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": list(range(12))}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
}


class _MovingAverage(BaseModel):
    """
    Moving Average model: returns the average of the last n observations.
    Default window size = 3
    """

    def __init__(self, window: int = 3):
        self.window = window

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        # No parameters to fit
        return

    def predict_row(self, x_row: List[float]) -> float:
        if not x_row:
            return 0.0
        # Average of the last window observations
        recent_values = x_row[:self.window] if len(x_row) >= self.window else x_row
        return float(sum(recent_values) / len(recent_values))

    def get_params(self) -> Dict:
        return {"window": self.window}

    def set_params(self, params: Dict) -> None:
        self.window = params.get("window", 3)


def create(params: Dict) -> BaseModel:
    return _MovingAverage(window=params.get("window", 3))

