from __future__ import annotations

from typing import Dict, List, Tuple

from core.base import BaseModel


NAME = "ElasticNetGrid"

SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": [0]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "alpha_grid": {"type": "list", "default": [0.1, 0.5, 1.0, 2.0, 5.0]},
        "l1_ratio_grid": {"type": "list", "default": [0.2, 0.5, 0.8]},
        "val_frac": {"type": "float", "default": 0.2, "min": 0.05, "max": 0.5},
        "max_iter": {"type": "int", "default": 300, "min": 1},
        "tol": {"type": "float", "default": 1e-6, "min": 0.0},
    },
}


def _soft_threshold(x: float, lam: float) -> float:
    if x > lam:
        return x - lam
    elif x < -lam:
        return x + lam
    return 0.0


class _ENetSolver:
    def __init__(self, alpha: float, l1_ratio: float, max_iter: int, tol: float):
        self.alpha = float(alpha)
        self.l1_ratio = float(l1_ratio)
        self.max_iter = int(max_iter)
        self.tol = float(tol)
        self.coef: List[float] = []  # [b0, b1..bp]

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        n = len(y)
        if not X or n == 0 or len(X) != n:
            self.coef = [0.0]
            return
        p = len(X[0])
        lambda1 = self.alpha * self.l1_ratio
        lambda2 = self.alpha * (1.0 - self.l1_ratio)
        # Precompute column norms
        Sj = [0.0] * p
        for j in range(p):
            Sj[j] = sum(float(X[i][j]) ** 2 for i in range(n))
        # initialize
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
            # intercept
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
        self.coef = [b0] + b

    def predict_row(self, x_row: List[float]) -> float:
        if not self.coef:
            return 0.0
        s = self.coef[0]
        for j, v in enumerate(x_row or []):
            if j + 1 < len(self.coef):
                s += self.coef[j + 1] * float(v)
        return s


class _ElasticNetGrid(BaseModel):
    def __init__(self, alpha_grid: List[float], l1_ratio_grid: List[float], val_frac: float, max_iter: int, tol: float):
        self.alpha_grid = [float(a) for a in alpha_grid]
        self.l1_ratio_grid = [float(r) for r in l1_ratio_grid]
        self.val_frac = float(val_frac)
        self.max_iter = int(max_iter)
        self.tol = float(tol)
        self.best_params: Dict[str, float] = {}
        self.best_coef: List[float] = []

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.best_coef = [0.0]
            self.best_params = {}
            return
        n = len(X)
        n_val = max(1, int(self.val_frac * n))
        n_tr = max(1, n - n_val)
        X_tr, y_tr = X[:n_tr], y[:n_tr]
        X_val, y_val = X[n_tr:], y[n_tr:]

        def mse(y_true: List[float], y_pred: List[float]) -> float:
            m = len(y_true)
            if m == 0:
                return float("inf")
            se = 0.0
            for a, b in zip(y_true, y_pred):
                e = float(a) - float(b)
                se += e * e
            return se / m

        best = (float("inf"), None, None, None)  # (mse, alpha, l1_ratio, solver)
        for a in self.alpha_grid:
            for r in self.l1_ratio_grid:
                solver = _ENetSolver(alpha=a, l1_ratio=r, max_iter=self.max_iter, tol=self.tol)
                solver.fit(X_tr, y_tr)
                preds = [solver.predict_row(x) for x in X_val]
                score = mse(y_val, preds)
                if score < best[0]:
                    best = (score, a, r, solver)
        _, a_best, r_best, solver_best = best
        if solver_best is None:
            # fallback single fit
            solver_best = _ENetSolver(alpha=self.alpha_grid[0], l1_ratio=self.l1_ratio_grid[0], max_iter=self.max_iter, tol=self.tol)
            solver_best.fit(X, y)
        self.best_params = {"alpha": a_best, "l1_ratio": r_best}
        self.best_coef = solver_best.coef[:]

    def predict_row(self, x_row: List[float]) -> float:
        if not self.best_coef:
            return 0.0
        s = self.best_coef[0]
        for j, v in enumerate(x_row or []):
            if j + 1 < len(self.best_coef):
                s += self.best_coef[j + 1] * float(v)
        return s

    def get_params(self) -> Dict:
        return {"best_params": self.best_params, "coef": self.best_coef[:], "alpha_grid": self.alpha_grid, "l1_ratio_grid": self.l1_ratio_grid, "val_frac": self.val_frac, "max_iter": self.max_iter, "tol": self.tol}

    def set_params(self, params: Dict) -> None:
        self.best_params = params.get("best_params", {})
        self.best_coef = [float(v) for v in params.get("coef", [])]
        self.alpha_grid = [float(v) for v in params.get("alpha_grid", self.alpha_grid)]
        self.l1_ratio_grid = [float(v) for v in params.get("l1_ratio_grid", self.l1_ratio_grid)]
        self.val_frac = float(params.get("val_frac", self.val_frac))
        self.max_iter = int(params.get("max_iter", self.max_iter))
        self.tol = float(params.get("tol", self.tol))


def create(params: Dict) -> BaseModel:
    ag = params.get("alpha_grid", SPEC["params_schema"]["alpha_grid"]["default"])
    rg = params.get("l1_ratio_grid", SPEC["params_schema"]["l1_ratio_grid"]["default"])
    val_frac = float(params.get("val_frac", SPEC["params_schema"]["val_frac"]["default"]))
    max_iter = int(params.get("max_iter", SPEC["params_schema"]["max_iter"]["default"]))
    tol = float(params.get("tol", SPEC["params_schema"]["tol"]["default"]))
    return _ElasticNetGrid(alpha_grid=ag, l1_ratio_grid=rg, val_frac=val_frac, max_iter=max_iter, tol=tol)

