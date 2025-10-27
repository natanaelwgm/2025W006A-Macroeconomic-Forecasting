from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "Huber"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "delta": {"type": "float", "default": 1.0, "min": 1e-6},
        "max_iter": {"type": "int", "default": 100, "min": 1},
        "tol": {"type": "float", "default": 1e-6, "min": 0.0},
    },
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


class _Huber(BaseModel):
    """
    Robust regression with Huber loss via IRLS (intercept included, not penalized).
    Weights: w_i = 1 if |r_i| <= delta else delta/|r_i|.
    """

    def __init__(self, delta: float = 1.0, max_iter: int = 100, tol: float = 1e-6):
        self.delta = float(delta)
        self.max_iter = int(max_iter)
        self.tol = float(tol)
        self.coef: List[float] = []  # coef[0]=intercept

    def _wls(self, X: List[List[float]], y: List[float], w: List[float]) -> List[float]:
        n = len(y)
        p = len(X[0]) if X else 0
        # design with intercept
        G = [[0.0 for _ in range(p + 1)] for _ in range(p + 1)]
        g = [0.0 for _ in range(p + 1)]
        for i in range(n):
            wi = float(w[i])
            zi0 = 1.0
            yi = float(y[i])
            g[0] += wi * zi0 * yi
            G[0][0] += wi * zi0 * zi0
            for a in range(1, p + 1):
                za = float(X[i][a - 1])
                g[a] += wi * za * yi
                G[a][0] += wi * za * zi0
                G[0][a] += wi * za * zi0
                for b in range(1, p + 1):
                    G[a][b] += wi * za * float(X[i][b - 1])
        return _solve(G, g)  # [b0, betas]

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.coef = [0.0]
            return
        n = len(y)
        p = len(X[0])
        # initialize with OLS
        w = [1.0] * n
        b = self._wls(X, y, w)
        y_hat = [b[0] + sum(b[j + 1] * float(X[i][j]) for j in range(p)) for i in range(n)]
        for _ in range(self.max_iter):
            # compute residuals and weights
            max_change = 0.0
            r = [float(y[i]) - y_hat[i] for i in range(n)]
            for i in range(n):
                ri = abs(r[i])
                w[i] = 1.0 if ri <= self.delta else (self.delta / (ri + 1e-12))
            b_new = self._wls(X, y, w)
            y_hat_new = [b_new[0] + sum(b_new[j + 1] * float(X[i][j]) for j in range(p)) for i in range(n)]
            max_change = max(max_change, max(abs(b_new[j] - b[j]) for j in range(len(b))))
            b = b_new
            y_hat = y_hat_new
            if max_change < self.tol:
                break
        self.coef = b

    def predict_row(self, x_row: List[float]) -> float:
        if not self.coef:
            return 0.0
        s = self.coef[0]
        for j, v in enumerate(x_row or []):
            if j + 1 < len(self.coef):
                s += self.coef[j + 1] * float(v)
        return s

    def get_params(self) -> Dict:
        return {"delta": self.delta, "coef": self.coef[:], "max_iter": self.max_iter, "tol": self.tol}

    def set_params(self, params: Dict) -> None:
        self.delta = float(params.get("delta", self.delta))
        self.max_iter = int(params.get("max_iter", self.max_iter))
        self.tol = float(params.get("tol", self.tol))
        self.coef = [float(v) for v in params.get("coef", [])]


def create(params: Dict) -> BaseModel:
    delta = float(params.get("delta", SPEC["params_schema"]["delta"]["default"]))
    max_iter = int(params.get("max_iter", SPEC["params_schema"]["max_iter"]["default"]))
    tol = float(params.get("tol", SPEC["params_schema"]["tol"]["default"]))
    return _Huber(delta=delta, max_iter=max_iter, tol=tol)

