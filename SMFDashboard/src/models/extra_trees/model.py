from __future__ import annotations

from typing import Dict, List, Optional, Tuple
import random as _random

from core.base import BaseModel
from ..tree.model import _TreeNode, _mean, _sse


NAME = "ExtraTrees"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "n_estimators": {"type": "int", "default": 100, "min": 1},
        "max_depth": {"type": "int", "default": 4, "min": 1},
        "min_samples_split": {"type": "int", "default": 8, "min": 2},
        "max_features": {"type": "str|int", "default": "sqrt"},
        "n_thresholds": {"type": "int", "default": 16, "min": 1},
        "random_state": {"type": "int", "default": 42},
    },
}


class _ExtraTree(BaseModel):
    def __init__(self, max_depth: int = 4, min_samples_split: int = 8, max_features: Optional[object] = "sqrt", n_thresholds: int = 16, random_state: int = 42):
        self.max_depth = int(max_depth)
        self.min_samples_split = int(min_samples_split)
        self.max_features = max_features
        self.n_thresholds = int(n_thresholds)
        self.random_state = int(random_state)
        self.root: Optional[_TreeNode] = None
        self._rng = _random.Random(self.random_state)

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.root = None
            return
        n_features = len(X[0]) if X else 0
        self.root = self._build_node(X, y, depth=0, feature_indices=list(range(n_features)))

    def predict_row(self, x_row: List[float]) -> float:
        node = self.root
        if node is None:
            return 0.0
        while node and node.feature is not None and node.left is not None and node.right is not None:
            j = node.feature
            thr = node.threshold if node.threshold is not None else 0.0
            xj = float(x_row[j]) if (x_row is not None and j < len(x_row)) else 0.0
            node = node.left if xj <= thr else node.right
        return node.value if node else 0.0

    def get_params(self) -> Dict:
        return {
            "max_depth": self.max_depth,
            "min_samples_split": self.min_samples_split,
            "max_features": self.max_features,
            "n_thresholds": self.n_thresholds,
            "random_state": self.random_state,
            "tree": self._serialize_node(self.root),
        }

    def set_params(self, params: Dict) -> None:
        self.max_depth = int(params.get("max_depth", self.max_depth))
        self.min_samples_split = int(params.get("min_samples_split", self.min_samples_split))
        self.max_features = params.get("max_features", self.max_features)
        self.n_thresholds = int(params.get("n_thresholds", self.n_thresholds))
        self.random_state = int(params.get("random_state", self.random_state))
        self._rng = _random.Random(self.random_state)
        self.root = self._deserialize_node(params.get("tree"))

    # --- helpers ---
    def _resolve_max_features(self, m: int) -> int:
        mf = self.max_features
        if mf is None:
            return m
        if isinstance(mf, int):
            return max(1, min(m, mf))
        s = str(mf).lower()
        if s == "sqrt":
            import math
            return max(1, int(math.sqrt(m)))
        if s in ("log2", "log"):
            import math
            return max(1, int(math.log2(m)))
        return m

    def _build_node(self, X: List[List[float]], y: List[float], depth: int, feature_indices: List[int]) -> _TreeNode:
        node = _TreeNode()
        node.n = len(y)
        node.value = _mean(y)
        if depth >= self.max_depth or len(y) < self.min_samples_split:
            return node
        m = len(feature_indices)
        k = self._resolve_max_features(m)
        features = feature_indices[:]
        self._rng.shuffle(features)
        features = features[:k]

        split = self._random_best_split(X, y, features)
        if split is None:
            return node
        feat, thr, left_idx, right_idx = split
        if not left_idx or not right_idx:
            return node
        node.feature = feat
        node.threshold = thr
        X_left = [X[i] for i in left_idx]
        y_left = [y[i] for i in left_idx]
        X_right = [X[i] for i in right_idx]
        y_right = [y[i] for i in right_idx]
        node.left = self._build_node(X_left, y_left, depth + 1, feature_indices)
        node.right = self._build_node(X_right, y_right, depth + 1, feature_indices)
        return node

    def _random_best_split(self, X: List[List[float]], y: List[float], features: List[int]) -> Optional[Tuple[int, float, List[int], List[int]]]:
        n = len(y)
        best_feat = -1
        best_thr = 0.0
        best_score = float("inf")
        best_left: List[int] = []
        best_right: List[int] = []
        total_sse = _sse(y)
        for j in features:
            xs = [float(row[j]) for row in X]
            mn = min(xs); mx = max(xs)
            if mn == mx:
                continue
            for _ in range(self.n_thresholds):
                thr = mn + (mx - mn) * self._rng.random()
                left_idx = []
                right_idx = []
                yL = []
                yR = []
                for i, row in enumerate(X):
                    if float(row[j]) <= thr:
                        left_idx.append(i); yL.append(float(y[i]))
                    else:
                        right_idx.append(i); yR.append(float(y[i]))
                if len(left_idx) < self.min_samples_split or len(right_idx) < self.min_samples_split:
                    continue
                sse = _sse(yL) + _sse(yR)
                if sse + 1e-12 < best_score:
                    best_score = sse
                    best_feat = j
                    best_thr = thr
                    best_left = left_idx
                    best_right = right_idx
        if best_feat == -1 or best_score >= total_sse - 1e-12:
            return None
        return best_feat, best_thr, best_left, best_right

    def _serialize_node(self, node: Optional[_TreeNode]) -> Optional[Dict]:
        if node is None:
            return None
        return {
            "feature": node.feature,
            "threshold": node.threshold,
            "value": node.value,
            "n": node.n,
            "left": self._serialize_node(node.left),
            "right": self._serialize_node(node.right),
        }

    def _deserialize_node(self, obj: Optional[Dict]) -> Optional[_TreeNode]:
        if obj is None:
            return None
        n = _TreeNode()
        n.feature = obj.get("feature")
        n.threshold = obj.get("threshold")
        n.value = float(obj.get("value", 0.0))
        n.n = int(obj.get("n", 0))
        n.left = self._deserialize_node(obj.get("left"))
        n.right = self._deserialize_node(obj.get("right"))
        return n


class _ExtraTrees(BaseModel):
    def __init__(self, n_estimators: int = 100, max_depth: int = 4, min_samples_split: int = 8, max_features: Optional[object] = "sqrt", n_thresholds: int = 16, random_state: int = 42):
        self.n_estimators = int(n_estimators)
        self.max_depth = int(max_depth)
        self.min_samples_split = int(min_samples_split)
        self.max_features = max_features
        self.n_thresholds = int(n_thresholds)
        self.random_state = int(random_state)
        self.trees: List[_ExtraTree] = []
        self._rng = _random.Random(self.random_state)

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        self.trees = []
        if not X or not y or len(X) != len(y):
            return
        n = len(y)
        for m in range(self.n_estimators):
            # no bootstrap by default; shuffle indices and take all
            idx = list(range(n))
            self._rng.shuffle(idx)
            Xs = [X[i] for i in idx]
            ys = [y[i] for i in idx]
            t = _ExtraTree(max_depth=self.max_depth, min_samples_split=self.min_samples_split, max_features=self.max_features, n_thresholds=self.n_thresholds, random_state=self._rng.randrange(0, 1_000_000))
            t.fit(Xs, ys)
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
            "max_features": self.max_features,
            "n_thresholds": self.n_thresholds,
            "random_state": self.random_state,
            "trees": [t.get_params() for t in self.trees],
        }

    def set_params(self, params: Dict) -> None:
        self.n_estimators = int(params.get("n_estimators", self.n_estimators))
        self.max_depth = int(params.get("max_depth", self.max_depth))
        self.min_samples_split = int(params.get("min_samples_split", self.min_samples_split))
        self.max_features = params.get("max_features", self.max_features)
        self.n_thresholds = int(params.get("n_thresholds", self.n_thresholds))
        self.random_state = int(params.get("random_state", self.random_state))
        self._rng = _random.Random(self.random_state)
        self.trees = []
        for tp in params.get("trees", []) or []:
            t = _ExtraTree()
            t.set_params(tp)
            self.trees.append(t)


def create(params: Dict) -> BaseModel:
    p = SPEC.get("params_schema", {})
    return _ExtraTrees(
        n_estimators=int(params.get("n_estimators", p.get("n_estimators", {}).get("default", 100))),
        max_depth=int(params.get("max_depth", p.get("max_depth", {}).get("default", 4))),
        min_samples_split=int(params.get("min_samples_split", p.get("min_samples_split", {}).get("default", 8))),
        max_features=params.get("max_features", p.get("max_features", {}).get("default", "sqrt")),
        n_thresholds=int(params.get("n_thresholds", p.get("n_thresholds", {}).get("default", 16))),
        random_state=int(params.get("random_state", p.get("random_state", {}).get("default", 42))),
    )

