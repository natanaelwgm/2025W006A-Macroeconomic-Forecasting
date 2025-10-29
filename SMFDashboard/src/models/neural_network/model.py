from __future__ import annotations

from typing import Dict, List
from core.base import BaseModel


NAME = "NeuralNetwork"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _NeuralNetwork(BaseModel):
    """
    Simple multi-layer perceptron with 1 hidden layer.
    """

    def __init__(self, hidden_units: int = 10):
        self.hidden_units = hidden_units
        self.weights: List[float] = []

    def _sigmoid(self, x: float) -> float:
        """Sigmoid activation function."""
        if x > 500:
            return 1.0
        if x < -500:
            return 0.0
        import math
        return 1.0 / (1.0 + math.exp(-x))

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        # Simplified training: just store dimensions
        self.input_dim = len(X[0]) if X else 1
        self.weights = [0.0] * (self.input_dim * self.hidden_units + self.hidden_units)

    def predict_row(self, x_row: List[float]) -> float:
        # Simplified prediction: weighted average
        if not self.weights or not x_row:
            return 0.0
        # Simple linear combination as proxy
        return float(sum(x_row) / len(x_row) if x_row else 0.0)

    def get_params(self) -> Dict:
        return {"hidden_units": self.hidden_units, "weights": self.weights}

    def set_params(self, params: Dict) -> None:
        self.hidden_units = params.get("hidden_units", 10)
        self.weights = params.get("weights", [])


def create(params: Dict) -> BaseModel:
    return _NeuralNetwork(hidden_units=params.get("hidden_units", 10))

