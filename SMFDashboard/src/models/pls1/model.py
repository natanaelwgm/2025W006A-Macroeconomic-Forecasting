from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "PLS1"

# Partial Least Squares with a single component over exogenous features.
# Uses a simple single-step NIPALS-like approach: weight vector w ∝ Z^T y (with Z standardized exog, y centered),
# normalized to unit length. Factor t = Z w, then y ~ intercept + target_cols + t.
SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": []}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "target_cols": {"type": "int", "default": 1, "min": 0},
        "standardize": {"type": "bool", "default": True}
    }
}


class _PLS1(BaseModel):
    def __init__(self, target_cols: int = 1, standardize: bool = True):
        self.target_cols = int(max(0, target_cols))
        self.standardize = bool(standardize)
        self.exog_means: List[float] = []
        self.exog_stds: List[float] = []
        self.weight: List[float] = []  # weights over exog columns
        self.y_mean: float = 0.0
        self.coef: List[float] = []  # [intercept] + target_cols + [t]

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.coef = [0.0]
            self.weight = []
            self.exog_means = []
            self.exog_stds = []
            self.y_mean = 0.0
            return
        n = len(X)
        p = len(X[0]) if X[0] else 0
        tcols = min(self.target_cols, p)
        T = [[float(v) for v in row[:tcols]] for row in X]
        E = [[float(v) for v in row[tcols:]] for row in X]
        m = len(E[0]) if E and E[0] else 0

        # Center y
        y_mean = sum(float(v) for v in y) / n
        yc = [float(v) - y_mean for v in y]

        if m > 0:
            means = [0.0] * m
            for row in E:
                for j in range(m):
                    means[j] += row[j]
            means = [v / n for v in means]
            stds = [0.0] * m
            for row in E:
                for j in range(m):
                    d = row[j] - means[j]
                    stds[j] += d * d
            stds = [(s / n) ** 0.5 for s in stds]
            # Z standardization
            Z = []
            if self.standardize:
                for row in E:
                    zr = []
                    for j in range(m):
                        sd = stds[j]
                        zr.append(0.0 if sd <= 1e-12 else (row[j] - means[j]) / sd)
                    Z.append(zr)
            else:
                for row in E:
                    Z.append([row[j] - means[j] for j in range(m)])
            # w ∝ Z^T y_c
            w = [0.0] * m
            for i in range(n):
                zi = Z[i]
                yi = yc[i]
                for j in range(m):
                    w[j] += zi[j] * yi
            # normalize weights
            norm = sum(v * v for v in w) ** 0.5
            if norm <= 1e-15:
                w = [0.0] * m
            else:
                w = [v / norm for v in w]
            # t = Z w
            t_score = [sum(Z[i][j] * w[j] for j in range(m)) for i in range(n)]
            self.exog_means = means
            self.exog_stds = [sd if sd > 1e-12 else 1.0 for sd in stds]
            self.weight = w
        else:
            t_score = [0.0 for _ in range(n)]
            self.exog_means = []
            self.exog_stds = []
            self.weight = []

        # Design matrix: intercept + T + t
        P = 1 + tcols + 1
        Zm = [[1.0] + T[i] + [t_score[i]] for i in range(n)]
        G = [[0.0 for _ in range(P)] for _ in range(P)]
        g = [0.0 for _ in range(P)]
        for i in range(n):
            zi = Zm[i]
            yi = float(y[i])
            for a in range(P):
                g[a] += zi[a] * yi
                za = zi[a]
                for b in range(P):
                    G[a][b] += za * zi[b]
        b = _solve(G, g)
        self.coef = b
        self.y_mean = y_mean

    def predict_row(self, x_row: List[float]) -> float:
        tcols = min(self.target_cols, len(x_row) if x_row else 0)
        t_part = [float(v) for v in (x_row[:tcols] if x_row else [])]
        e_part = [float(v) for v in (x_row[tcols:] if x_row else [])]
        if self.weight and e_part:
            m = min(len(e_part), len(self.exog_means), len(self.exog_stds), len(self.weight))
            z = [(e_part[j] - self.exog_means[j]) / (self.exog_stds[j] if self.exog_stds[j] > 1e-12 else 1.0) for j in range(m)]
            t = sum(z[j] * self.weight[j] for j in range(m))
        else:
            t = 0.0
        z = [1.0] + t_part + [t]
        if len(z) < len(self.coef):
            z += [0.0] * (len(self.coef) - len(z))
        return sum(c * v for c, v in zip(self.coef, z)) if self.coef else 0.0

    def get_params(self) -> Dict:
        return {
            "target_cols": self.target_cols,
            "standardize": self.standardize,
            "coef": self.coef[:],
            "exog_means": self.exog_means[:],
            "exog_stds": self.exog_stds[:],
            "weight": self.weight[:],
            "y_mean": self.y_mean,
        }

    def set_params(self, params: Dict) -> None:
        self.target_cols = int(params.get("target_cols", self.target_cols))
        self.standardize = bool(params.get("standardize", self.standardize))
        self.coef = [float(v) for v in params.get("coef", [])]
        self.exog_means = [float(v) for v in params.get("exog_means", [])]
        self.exog_stds = [float(v) for v in params.get("exog_stds", [])]
        self.weight = [float(v) for v in params.get("weight", [])]
        self.y_mean = float(params.get("y_mean", 0.0))


def _solve(A: List[List[float]], b: List[float]) -> List[float]:
    n = len(A)
    if n == 0:
        return []
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for k in range(n):
        pivot_row = max(range(k, n), key=lambda r: abs(M[r][k]))
        if abs(M[pivot_row][k]) < 1e-12:
            return [0.0] * n
        if pivot_row != k:
            M[k], M[pivot_row] = M[pivot_row], M[k]
        pivot = M[k][k]
        for j in range(k, n + 1):
            M[k][j] /= pivot
        for i in range(k + 1, n):
            factor = M[i][k]
            for j in range(k, n + 1):
                M[i][j] -= factor * M[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
    return x


def create(params: Dict) -> BaseModel:
    target_cols = int(params.get("target_cols", SPEC["params_schema"]["target_cols"]["default"]))
    standardize = bool(params.get("standardize", SPEC["params_schema"]["standardize"]["default"]))
    return _PLS1(target_cols=target_cols, standardize=standardize)

