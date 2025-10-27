from __future__ import annotations

from typing import Dict, List
import random as _random

from core.base import BaseModel
from ..tree.model import _TreeRegressor


NAME = "Bagging"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "n_estimators": {"type": "int", "default": 30, "min": 1},
        "max_depth": {"type": "int", "default": 4, "min": 1},
        "min_samples_split": {"type": "int", "default": 8, "min": 2},
        "bootstrap": {"type": "bool", "default": True},
        "max_samples": {"type": "float", "default": 1.0, "min": 0.1, "max": 1.0},
        "random_state": {"type": "int", "default": 42},
    },
}


class _Bagging(BaseModel):
    def __init__(self, n_estimators: int = 30, max_depth: int = 4, min_samples_split: int = 8, bootstrap: bool = True, max_samples: float = 1.0, random_state: int = 42):
        self.n_estimators = int(n_estimators)
        self.max_depth = int(max_depth)
        self.min_samples_split = int(min_samples_split)
        self.bootstrap = bool(bootstrap)
        self.max_samples = float(max_samples)
        self.random_state = int(random_state)
        self.trees: List[_TreeRegressor] = []
        self._rng = _random.Random(self.random_state)

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.trees = []
        if not X or not y or len(X) != len(y):
            return
        n = len(y)
        m = max(1, min(n, int(round(self.max_samples * n))))
        for i in range(self.n_estimators):
            if self.bootstrap:
                idx = [self._rng.randrange(0, n) for _ in range(m)]
            else:
                idx = list(range(n))
                self._rng.shuffle(idx)
                idx = idx[:m]
            Xb = [X[j] for j in idx]
            yb = [y[j] for j in idx]
            t = _TreeRegressor(max_depth=self.max_depth, min_samples_split=self.min_samples_split, max_features=None, random_state=self._rng.randrange(0, 1_000_000))
            t.fit(Xb, yb)
            self.trees.append(t)

    def predict_row(self, x_row: List[float]) -> float:
        if not self.trees:
            return 0.0
        s = 0.0
        for t in self.trees:
            s += t.predict_row(x_row)
        return s / len(self.trees)

    def get_params(self) -> Dict:
        return {
            "n_estimators": self.n_estimators,
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "bootstrap": self.bootstrap,
            "max_samples": self.max_samples,
            "random_state": self.random_state,
            "trees": [t.get_params() for t in self.trees],
        }

    def set_params(self, params: Dict) -> None:
        self.n_estimators = int(params.get("n_estimators", self.n_estimators))
        self.max_depth = int(params.get("max_depth", self.max_depth))
        self.min_samples_split = int(params.get("min_samples_split", self.min_samples_split))
        self.bootstrap = bool(params.get("bootstrap", self.bootstrap))
        self.max_samples = float(params.get("max_samples", self.max_samples))
        self.random_state = int(params.get("random_state", self.random_state))
        self._rng = _random.Random(self.random_state)
        self.trees = []
        for tp in params.get("trees", []) or []:
            t = _TreeRegressor()
            t.set_params(tp)
            self.trees.append(t)


def create(params: Dict) -> BaseModel:
    p = SPEC.get("params_schema", {})
    return _Bagging(
        n_estimators=int(params.get("n_estimators", p.get("n_estimators", {}).get("default", 30))),
        max_depth=int(params.get("max_depth", p.get("max_depth", {}).get("default", 4))),
        min_samples_split=int(params.get("min_samples_split", p.get("min_samples_split", {}).get("default", 8))),
        bootstrap=bool(params.get("bootstrap", p.get("bootstrap", {}).get("default", True))),
        max_samples=float(params.get("max_samples", p.get("max_samples", {}).get("default", 1.0))),
        random_state=int(params.get("random_state", p.get("random_state", {}).get("default", 42))),
    )

