from __future__ import annotations

from typing import Dict, List, Tuple

from core.base import BaseModel


NAME = "StandardizedLinear"

SPEC = {
    "frequency": "any",
    # Uses whatever features are provided by the recipe
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
}


def _solve(A: List[List[float]], b: List[float]) -> List[float]:
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for k in range(n):
        pr = max(range(k, n), key=lambda r: abs(M[r][k]))
        if abs(M[pr][k]) < 1e-12:
            return [0.0] * n
        if pr != k:
            M[k], M[pr] = M[pr], M[k]
        piv = M[k][k]
        for j in range(k, n + 1):
            M[k][j] /= piv
        for i in range(k + 1, n):
            f = M[i][k]
            for j in range(k, n + 1):
                M[i][j] -= f * M[k][j]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))
    return x


class _StdLinear(BaseModel):
    """
    OLS with intercept on standardized features (zero mean, unit variance),
    then mapped back to original feature space.
    """

    def __init__(self):
        self.coef: List[float] = []  # coef[0] is intercept in original space
        self.mu: List[float] = []
        self.sig: List[float] = []

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.coef = [0.0]
            self.mu = []
            self.sig = []
            return
        n = len(X)
        p = len(X[0])
        # Compute means and stds
        mu = [0.0] * p
        sig = [0.0] * p
        for j in range(p):
            col = [float(X[i][j]) for i in range(n)]
            m = sum(col) / n
            v = sum((v - m) ** 2 for v in col) / n
            s = v ** 0.5 if v > 0 else 1.0
            mu[j] = m
            sig[j] = s
        # Z = standardized features; build design [1, Z]
        Z = [[(float(X[i][j]) - mu[j]) / sig[j] for j in range(p)] for i in range(n)]
        G = [[0.0 for _ in range(p + 1)] for _ in range(p + 1)]
        g = [0.0 for _ in range(p + 1)]
        for i in range(n):
            zi = Z[i]
            yi = float(y[i])
            # intercept index 0
            g[0] += yi
            G[0][0] += 1.0
            for a in range(1, p + 1):
                za = zi[a - 1]
                g[a] += za * yi
                G[a][0] += za
                G[0][a] += za
                for b in range(1, p + 1):
                    G[a][b] += za * zi[b - 1]
        b_z = _solve(G, g)  # [b0_z, beta_z...]
        # Map back to original space
        b0_z = b_z[0]
        betas_z = b_z[1:]
        betas = [betas_z[j] / sig[j] for j in range(p)]
        b0 = b0_z - sum(betas_z[j] * (mu[j] / sig[j]) for j in range(p))
        self.coef = [b0] + betas
        self.mu = mu
        self.sig = sig

    def predict_row(self, x_row: List[float]) -> float:
        if not self.coef:
            return 0.0
        s = self.coef[0]
        for j, v in enumerate(x_row or []):
            if j + 1 < len(self.coef):
                s += self.coef[j + 1] * float(v)
        return s

    def get_params(self) -> Dict:
        return {"coef": self.coef[:], "mu": self.mu[:], "sig": self.sig[:]}

    def set_params(self, params: Dict) -> None:
        self.coef = [float(v) for v in params.get("coef", [])]
        self.mu = [float(v) for v in params.get("mu", [])]
        self.sig = [float(v) for v in params.get("sig", [])]


def create(params: Dict) -> BaseModel:
    return _StdLinear()

