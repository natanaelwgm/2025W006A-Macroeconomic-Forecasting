from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union
import math
import random as _random

from core.base import BaseModel


NAME = "Tree"

SPEC = {
    "frequency": "any",
    # By default expect y_t as a feature; recipes can override features.
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "max_depth": {"type": "int", "default": 4, "min": 1},
        "min_samples_split": {"type": "int", "default": 8, "min": 2},
        "max_features": {"type": "str|int", "default": "sqrt"},
        "random_state": {"type": "int", "default": 42},
    },
}


class _TreeNode:
    __slots__ = ("feature", "threshold", "left", "right", "value", "n")

    def __init__(self):
        self.feature: Optional[int] = None
        self.threshold: Optional[float] = None
        self.left: Optional["_TreeNode"] = None
        self.right: Optional["_TreeNode"] = None
        self.value: float = 0.0
        self.n: int = 0


class _TreeRegressor(BaseModel):
    def __init__(self, max_depth: int = 4, min_samples_split: int = 8, max_features: Optional[Union[int, str]] = "sqrt", random_state: int = 42):
        self.max_depth = int(max_depth)
        self.min_samples_split = int(min_samples_split)
        self.max_features = max_features
        self.random_state = int(random_state)
        self.root: Optional[_TreeNode] = None
        self._rng = _random.Random(self.random_state)

    # --- Public API ---
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.root = None
            return
        # Build tree recursively
        n_features = len(X[0]) if X else 0
        self.root = self._build_node(X, y, depth=0, feature_indices=list(range(n_features)))

    def predict_row(self, x_row: List[float]) -> float:
        if self.root is None:
            return 0.0
        node = self.root
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
            "random_state": self.random_state,
            "tree": self._serialize_node(self.root),
        }

    def set_params(self, params: Dict) -> None:
        self.max_depth = int(params.get("max_depth", self.max_depth))
        self.min_samples_split = int(params.get("min_samples_split", self.min_samples_split))
        self.max_features = params.get("max_features", self.max_features)
        self.random_state = int(params.get("random_state", self.random_state))
        self._rng = _random.Random(self.random_state)
        self.root = self._deserialize_node(params.get("tree"))

    # --- Tree building helpers ---
    def _build_node(self, X: List[List[float]], y: List[float], depth: int, feature_indices: List[int]) -> _TreeNode:
        node = _TreeNode()
        node.n = len(y)
        node.value = _mean(y)
        if depth >= self.max_depth or len(y) < self.min_samples_split:
            return node

        # Select feature subset
        m = len(feature_indices)
        k = self._resolve_max_features(m)
        features = feature_indices[:]
        self._rng.shuffle(features)
        features = features[:k]

        best = self._best_split(X, y, features)
        if best is None:
            return node
        feat, thr, left_idx, right_idx = best
        if len(left_idx) == 0 or len(right_idx) == 0:
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

    def _resolve_max_features(self, m: int) -> int:
        mf = self.max_features
        if mf is None:
            return m
        if isinstance(mf, int):
            return max(1, min(m, mf))
        s = str(mf).lower()
        if s == "sqrt":
            return max(1, int(math.sqrt(m)))
        if s in ("log2", "log"):
            return max(1, int(math.log2(m)))
        return m

    def _best_split(self, X: List[List[float]], y: List[float], features: List[int]) -> Optional[Tuple[int, float, List[int], List[int]]]:
        n = len(y)
        if n < 2 * self.min_samples_split:
            return None
        best_feat = -1
        best_thr = 0.0
        best_score = float("inf")
        best_left_idx: List[int] = []
        best_right_idx: List[int] = []

        # Precompute total SSE to ensure the split improves
        total_sse = _sse(y)

        for j in features:
            pairs = sorted(((float(row[j]), float(y[i])), i) for i, row in enumerate(X))
            x_sorted = [p[0][0] for p in pairs]
            y_sorted = [p[0][1] for p in pairs]
            idx_sorted = [p[1] for p in pairs]
            # Skip if all x are equal
            if x_sorted[0] == x_sorted[-1]:
                continue
            # Prefix sums
            ps = [0.0]
            pss = [0.0]
            for v in y_sorted:
                ps.append(ps[-1] + v)
                pss.append(pss[-1] + v * v)
            # Try splits between distinct x values
            for k in range(self.min_samples_split, n - self.min_samples_split + 1):
                if x_sorted[k - 1] == x_sorted[k]:
                    continue
                nL = k
                nR = n - k
                sumL = ps[k]
                ssL = pss[k]
                sumR = ps[n] - ps[k]
                ssR = pss[n] - pss[k]
                sseL = ssL - (sumL * sumL) / nL
                sseR = ssR - (sumR * sumR) / nR
                score = sseL + sseR
                if score + 1e-12 < best_score:
                    best_score = score
                    best_feat = j
                    best_thr = 0.5 * (x_sorted[k - 1] + x_sorted[k])
                    left_idx = idx_sorted[:k]
                    right_idx = idx_sorted[k:]
                    best_left_idx = left_idx
                    best_right_idx = right_idx
        # Require improvement
        if best_feat == -1 or best_score >= total_sse - 1e-12:
            return None
        return best_feat, best_thr, best_left_idx, best_right_idx

    # --- Serialization helpers ---
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


def _mean(arr: List[float]) -> float:
    return sum(arr) / len(arr) if arr else 0.0


def _sse(arr: List[float]) -> float:
    if not arr:
        return 0.0
    m = _mean(arr)
    return sum((v - m) * (v - m) for v in arr)


def create(params: Dict) -> BaseModel:
    p = SPEC.get("params_schema", {})
    return _TreeRegressor(
        max_depth=int(params.get("max_depth", p.get("max_depth", {}).get("default", 4))),
        min_samples_split=int(params.get("min_samples_split", p.get("min_samples_split", {}).get("default", 8))),
        max_features=params.get("max_features", p.get("max_features", {}).get("default", "sqrt")),
        random_state=int(params.get("random_state", p.get("random_state", {}).get("default", 42))),
    )
