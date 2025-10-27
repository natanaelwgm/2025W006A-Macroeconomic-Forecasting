from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "DFM"

# Simplified Dynamic Factor Model plugin.
# - Computes a single latent factor as the first principal component of the exogenous
#   feature block (columns after the first `target_cols`), using standardized inputs.
# - Regresses y on [intercept, target_lag_cols, factor].
# - Horizon handling is done by the engine (direct strategy); this model uses
#   contemporaneous factor only (no factor lags) to remain stateless.
SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": []}, "exog": {}},  # recipe should specify features
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "target_cols": {"type": "int", "default": 0, "min": 0},
        "num_factors": {"type": "int", "default": 1, "min": 1},
        "standardize": {"type": "bool", "default": True},
    },
}


class _DFM(BaseModel):
    def __init__(self, target_cols: int = 0, num_factors: int = 1, standardize: bool = True):
        # Model hyperparameters
        self.target_cols = int(max(0, target_cols))
        self.num_factors = int(max(1, num_factors))  # implementation supports 1
        self.standardize = bool(standardize)

        # Learned params
        self.exog_means: List[float] = []
        self.exog_stds: List[float] = []
        self.factor_weights: List[float] = []  # first PC weights over exog columns
        self.coef: List[float] = []  # OLS coefficients: [intercept] + target_cols + [factor]

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.coef = [0.0]
            self.exog_means = []
            self.exog_stds = []
            self.factor_weights = []
            return

        n = len(X)
        p = len(X[0]) if X[0] else 0

        tcols = min(self.target_cols, p)
        # Split features
        # Target-lag block: first tcols columns
        T = [[float(v) for v in row[:tcols]] for row in X]
        # Exogenous block: remaining columns
        E = [[float(v) for v in row[tcols:]] for row in X]
        m = len(E[0]) if E and E[0] else 0

        # Prepare factor
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
            # Use population variance normalization for stability (divide by n)
            stds = [(s / n) ** 0.5 for s in stds]
            # Build standardized matrix Z
            Z = []
            if self.standardize:
                for row in E:
                    zr = []
                    for j in range(m):
                        sd = stds[j]
                        if sd <= 1e-12:
                            zr.append(0.0)
                        else:
                            zr.append((row[j] - means[j]) / sd)
                    Z.append(zr)
            else:
                # Center only
                for row in E:
                    zr = [row[j] - means[j] for j in range(m)]
                    Z.append(zr)

            # Compute covariance matrix C = Z^T Z / (n - 1) (or /n if n==1)
            C = [[0.0 for _ in range(m)] for _ in range(m)]
            denom = float(n - 1 if n > 1 else 1)
            for i in range(n):
                zi = Z[i]
                for a in range(m):
                    za = zi[a]
                    for b in range(m):
                        C[a][b] += za * zi[b]
            for a in range(m):
                for b in range(m):
                    C[a][b] /= denom

            # First principal component via power iteration
            w = _first_eigenvector(C)
            # Compute factor score f_t = Z_t . w
            f_series = [sum(zi[j] * w[j] for j in range(m)) for zi in Z]

            self.exog_means = means
            # store stds regardless of standardize flag for predict normalization
            self.exog_stds = [sd if sd > 1e-12 else 1.0 for sd in stds]
            self.factor_weights = w
        else:
            f_series = [0.0 for _ in range(n)]
            self.exog_means = []
            self.exog_stds = []
            self.factor_weights = []

        # Build design matrix: intercept + T + factor
        P = tcols + 1  # +1 for factor
        Zm = [[1.0] + T[i] + [f_series[i]] for i in range(n)]

        # Normal equations
        G = [[0.0 for _ in range(P + 1)] for _ in range(P + 1)]
        g = [0.0 for _ in range(P + 1)]
        for i in range(n):
            zi = Zm[i]
            yi = float(y[i])
            for a in range(P + 1):
                g[a] += zi[a] * yi
                za = zi[a]
                for b in range(P + 1):
                    G[a][b] += za * zi[b]

        b = _solve(G, g)
        self.coef = b

    def predict_row(self, x_row: List[float]) -> float:
        tcols = min(self.target_cols, len(x_row) if x_row else 0)
        t_part = [float(v) for v in (x_row[:tcols] if x_row else [])]

        # Factor from exog part
        e_part = [float(v) for v in (x_row[tcols:] if x_row else [])]
        if self.factor_weights and e_part:
            # standardize using stored means/stds
            m = min(len(self.factor_weights), len(e_part), len(self.exog_means), len(self.exog_stds))
            f = 0.0
            for j in range(m):
                z = (e_part[j] - self.exog_means[j]) / (self.exog_stds[j] if self.exog_stds[j] > 1e-12 else 1.0)
                f += z * self.factor_weights[j]
        else:
            f = 0.0

        z = [1.0] + t_part + [f]
        # Pad if needed
        if len(z) < len(self.coef):
            z += [0.0] * (len(self.coef) - len(z))
        return sum(c * v for c, v in zip(self.coef, z)) if self.coef else 0.0

    def get_params(self) -> Dict:
        return {
            "target_cols": self.target_cols,
            "num_factors": self.num_factors,
            "standardize": self.standardize,
            "coef": self.coef[:],
            "exog_means": self.exog_means[:],
            "exog_stds": self.exog_stds[:],
            "factor_weights": self.factor_weights[:],
        }

    def set_params(self, params: Dict) -> None:
        self.target_cols = int(params.get("target_cols", self.target_cols))
        self.num_factors = int(params.get("num_factors", self.num_factors))
        self.standardize = bool(params.get("standardize", self.standardize))
        self.coef = [float(v) for v in params.get("coef", [])]
        self.exog_means = [float(v) for v in params.get("exog_means", [])]
        self.exog_stds = [float(v) for v in params.get("exog_stds", [])]
        self.factor_weights = [float(v) for v in params.get("factor_weights", [])]


def _first_eigenvector(C: List[List[float]], max_iter: int = 200, tol: float = 1e-9) -> List[float]:
    m = len(C)
    if m == 0:
        return []
    # Initialize with equal weights
    v = [1.0 / (m ** 0.5) for _ in range(m)]
    for _ in range(max_iter):
        # w = C @ v
        w = [0.0] * m
        for i in range(m):
            s = 0.0
            Ci = C[i]
            for j in range(m):
                s += Ci[j] * v[j]
            w[i] = s
        # normalize
        norm = sum(x * x for x in w) ** 0.5
        if norm <= 1e-15:
            return v
        v_new = [x / norm for x in w]
        # check convergence
        diff = sum((v_new[i] - v[i]) ** 2 for i in range(m)) ** 0.5
        v = v_new
        if diff < tol:
            break
    return v


def _solve(A: List[List[float]], b: List[float]) -> List[float]:
    n = len(A)
    if n == 0:
        return []
    # Augmented matrix
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for k in range(n):
        # Partial pivoting
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
    target_cols = int(params.get("target_cols", SPEC.get("params_schema", {}).get("target_cols", {}).get("default", 0)))
    num_factors = int(params.get("num_factors", SPEC.get("params_schema", {}).get("num_factors", {}).get("default", 1)))
    standardize = bool(params.get("standardize", SPEC.get("params_schema", {}).get("standardize", {}).get("default", True)))
    # Current implementation supports a single factor; num_factors>1 is treated as 1
    return _DFM(target_cols=target_cols, num_factors=num_factors, standardize=standardize)

