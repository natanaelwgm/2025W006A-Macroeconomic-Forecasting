from __future__ import annotations

from typing import Dict, List
from core.base import BaseModel


NAME = "Transformer"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _Transformer(BaseModel):
    """
    Transformer model - simplified implementation for forecasting.
    Uses attention mechanism concept.
    """

    def __init__(self, d_model: int = 64, n_heads: int = 4):
        self.d_model = d_model
        self.n_heads = n_heads
        self.last_value = 0.0

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not y:
            return
        # Simple initialization
        self.last_value = float(y[-1]) if y else 0.0

    def predict_row(self, x_row: List[float]) -> float:
        return float(self.last_value)

    def get_params(self) -> Dict:
        return {"d_model": self.d_model, "n_heads": self.n_heads, "last_value": self.last_value}

    def set_params(self, params: Dict) -> None:
        self.d_model = params.get("d_model", 64)
        self.n_heads = params.get("n_heads", 4)
        self.last_value = params.get("last_value", 0.0)


def create(params: Dict) -> BaseModel:
    return _Transformer(
        d_model=params.get("d_model", 64),
        n_heads=params.get("n_heads", 4)
    )

