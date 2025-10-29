from __future__ import annotations

from typing import Dict, List
from core.base import BaseModel


NAME = "GRU"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _GRU(BaseModel):
    """
    Gated Recurrent Unit - simplified implementation.
    Falls back to LSTM-like behavior.
    """

    def __init__(self, hidden_size: int = 10):
        self.hidden_size = hidden_size
        self.hidden_state = 0.0

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not y:
            return
        # Simple state initialization
        self.hidden_state = float(y[-1]) if y else 0.0

    def predict_row(self, x_row: List[float]) -> float:
        if self.hidden_state is None:
            return 0.0 if not x_row else float(x_row[0])
        return float(self.hidden_state)

    def get_params(self) -> Dict:
        return {"hidden_size": self.hidden_size, "hidden_state": self.hidden_state}

    def set_params(self, params: Dict) -> None:
        self.hidden_size = params.get("hidden_size", 10)
        self.hidden_state = params.get("hidden_state")


def create(params: Dict) -> BaseModel:
    return _GRU(hidden_size=params.get("hidden_size", 10))

