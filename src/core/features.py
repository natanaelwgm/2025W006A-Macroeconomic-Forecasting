from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import math

from .data import TimeSeriesFrame


def build_lagged_columns(frame: TimeSeriesFrame, spec: Dict[str, List[int]]) -> Dict[str, List[float | None]]:
    """
    Build lagged series for a dict spec: { col_name: [lags...] }.
    Returns a dict mapping synthetic column names 'col__lag{K}' to values with Nones for unavailable positions.
    """
    out: Dict[str, List[float | None]] = {}
    n = len(frame.dates)
    for col, lags in spec.items():
        base = frame.columns.get(col)
        if base is None:
            continue
        for k in sorted(set(int(l) for l in lags)):
            name = f"{col}__lag{k}"
            vals: List[float | None] = [None] * n
            for i in range(n):
                j = i - k
                if 0 <= j < n:
                    vals[i] = base[j]
            out[name] = vals
    return out

def _rolling_mean(vals: List[Optional[float]], window: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    if window <= 1:
        return [float(v) if v is not None else None for v in vals]
    s = 0.0
    cnt = 0
    for i in range(len(vals)):
        v = vals[i]
        if v is not None:
            s += v
            cnt += 1
        if i >= window:
            old = vals[i - window]
            if old is not None:
                s -= old
                cnt -= 1
        if i >= window - 1 and cnt > 0:
            out[i] = s / cnt
    return out


def _rolling_std(vals: List[Optional[float]], window: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    if window <= 1:
        return [0.0 if v is not None else None for v in vals]
    for i in range(len(vals)):
        j0 = i - window + 1
        if j0 < 0:
            continue
        seg = [vals[j] for j in range(j0, i + 1) if vals[j] is not None]
        if len(seg) < window:
            continue
        m = sum(seg) / len(seg)
        var = sum((x - m) ** 2 for x in seg) / len(seg)
        out[i] = math.sqrt(var)
    return out


def _ema(vals: List[Optional[float]], span: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    if not vals:
        return out
    alpha = 2.0 / (span + 1.0) if span > 0 else 1.0
    ema_val: Optional[float] = None
    for i, v in enumerate(vals):
        if v is None:
            out[i] = ema_val
            continue
        if ema_val is None:
            ema_val = v
        else:
            ema_val = alpha * v + (1 - alpha) * ema_val
        out[i] = ema_val
    return out


def _zscore(vals: List[Optional[float]], window: int) -> List[Optional[float]]:
    mu = _rolling_mean(vals, window)
    sd = _rolling_std(vals, window)
    out: List[Optional[float]] = [None] * len(vals)
    for i in range(len(vals)):
        v = vals[i]
        if v is None or mu[i] is None or sd[i] is None or sd[i] == 0:
            continue
        out[i] = (v - mu[i]) / sd[i]
    return out


def _diff(vals: List[Optional[float]], k: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    for i in range(len(vals)):
        j = i - k
        if j >= 0 and vals[i] is not None and vals[j] is not None:
            out[i] = vals[i] - vals[j]
    return out


def _pct_change(vals: List[Optional[float]], k: int) -> List[Optional[float]]:
    out: List[Optional[float]] = [None] * len(vals)
    eps = 1e-12
    for i in range(len(vals)):
        j = i - k
        if j >= 0 and vals[i] is not None and vals[j] is not None and abs(vals[j]) > eps:
            out[i] = (vals[i] - vals[j]) / abs(vals[j]) * 100.0
    return out


def _apply_derived(frame: TimeSeriesFrame, spec_list: List[Dict]) -> Dict[str, List[Optional[float]]]:
    out: Dict[str, List[Optional[float]]] = {}
    n = len(frame.dates)
    for spec in (spec_list or []):
        on = spec.get("on")
        op = (spec.get("op") or "").lower()
        if not on or on not in frame.columns:
            continue
        base = [float(v) if v is not None else None for v in frame.columns[on]]
        name = None
        vals: List[Optional[float]] = [None] * n
        if op == "diff":
            k = int(spec.get("k", 1))
            vals = _diff(base, k)
            name = f"{on}__diff{k}"
        elif op == "pct_change":
            k = int(spec.get("k", 1))
            vals = _pct_change(base, k)
            name = f"{on}__pctchg{k}"
        elif op == "rolling_mean":
            w = int(spec.get("window", 3))
            vals = _rolling_mean(base, w)
            name = f"{on}__ma{w}"
        elif op == "rolling_std":
            w = int(spec.get("window", 3))
            vals = _rolling_std(base, w)
            name = f"{on}__std{w}"
        elif op == "ema":
            span = int(spec.get("span", 6))
            vals = _ema(base, span)
            name = f"{on}__ema{span}"
        elif op == "zscore":
            w = int(spec.get("window", 12))
            vals = _zscore(base, w)
            name = f"{on}__z{w}"
        else:
            continue
        if name:
            out[name] = vals
    return out


def _pack_to_derived(pack: str, target_id: str, exog: Dict[str, Dict]) -> List[Dict]:
    p = (pack or "").lower().strip()
    derived: List[Dict] = []
    if p == "ta_basic":
        # Target transforms
        derived += [
            {"on": target_id, "op": "diff", "k": 1},
            {"on": target_id, "op": "diff", "k": 12},
            {"on": target_id, "op": "pct_change", "k": 1},
            {"on": target_id, "op": "pct_change", "k": 12},
            {"on": target_id, "op": "rolling_mean", "window": 6},
            {"on": target_id, "op": "rolling_std", "window": 6},
            {"on": target_id, "op": "ema", "span": 6},
        ]
        # Exog simple MAs/EMAs
        for ex in sorted((exog or {}).keys()):
            derived += [
                {"on": ex, "op": "rolling_mean", "window": 3},
                {"on": ex, "op": "ema", "span": 5},
            ]
    return derived


def assemble_supervised_v2(
    frame: TimeSeriesFrame,
    target_id: str,
    features_cfg: Dict,
    horizon: int,
) -> Tuple[List, List[List[float]], List[float], List[float]]:
    """
    Assemble X and y for a given horizon using extended feature config.
    features_cfg may contain: target_lags, exog, derived, pack, normalize, max_features.
    """
    n = len(frame.dates)
    target_lags: List[int] = list((features_cfg or {}).get("target_lags", []))
    exog_cfg: Dict[str, Dict] = (features_cfg or {}).get("exog", {}) or {}
    # Expand __all__ shorthand to all columns except target_id
    if "__all__" in exog_cfg:
        spec_all = exog_cfg.get("__all__") or {}
        expanded: Dict[str, Dict] = {}
        for col in sorted(frame.columns.keys()):
            if col == target_id:
                continue
            expanded[col] = {"lags": list(spec_all.get("lags", []))}
        # Explicitly specified exogs override __all__ for those keys
        for k, v in exog_cfg.items():
            if k == "__all__":
                continue
            expanded[k] = v
        exog_cfg = expanded

    # Build lag specs (baseline features)
    lag_spec: Dict[str, List[int]] = {target_id: list(target_lags)}
    for ex_name, cfg in exog_cfg.items():
        lags = list(cfg.get("lags", []))
        if lags:
            lag_spec[ex_name] = lags
    lagged = build_lagged_columns(frame, lag_spec)

    # Derived transforms (optional)
    derived_spec: List[Dict] = []
    if features_cfg and features_cfg.get("pack"):
        derived_spec.extend(_pack_to_derived(features_cfg.get("pack"), target_id, exog_cfg))
    if features_cfg and features_cfg.get("derived"):
        derived_spec.extend(features_cfg.get("derived"))
    derived_cols = _apply_derived(frame, derived_spec)

    # Optionally normalize all features via rolling z-score
    norm = (features_cfg or {}).get("normalize") or {}
    if norm and (norm.get("method") == "zscore"):
        w = int(norm.get("window", 12))
        # apply to both lagged and derived feature columns
        for name in list(lagged.keys()):
            lagged[name] = _zscore(lagged[name], w)
        for name in list(derived_cols.keys()):
            derived_cols[name] = _zscore(derived_cols[name], w)

    # Column order: lags first (target then exogs), then derived sorted
    target_cols = [f"{target_id}__lag{k}" for k in sorted(set(target_lags))]
    exog_names = sorted([k for k in exog_cfg.keys()])
    exog_cols: List[str] = []
    for name in exog_names:
        lags = sorted(set(exog_cfg.get(name, {}).get("lags", [])))
        for k in lags:
            exog_cols.append(f"{name}__lag{k}")
    derived_order = sorted(derived_cols.keys())

    col_order = target_cols + exog_cols + derived_order

    # Cap features if requested (keep lags preferred)
    max_feat = (features_cfg or {}).get("max_features")
    if isinstance(max_feat, int) and max_feat > 0 and len(col_order) > max_feat:
        # Keep as many derived features as fit after lags
        base_len = len(target_cols) + len(exog_cols)
        keep = max_feat
        if base_len >= keep:
            col_order = (target_cols + exog_cols)[:keep]
        else:
            remain = keep - base_len
            col_order = target_cols + exog_cols + derived_order[:remain]

    max_lag = 0
    if target_lags:
        max_lag = max(max_lag, max(target_lags))
    for name in exog_names:
        lags = exog_cfg.get(name, {}).get("lags", [])
        if lags:
            max_lag = max(max_lag, max(lags))

    origin_dates: List = []
    X: List[List[float]] = []
    y: List[float] = []
    y_t: List[float] = []

    y_series = frame.columns.get(target_id, [])
    for i in range(n):
        # must have features at t and target at t+h
        j_target = i + horizon
        if i < max_lag or j_target >= n:
            continue
        # Check that no feature is None
        row_vals: List[float] = []
        ok = True
        for cname in col_order:
            vals = lagged.get(cname)
            if vals is None:
                # maybe from derived
                vals = derived_cols.get(cname)
            v = None if vals is None else vals[i]
            if v is None or (isinstance(v, float) and not math.isfinite(v)):
                ok = False
                break
            row_vals.append(float(v))
        if not ok:
            continue
        origin_dates.append(frame.dates[i])
        X.append(row_vals)
        y.append(float(y_series[j_target]))
        y_t.append(float(y_series[i]))

    return origin_dates, X, y, y_t


# Backward-compatible wrapper used by earlier code in v2
def assemble_supervised(
    frame: TimeSeriesFrame,
    target_id: str,
    target_lags: List[int],
    exog: Dict[str, Dict[str, List[int]]],
    horizon: int,
) -> Tuple[List, List[List[float]], List[float], List[float]]:
    features_cfg = {"target_lags": target_lags, "exog": exog}
    return assemble_supervised_v2(frame, target_id, features_cfg, horizon)


def build_feature_manifest(frame: TimeSeriesFrame, target_id: str, features_cfg: Dict) -> Dict:
    """Return a manifest dict summarizing feature config and the final column names used.
    Does not depend on horizon (column order is horizon-agnostic)."""
    features_cfg = features_cfg or {}
    target_lags: List[int] = list(features_cfg.get("target_lags", []))
    exog_cfg: Dict[str, Dict] = features_cfg.get("exog", {}) or {}
    pack = features_cfg.get("pack")
    normalize = features_cfg.get("normalize") or {}
    max_features = features_cfg.get("max_features")

    # Build columns deterministically similar to assemble_supervised_v2
    lag_spec: Dict[str, List[int]] = {target_id: list(target_lags)}
    for ex_name, cfg in exog_cfg.items():
        lags = list(cfg.get("lags", []))
        if lags:
            lag_spec[ex_name] = lags
    # Names only
    target_cols = [f"{target_id}__lag{k}" for k in sorted(set(target_lags))]
    exog_names = sorted(list(exog_cfg.keys()))
    exog_cols: List[str] = []
    for name in exog_names:
        lags = sorted(set(exog_cfg.get(name, {}).get("lags", [])))
        for k in lags:
            exog_cols.append(f"{name}__lag{k}")

    # Derived
    derived_spec: List[Dict] = []
    if pack:
        derived_spec.extend(_pack_to_derived(pack, target_id, exog_cfg))
    if features_cfg.get("derived"):
        derived_spec.extend(features_cfg.get("derived"))
    # Derived column names mirroring implementations
    derived_names: List[str] = []
    for spec in derived_spec:
        on = spec.get("on"); op = (spec.get("op") or "").lower()
        if not on or on not in frame.columns:
            continue
        if op == "diff":
            k = int(spec.get("k", 1)); derived_names.append(f"{on}__diff{k}")
        elif op == "pct_change":
            k = int(spec.get("k", 1)); derived_names.append(f"{on}__pctchg{k}")
        elif op == "rolling_mean":
            w = int(spec.get("window", 3)); derived_names.append(f"{on}__ma{w}")
        elif op == "rolling_std":
            w = int(spec.get("window", 3)); derived_names.append(f"{on}__std{w}")
        elif op == "ema":
            span = int(spec.get("span", 6)); derived_names.append(f"{on}__ema{span}")
        elif op == "zscore":
            w = int(spec.get("window", 12)); derived_names.append(f"{on}__z{w}")
        else:
            continue

    derived_order = sorted(derived_names)
    col_order = target_cols + exog_cols + derived_order
    if isinstance(max_features, int) and max_features > 0 and len(col_order) > max_features:
        base_len = len(target_cols) + len(exog_cols)
        if base_len >= max_features:
            col_order = (target_cols + exog_cols)[:max_features]
        else:
            col_order = target_cols + exog_cols + derived_order[: (max_features - base_len)]

    manifest = {
        "pack": pack or None,
        "normalize": normalize or None,
        "target_lags": target_lags,
        "exog_lags": {k: (exog_cfg.get(k, {}) or {}).get("lags", []) for k in exog_names},
        "derived_count": len(derived_order),
        "columns_count": len(col_order),
        "columns": col_order,
    }
    return manifest
