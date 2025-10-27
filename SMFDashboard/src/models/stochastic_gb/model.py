from __future__ import annotations

from typing import Dict, List, Optional, Union
import random as _random

from core.base import BaseModel
from ..tree.model import _TreeRegressor


NAME = "StochasticGB"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "n_estimators": {"type": "int", "default": 100, "min": 1},
        "learning_rate": {"type": "float", "default": 0.1, "min": 0.0},
        "subsample": {"type": "float", "default": 0.7, "min": 0.1, "max": 1.0},
        "max_depth": {"type": "int", "default": 2, "min": 1},
        "min_samples_split": {"type": "int", "default": 8, "min": 2},
        "max_features": {"type": "str|int", "default": "sqrt"},
        "random_state": {"type": "int", "default": 42}
    },
}


class _StochasticGB(BaseModel):
    def __init__(self, n_estimators: int = 100, learning_rate: float = 0.1, subsample: float = 0.7, max_depth: int = 2, min_samples_split: int = 8, max_features: Optional[Union[int, str]] = "sqrt", random_state: int = 42):
        self.n_estimators = int(n_estimators)
        self.learning_rate = float(learning_rate)
        self.subsample = float(subsample)
        self.max_depth = int(max_depth)
        self.min_samples_split = int(min_samples_split)
        self.max_features = max_features
        self.random_state = int(random_state)
        self.init_: float = 0.0
        self.trees: List[_TreeRegressor] = []
        self._rng = _random.Random(self.random_state)

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.trees = []
        if not X or not y or len(X) != len(y):
            self.init_ = 0.0
            return
        n = len(y)
        # Initial prediction is mean
        self.init_ = sum(float(v) for v in y) / n
        residual = [float(y[i]) - self.init_ for i in range(n)]
        msize = max(1, min(n, int(round(self.subsample * n))))
        for m in range(self.n_estimators):
            # sample without replacement indices for fitting
            idx = list(range(n))
            self._rng.shuffle(idx)
            idx = idx[:msize]
            Xs = [X[i] for i in idx]
            rs = [residual[i] for i in idx]
            t = _TreeRegressor(max_depth=self.max_depth, min_samples_split=self.min_samples_split, max_features=self.max_features, random_state=self._rng.randrange(0, 1_000_000))
            t.fit(Xs, rs)
            # Update residuals on full dataset
            lr = self.learning_rate
            for i, row in enumerate(X):
                residual[i] -= lr * t.predict_row(row)
            self.trees.append(t)

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
            "subsample": self.subsample,
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "max_features": self.max_features,
            "random_state": self.random_state,
            "init_": self.init_,
            "trees": [t.get_params() for t in self.trees],
        }

    def set_params(self, params: Dict) -> None:
        self.n_estimators = int(params.get("n_estimators", self.n_estimators))
        self.learning_rate = float(params.get("learning_rate", self.learning_rate))
        self.subsample = float(params.get("subsample", self.subsample))
        self.max_depth = int(params.get("max_depth", self.max_depth))
        self.min_samples_split = int(params.get("min_samples_split", self.min_samples_split))
        self.max_features = params.get("max_features", self.max_features)
        self.random_state = int(params.get("random_state", self.random_state))
        self.init_ = float(params.get("init_", self.init_))
        self._rng = _random.Random(self.random_state)
        self.trees = []
        for tp in params.get("trees", []) or []:
            t = _TreeRegressor()
            t.set_params(tp)
            self.trees.append(t)


def create(params: Dict) -> BaseModel:
    p = SPEC.get("params_schema", {})
    return _StochasticGB(
        n_estimators=int(params.get("n_estimators", p.get("n_estimators", {}).get("default", 100))),
        learning_rate=float(params.get("learning_rate", p.get("learning_rate", {}).get("default", 0.1))),
        subsample=float(params.get("subsample", p.get("subsample", {}).get("default", 0.7))),
        max_depth=int(params.get("max_depth", p.get("max_depth", {}).get("default", 2))),
        min_samples_split=int(params.get("min_samples_split", p.get("min_samples_split", {}).get("default", 8))),
        max_features=params.get("max_features", p.get("max_features", {}).get("default", "sqrt")),
        random_state=int(params.get("random_state", p.get("random_state", {}).get("default", 42))),
    )

