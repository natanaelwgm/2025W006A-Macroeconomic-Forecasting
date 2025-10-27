from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "DFM2"

# Two-factor Dynamic Factor Model (principal components over exogenous block).
SPEC = {
    "frequency": "any",
    "input": {"target": {"lags": []}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {
        "target_cols": {"type": "int", "default": 1, "min": 0},
        "num_factors": {"type": "int", "default": 2, "min": 1},
        "standardize": {"type": "bool", "default": True}
    },
}


class _DFM2(BaseModel):
    def __init__(self, target_cols: int = 1, num_factors: int = 2, standardize: bool = True):
        self.target_cols = int(max(0, target_cols))
        self.num_factors = int(max(1, num_factors))
        self.standardize = bool(standardize)
        self.exog_means: List[float] = []
        self.exog_stds: List[float] = []
        self.factor_weights: List[List[float]] = []  # k x m
        self.coef: List[float] = []  # [intercept] + target_cols + k factors

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        if not X or not y or len(X) != len(y):
            self.coef = [0.0]
            self.exog_means = []
            self.exog_stds = []
            self.factor_weights = []
            return
        n = len(X)
        p = len(X[0])
        tcols = min(self.target_cols, p)
        T = [[float(v) for v in row[:tcols]] for row in X]
        E = [[float(v) for v in row[tcols:]] for row in X]
        m = len(E[0]) if E and E[0] else 0

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

            # Covariance matrix
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

            # Top-k eigenvectors via power iteration + deflation
            k = min(self.num_factors, m)
            ws: List[List[float]] = []
            Ck = [row[:] for row in C]
            for _ in range(k):
                w = _first_eigenvector(Ck)
                if not w:
                    break
                # eigenvalue approx
                lam = _rayleigh(Ck, w)
                # deflate: C = C - lam * w w^T
                for i in range(m):
                    for j in range(m):
                        Ck[i][j] -= lam * w[i] * w[j]
                ws.append(w)
            # Factor series matrix N x k
            F = [[0.0 for _ in range(len(ws))] for _ in range(n)]
            for i in range(n):
                zi = Z[i]
                for r, w in enumerate(ws):
                    F[i][r] = sum(zi[j] * w[j] for j in range(m))
            self.exog_means = means
            self.exog_stds = [sd if sd > 1e-12 else 1.0 for sd in stds]
            self.factor_weights = ws
        else:
            F = [[0.0] for _ in range(n)]
            self.exog_means = []
            self.exog_stds = []
            self.factor_weights = []

        # Design: intercept + T + F (all factors)
        k = len(self.factor_weights) if self.factor_weights else 1
        P = 1 + tcols + k
        Zm = [[1.0] + T[i] + F[i] for i in range(n)]

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
        self.coef = _solve(G, g)

    def predict_row(self, x_row: List[float]) -> float:
        tcols = min(self.target_cols, len(x_row) if x_row else 0)
        t_part = [float(v) for v in (x_row[:tcols] if x_row else [])]
        e_part = [float(v) for v in (x_row[tcols:] if x_row else [])]
        # compute factors
        factors: List[float] = []
        if self.factor_weights and e_part:
            m = min(len(e_part), len(self.exog_means), len(self.exog_stds))
            z = [(e_part[j] - self.exog_means[j]) / (self.exog_stds[j] if self.exog_stds[j] > 1e-12 else 1.0) for j in range(m)]
            for w in self.factor_weights:
                k = min(len(w), m)
                factors.append(sum(z[j] * w[j] for j in range(k)))
        else:
            factors = [0.0] * (len(self.factor_weights) if self.factor_weights else 1)
        z = [1.0] + t_part + factors
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
            "factor_weights": [w[:] for w in self.factor_weights],
        }

    def set_params(self, params: Dict) -> None:
        self.target_cols = int(params.get("target_cols", self.target_cols))
        self.num_factors = int(params.get("num_factors", self.num_factors))
        self.standardize = bool(params.get("standardize", self.standardize))
        self.coef = [float(v) for v in params.get("coef", [])]
        self.exog_means = [float(v) for v in params.get("exog_means", [])]
        self.exog_stds = [float(v) for v in params.get("exog_stds", [])]
        self.factor_weights = [[float(v) for v in row] for row in params.get("factor_weights", [])]


def _first_eigenvector(C: List[List[float]], max_iter: int = 200, tol: float = 1e-9) -> List[float]:
    m = len(C)
    if m == 0:
        return []
    v = [1.0 / (m ** 0.5) for _ in range(m)]
    for _ in range(max_iter):
        w = [0.0] * m
        for i in range(m):
            s = 0.0
            Ci = C[i]
            for j in range(m):
                s += Ci[j] * v[j]
            w[i] = s
        norm = sum(x * x for x in w) ** 0.5
        if norm <= 1e-15:
            return v
        v_new = [x / norm for x in w]
        diff = sum((v_new[i] - v[i]) ** 2 for i in range(m)) ** 0.5
        v = v_new
        if diff < tol:
            break
    return v


def _rayleigh(C: List[List[float]], v: List[float]) -> float:
    m = len(v)
    # lambda = (v^T C v) / (v^T v) with v normalized -> numerator only
    num = 0.0
    for i in range(m):
        s = 0.0
        Ci = C[i]
        for j in range(m):
            s += Ci[j] * v[j]
        num += v[i] * s
    den = sum(vi * vi for vi in v) or 1.0
    return num / den


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
    num_factors = int(params.get("num_factors", SPEC["params_schema"]["num_factors"]["default"]))
    standardize = bool(params.get("standardize", SPEC["params_schema"]["standardize"]["default"]))
    return _DFM2(target_cols=target_cols, num_factors=num_factors, standardize=standardize)

