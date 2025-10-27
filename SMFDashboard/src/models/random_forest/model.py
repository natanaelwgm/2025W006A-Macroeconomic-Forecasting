from __future__ import annotations

from typing import Dict, List, Optional, Union
import random as _random

from core.base import BaseModel
from ..tree.model import _TreeRegressor


NAME = "RandomForest"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "n_estimators": {"type": "int", "default": 50, "min": 1},
        "max_depth": {"type": "int", "default": 4, "min": 1},
        "min_samples_split": {"type": "int", "default": 8, "min": 2},
        "max_features": {"type": "str|int", "default": "sqrt"},
        "bootstrap": {"type": "bool", "default": True},
        "random_state": {"type": "int", "default": 42},
    },
}


class _RandomForest(BaseModel):
    def __init__(self, n_estimators: int = 50, max_depth: int = 4, min_samples_split: int = 8, max_features: Optional[Union[int, str]] = "sqrt", bootstrap: bool = True, random_state: int = 42):
        self.n_estimators = int(n_estimators)
        self.max_depth = int(max_depth)
        self.min_samples_split = int(min_samples_split)
        self.max_features = max_features
        self.bootstrap = bool(bootstrap)
        self.random_state = int(random_state)
        self.trees: List[_TreeRegressor] = []
        self._rng = _random.Random(self.random_state)

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.trees = []
        if not X or not y or len(X) != len(y):
            return
        n = len(y)
        for i in range(self.n_estimators):
            # Bootstrap sample indices
            if self.bootstrap:
                idx = [self._rng.randrange(0, n) for _ in range(n)]
            else:
                idx = list(range(n))
                self._rng.shuffle(idx)
            Xb = [X[j] for j in idx]
            yb = [y[j] for j in idx]
            tree = _TreeRegressor(
                max_depth=self.max_depth,
                min_samples_split=self.min_samples_split,
                max_features=self.max_features,
                random_state=self._rng.randrange(0, 1_000_000),
            )
            tree.fit(Xb, yb)
            self.trees.append(tree)

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
            "max_features": self.max_features,
            "bootstrap": self.bootstrap,
            "random_state": self.random_state,
            "trees": [t.get_params() for t in self.trees],
        }

    def set_params(self, params: Dict) -> None:
        self.n_estimators = int(params.get("n_estimators", self.n_estimators))
        self.max_depth = int(params.get("max_depth", self.max_depth))
        self.min_samples_split = int(params.get("min_samples_split", self.min_samples_split))
        self.max_features = params.get("max_features", self.max_features)
        self.bootstrap = bool(params.get("bootstrap", self.bootstrap))
        self.random_state = int(params.get("random_state", self.random_state))
        self._rng = _random.Random(self.random_state)
        self.trees = []
        for tp in params.get("trees", []) or []:
            t = _TreeRegressor()
            t.set_params(tp)
            self.trees.append(t)


def create(params: Dict) -> BaseModel:
    p = SPEC.get("params_schema", {})
    return _RandomForest(
        n_estimators=int(params.get("n_estimators", p.get("n_estimators", {}).get("default", 50))),
        max_depth=int(params.get("max_depth", p.get("max_depth", {}).get("default", 4))),
        min_samples_split=int(params.get("min_samples_split", p.get("min_samples_split", {}).get("default", 8))),
        max_features=params.get("max_features", p.get("max_features", {}).get("default", "sqrt")),
        bootstrap=bool(params.get("bootstrap", p.get("bootstrap", {}).get("default", True))),
        random_state=int(params.get("random_state", p.get("random_state", {}).get("default", 42))),
    )
