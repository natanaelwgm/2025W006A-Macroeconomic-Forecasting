from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "ElasticNet"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "alpha": {"type": "float", "default": 1.0, "min": 0.0},
        "l1_ratio": {"type": "float", "default": 0.5, "min": 0.0, "max": 1.0},
        "max_iter": {"type": "int", "default": 200, "min": 1},
        "tol": {"type": "float", "default": 1e-6, "min": 0.0},
    },
}


def _soft_threshold(x: float, lam: float) -> float:
    if x > lam:
        return x - lam
    elif x < -lam:
        return x + lam
    return 0.0


class _ElasticNet(BaseModel):
    """
    Elastic Net via coordinate descent with unpenalized intercept.
    Objective (informal): 0.5 * ||y - (b0 + X b)||^2 + lambda1 * ||b||_1 + 0.5 * lambda2 * ||b||_2^2
    where lambda1 = alpha * l1_ratio, lambda2 = alpha * (1 - l1_ratio)
    """

    def __init__(self, alpha: float = 1.0, l1_ratio: float = 0.5, max_iter: int = 200, tol: float = 1e-6):
        self.alpha = float(alpha)
        self.l1_ratio = float(l1_ratio)
        self.max_iter = int(max_iter)
        self.tol = float(tol)
        self.coef: List[float] = []  # includes intercept at index 0

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        n = len(y)
        if not X or n == 0 or len(X) != n:
            self.coef = [0.0]
            return
        p = len(X[0])

        lambda1 = self.alpha * self.l1_ratio
        lambda2 = self.alpha * (1.0 - self.l1_ratio)

        # Precompute column norms S_j = sum_i X_{ij}^2
        Sj = [0.0] * p
        for j in range(p):
            s = 0.0
            for i in range(n):
                s += float(X[i][j]) ** 2
            Sj[j] = s

        # Initialize
        b0 = sum(float(v) for v in y) / n
        b = [0.0] * p
        y_hat = [b0 for _ in range(n)]

        for _ in range(self.max_iter):
            max_change = 0.0
            for j in range(p):
                if Sj[j] == 0.0:
                    if b[j] != 0.0:
                        b[j] = 0.0
                    continue
                # Partial residual including current feature
                rho = 0.0
                for i in range(n):
                    xij = float(X[i][j])
                    r_i = float(y[i]) - (y_hat[i] - b[j] * xij)
                    rho += xij * r_i
                denom = Sj[j] + lambda2
                new_bj = _soft_threshold(rho, lambda1) / denom
                delta = new_bj - b[j]
                if delta != 0.0:
                    for i in range(n):
                        y_hat[i] += delta * float(X[i][j])
                max_change = max(max_change, abs(delta))
                b[j] = new_bj

            # Update intercept
            xb_mean = sum((y_hat[i] - b0) for i in range(n)) / n
            new_b0 = sum(float(v) for v in y) / n - xb_mean
            delta0 = new_b0 - b0
            if delta0 != 0.0:
                for i in range(n):
                    y_hat[i] += delta0
            max_change = max(max_change, abs(delta0))
            b0 = new_b0

            if max_change < self.tol:
                break

        self.coef = [b0] + b[:]

    def predict_row(self, x_row: List[float]) -> float:
        if not self.coef:
            return 0.0
        b0 = self.coef[0]
        s = b0
        for j, v in enumerate(x_row or []):
            if j + 1 < len(self.coef):
                s += self.coef[j + 1] * float(v)
        return s

    def get_params(self) -> Dict:
        return {"alpha": self.alpha, "l1_ratio": self.l1_ratio, "coef": self.coef[:], "max_iter": self.max_iter, "tol": self.tol}

    def set_params(self, params: Dict) -> None:
        self.alpha = float(params.get("alpha", self.alpha))
        self.l1_ratio = float(params.get("l1_ratio", self.l1_ratio))
        self.max_iter = int(params.get("max_iter", self.max_iter))
        self.tol = float(params.get("tol", self.tol))
        self.coef = [float(v) for v in params.get("coef", [])]


def create(params: Dict) -> BaseModel:
    alpha = float(params.get("alpha", SPEC["params_schema"]["alpha"]["default"]))
    l1_ratio = float(params.get("l1_ratio", SPEC["params_schema"]["l1_ratio"]["default"]))
    max_iter = int(params.get("max_iter", SPEC["params_schema"]["max_iter"]["default"]))
    tol = float(params.get("tol", SPEC["params_schema"]["tol"]["default"]))
    return _ElasticNet(alpha=alpha, l1_ratio=l1_ratio, max_iter=max_iter, tol=tol)

