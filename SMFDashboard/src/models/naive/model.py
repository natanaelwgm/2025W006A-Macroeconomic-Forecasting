from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "Naive"

SPEC = {
    "frequency": "any",
    # Requires current y_t as a feature (lag 0)
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
}


class _Naive(BaseModel):
    """
    Returns the first feature as the forecast (assumes y__lag0 is the first column).
    """

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        # No parameters
        return

    def predict_row(self, x_row: List[float]) -> float:
        return 0.0 if not x_row else float(x_row[0])

    def get_params(self) -> Dict:
        return {}

    def set_params(self, params: Dict) -> None:
        return


def create(params: Dict) -> BaseModel:
    return _Naive()
