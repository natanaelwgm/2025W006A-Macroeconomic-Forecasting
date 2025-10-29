from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "KNN"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen"],
    "supports_horizons": "any",
}


class _KNN(BaseModel):
    """
    K-Nearest Neighbors regressor.
    """

    def __init__(self, n_neighbors: int = 5):
        self.n_neighbors = n_neighbors
        self.X_train: List[List[float]] = []
        self.y_train: List[float] = []

    def _distance(self, x1: List[float], x2: List[float]) -> float:
        """Calculate Euclidean distance."""
        return sum((a - b) ** 2 for a, b in zip(x1, x2)) ** 0.5

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.X_train = X
        self.y_train = y

    def predict_row(self, x_row: List[float]) -> float:
        if not self.X_train:
            return 0.0
        
        # Find k nearest neighbors
        distances = [(self._distance(x_row, x), y) for x, y in zip(self.X_train, self.y_train)]
        distances.sort()
        
        # Take average of k nearest
        k = min(self.n_neighbors, len(distances))
        return float(sum(distances[i][1] for i in range(k)) / k)

    def get_params(self) -> Dict:
        return {"n_neighbors": self.n_neighbors}

    def set_params(self, params: Dict) -> None:
        self.n_neighbors = params.get("n_neighbors", 5)


def create(params: Dict) -> BaseModel:
    return _KNN(n_neighbors=params.get("n_neighbors", 5))

