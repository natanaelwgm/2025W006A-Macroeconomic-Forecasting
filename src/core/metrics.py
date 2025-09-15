from __future__ import annotations

from typing import List, Dict
import math


def rmse_mae(actual: List[float], forecast: List[float]) -> Dict[str, float]:
    n = 0
    se = 0.0
    ae = 0.0
    for a, f in zip(actual, forecast):
        if a is None or f is None:
            continue
        e = a - f
        se += e * e
        ae += abs(e)
        n += 1
    if n == 0:
        return {"rmse": float("nan"), "mae": float("nan")}
    return {"rmse": math.sqrt(se / n), "mae": ae / n}

