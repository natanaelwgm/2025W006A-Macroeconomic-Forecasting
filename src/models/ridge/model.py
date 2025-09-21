from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "Ridge"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {"alpha": {"type": "float", "default": 1.0, "min": 0.0}},
}


class _Ridge(BaseModel):
    """
    Ridge regression with intercept (intercept not penalized).
    Solves (Z^T Z + A) b = Z^T y, where A = diag([0, alpha, ..., alpha]).
    """

    def __init__(self, alpha: float = 1.0):
        self.alpha = float(alpha)
        self.coef: List[float] = []

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.coef = [0.0]
            return
        n = len(X)
        p = len(X[0])
        Z = [[1.0] + [float(v) for v in row] for row in X]
        G = [[0.0 for _ in range(p + 1)] for _ in range(p + 1)]
        g = [0.0 for _ in range(p + 1)]
        for i in range(n):
            zi = Z[i]
            yi = float(y[i])
            for a in range(p + 1):
                g[a] += zi[a] * yi
                za = zi[a]
                for b in range(p + 1):
                    G[a][b] += za * zi[b]
        # Add ridge penalty to non-intercept diagonal
        for j in range(1, p + 1):
            G[j][j] += self.alpha
        b = _solve(G, g)
        self.coef = b

    def predict_row(self, x_row: List[float]) -> float:
        if not self.coef:
            return 0.0
        z = [1.0] + [float(v) for v in (x_row or [])]
        if len(z) < len(self.coef):
            z += [0.0] * (len(self.coef) - len(z))
        return sum(c * v for c, v in zip(self.coef, z))

    def get_params(self) -> Dict:
        return {"alpha": self.alpha, "coef": self.coef[:]}

    def set_params(self, params: Dict) -> None:
        self.alpha = float(params.get("alpha", self.alpha))
        self.coef = [float(v) for v in params.get("coef", [])]


def _solve(A: List[List[float]], b: List[float]) -> List[float]:
    n = len(A)
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
    alpha = float(params.get("alpha", SPEC.get("params_schema", {}).get("alpha", {}).get("default", 1.0)))
    return _Ridge(alpha=alpha)

