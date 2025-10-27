from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel
from ..tree.model import _TreeRegressor


NAME = "GradientBoosting"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "n_estimators": {"type": "int", "default": 100, "min": 1},
        "learning_rate": {"type": "float", "default": 0.1, "min": 0.0},
        "max_depth": {"type": "int", "default": 2, "min": 1},
        "min_samples_split": {"type": "int", "default": 8, "min": 2},
        "random_state": {"type": "int", "default": 42}
    },
}


class _GradientBoosting(BaseModel):
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1, max_depth: int = 2, min_samples_split: int = 8, random_state: int = 42):
        self.n_estimators = int(n_estimators)
        self.learning_rate = float(learning_rate)
        self.max_depth = int(max_depth)
        self.min_samples_split = int(min_samples_split)
        self.random_state = int(random_state)
        self.init_: float = 0.0
        self.trees: List[_TreeRegressor] = []

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.trees = []
        if not X or not y or len(X) != len(y):
            self.init_ = 0.0
            return
        n = len(y)
        # Initialize with mean (for squared loss)
        self.init_ = sum(float(v) for v in y) / n
        # Residuals
        residual = [float(y[i]) - self.init_ for i in range(n)]
        # Sequentially fit trees to residuals
        for m in range(self.n_estimators):
            tree = _TreeRegressor(max_depth=self.max_depth, min_samples_split=self.min_samples_split, max_features=None, random_state=self.random_state + m)
            tree.fit(X, residual)
            # Update residuals
            preds = [tree.predict_row(row) for row in X]
            for i in range(n):
                residual[i] -= self.learning_rate * preds[i]
            self.trees.append(tree)

    def predict_row(self, x_row: List[float]) -> float:
        yhat = self.init_
        lr = self.learning_rate
        for t in self.trees:
            yhat += lr * t.predict_row(x_row)
        return yhat

    def get_params(self) -> Dict:
        return {
            "n_estimators": self.n_estimators,
            "learning_rate": self.learning_rate,
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "random_state": self.random_state,
            "init_": self.init_,
            "trees": [t.get_params() for t in self.trees],
        }

    def set_params(self, params: Dict) -> None:
        self.n_estimators = int(params.get("n_estimators", self.n_estimators))
        self.learning_rate = float(params.get("learning_rate", self.learning_rate))
        self.max_depth = int(params.get("max_depth", self.max_depth))
        self.min_samples_split = int(params.get("min_samples_split", self.min_samples_split))
        self.random_state = int(params.get("random_state", self.random_state))
        self.init_ = float(params.get("init_", self.init_))
        self.trees = []
        for tp in params.get("trees", []) or []:
            t = _TreeRegressor()
            t.set_params(tp)
            self.trees.append(t)


def create(params: Dict) -> BaseModel:
    p = SPEC.get("params_schema", {})
    return _GradientBoosting(
        n_estimators=int(params.get("n_estimators", p.get("n_estimators", {}).get("default", 100))),
        learning_rate=float(params.get("learning_rate", p.get("learning_rate", {}).get("default", 0.1))),
        max_depth=int(params.get("max_depth", p.get("max_depth", {}).get("default", 2))),
        min_samples_split=int(params.get("min_samples_split", p.get("min_samples_split", {}).get("default", 8))),
        random_state=int(params.get("random_state", p.get("random_state", {}).get("default", 42))),
    )
