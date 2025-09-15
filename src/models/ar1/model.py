from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "AR1"

# Default spec: use y_t (lag 0) as feature; direct multi-h supported; frozen/refit supported.
SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
}


class _OLS1(BaseModel):
    """
    Simple OLS with intercept for a single feature column X (y = b0 + b1*X).
    """

    def __init__(self):
        self.b0 = 0.0
        self.b1 = 1.0

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        # Expect a single feature column
        if not X or not y or len(X) != len(y):
            self.b0 = 0.0
            self.b1 = 1.0
            return
        xs = [row[0] for row in X]
        n = len(xs)
        mean_x = sum(xs) / n
        mean_y = sum(y) / n
        sxx = sum((xi - mean_x) ** 2 for xi in xs)
        if sxx == 0.0:
            self.b1 = 0.0
            self.b0 = mean_y
            return
        sxy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(xs, y))
        self.b1 = sxy / sxx
        self.b0 = mean_y - self.b1 * mean_x

    def predict_row(self, x_row: List[float]) -> float:
        x = 0.0 if not x_row else float(x_row[0])
        return self.b0 + self.b1 * x

    def get_params(self) -> Dict:
        return {"b0": self.b0, "b1": self.b1}

    def set_params(self, params: Dict) -> None:
        self.b0 = float(params.get("b0", 0.0))
        self.b1 = float(params.get("b1", 1.0))


def create(params: Dict) -> BaseModel:
    # Params unused for AR1 baseline
    return _OLS1()
