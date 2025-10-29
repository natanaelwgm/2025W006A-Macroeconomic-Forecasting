from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "Drift"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0, 1]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
}


class _Drift(BaseModel):
    """
    Drift model: y_{t+h} = y_t + h * (y_t - y_{t-1})
    Forecast = last value + h * (last value - second last value)
    """

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        # No parameters to fit
        return

    def predict_row(self, x_row: List[float]) -> float:
        if not x_row or len(x_row) < 2:
            return 0.0
        # Assuming x_row[0] = y_t, x_row[1] = y_{t-1}
        y_t = float(x_row[0])
        y_tm1 = float(x_row[1])
        drift = y_t - y_tm1
        # For h=1: y_{t+1} = y_t + drift
        return float(y_t + drift)

    def get_params(self) -> Dict:
        return {}

    def set_params(self, params: Dict) -> None:
        return


def create(params: Dict) -> BaseModel:
    return _Drift()

