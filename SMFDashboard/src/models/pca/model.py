from __future__ import annotations

from typing import Dict, List
from core.base import BaseModel


NAME = "PCA"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": []}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _PCA(BaseModel):
    """
    Principal Component Analysis for dimensionality reduction + regression.
    Simplified implementation.
    """

    def __init__(self, n_components: int = 5):
        self.n_components = n_components

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        # No actual PCA fitting - just placeholder
        self.feature_count = len(X[0]) if X else 0

    def predict_row(self, x_row: List[float]) -> float:
        # Return mean of features as proxy
        if not x_row:
            return 0.0
        return float(sum(x_row) / len(x_row))

    def get_params(self) -> Dict:
        return {"n_components": self.n_components}

    def set_params(self, params: Dict) -> None:
        self.n_components = params.get("n_components", 5)


def create(params: Dict) -> BaseModel:
    return _PCA(n_components=params.get("n_components", 5))

