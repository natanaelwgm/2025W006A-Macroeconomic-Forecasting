from __future__ import annotations

from typing import Dict, List
from core.base import BaseModel


NAME = "SARIMAX"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": []}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _SARIMAX(BaseModel):
    """
    Seasonal ARIMA with eXogenous regressors.
    Simplified implementation.
    """

    def __init__(self, p: int = 1, d: int = 0, q: int = 1, s: int = 12):
        self.p = p
        self.d = d
        self.q = q
        self.s = s
        self.last_values = []

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not y:
            return
        # Store last s observations for seasonal component
        self.last_values = y[-self.s:] if len(y) >= self.s else y.copy()

    def predict_row(self, x_row: List[float]) -> float:
        if not self.last_values:
            return 0.0 if not x_row else float(x_row[0])
        # Use seasonal average
        return float(sum(self.last_values) / len(self.last_values))

    def get_params(self) -> Dict:
        return {"p": self.p, "d": self.d, "q": self.q, "s": self.s, "last_values": self.last_values}

    def set_params(self, params: Dict) -> None:
        self.p = params.get("p", 1)
        self.d = params.get("d", 0)
        self.q = params.get("q", 1)
        self.s = params.get("s", 12)
        self.last_values = params.get("last_values", [])


def create(params: Dict) -> BaseModel:
    return _SARIMAX(
        p=params.get("p", 1),
        d=params.get("d", 0),
        q=params.get("q", 1),
        s=params.get("s", 12)
    )

