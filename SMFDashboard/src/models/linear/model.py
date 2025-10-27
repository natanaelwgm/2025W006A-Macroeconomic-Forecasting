from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "Linear"

SPEC = {
    "frequency": "any",
    # Linear model uses whatever features are provided by the recipe.
    # If none provided, recipe must specify at least one feature.
    "input": {"target": {"lags": []}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
}


class _OLS(BaseModel):
    """
    Multiple linear regression with intercept using normal equations.
    Implements a tiny solver for (X^T X) b = X^T y with basic Gaussian elimination.
    """

    def __init__(self):
        self.coef: List[float] = []  # includes intercept as coef[0]

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.coef = [0.0]
            return
        n = len(X)
        p = len(X[0])
        # Build design matrix with intercept: Z = [1, X]
        Z = [[1.0] + [float(v) for v in row] for row in X]
        # Compute G = Z^T Z and g = Z^T y
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
        # Solve G b = g via Gaussian elimination with partial pivoting
        b = _solve_linear_system(G, g)
        self.coef = b

    def predict_row(self, x_row: List[float]) -> float:
        if not self.coef:
            return 0.0
        z = [1.0] + [float(v) for v in (x_row or [])]
        # pad if fewer features than trained (unlikely in correct use)
        if len(z) < len(self.coef):
            z += [0.0] * (len(self.coef) - len(z))
        return sum(c * v for c, v in zip(self.coef, z))

    def get_params(self) -> Dict:
        return {"coef": self.coef[:]}  # copy

    def set_params(self, params: Dict) -> None:
        self.coef = [float(v) for v in params.get("coef", [])]


def _solve_linear_system(A: List[List[float]], b: List[float]) -> List[float]:
    # Augment matrix
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    # Forward elimination with partial pivoting
    for k in range(n):
        # pivot
        pivot_row = max(range(k, n), key=lambda r: abs(M[r][k]))
        if abs(M[pivot_row][k]) < 1e-12:
            # Singular; return zeros
            return [0.0] * n
        if pivot_row != k:
            M[k], M[pivot_row] = M[pivot_row], M[k]
        # normalize row k
        pivot = M[k][k]
        for j in range(k, n + 1):
            M[k][j] /= pivot
        # eliminate below
        for i in range(k + 1, n):
            factor = M[i][k]
            for j in range(k, n + 1):
                M[i][j] -= factor * M[k][j]
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
    return x


def create(params: Dict) -> BaseModel:
    return _OLS()
