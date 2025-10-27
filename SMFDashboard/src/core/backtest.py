from __future__ import annotations

from typing import Dict, List, Tuple
from datetime import datetime

from .base import BaseModel
from .features import assemble_supervised_v2
from .metrics import rmse_mae
from .utils import format_ymd, advance_date


def split_by_date(
    dates: List[datetime],
    X: List[List[float]],
    y: List[float],
    y_t: List[float],
    start: datetime | None,
    end: datetime | None,
) -> Tuple[List[datetime], List[List[float]], List[float], List[float]]:
    out_d: List[datetime] = []
    out_X: List[List[float]] = []
    out_y: List[float] = []
    out_yt: List[float] = []
    for d, xr, yr, yt in zip(dates, X, y, y_t):
        if start is not None and d < start:
            continue
        if end is not None and d > end:
            continue
        out_d.append(d)
        out_X.append(xr)
        out_y.append(yr)
        out_yt.append(yt)
    return out_d, out_X, out_y, out_yt


def backtest_direct(
    model_factory,
    model_params: Dict,
    frame,
    target_id: str,
    freq: str,
    features_cfg: Dict,
    horizons: List[int],
    train_range: Tuple[datetime | None, datetime | None],
    test_range: Tuple[datetime | None, datetime | None],
    strategy: str = "frozen",
) -> Tuple[Dict[int, Dict[str, float]], List[Dict[str, object]]]:
    """
    Direct multi-horizon backtest with frozen or refit strategies.
    Returns per-horizon metrics and long-form rows per origin/horizon.
    """
    target_lags = features_cfg.get("target_lags", [0])
    exog_cfg = features_cfg.get("exog", {})
    train_start, train_end = train_range
    test_start, test_end = test_range

    all_rows: List[Dict[str, object]] = []
    metrics_by_h: Dict[int, Dict[str, float]] = {}

    for h in sorted(horizons):
        dates, X, y, y_t = assemble_supervised_v2(
            frame=frame,
            target_id=target_id,
            features_cfg=features_cfg,
            horizon=h,
        )
        # train split by origin dates
        d_tr, X_tr, y_tr, ytr_tr = split_by_date(dates, X, y, y_t, train_start, train_end)
        d_te, X_te, y_te, ytr_te = split_by_date(dates, X, y, y_t, test_start, test_end)

        if not d_tr or not d_te:
            metrics_by_h[h] = {"rmse": float("nan"), "mae": float("nan")}
            continue

        if strategy == "frozen":
            model: BaseModel = model_factory(model_params)
            model.fit(X_tr, y_tr)
            preds: List[float] = [model.predict_row(x) for x in X_te]
            m = rmse_mae(y_te, preds)
            metrics_by_h[h] = m
            for d, yt, a, f in zip(d_te, ytr_te, y_te, preds):
                all_rows.append({
                    "origin_date": format_ymd(d),
                    "target_date": format_ymd(advance_date(d, freq=freq, steps=h)),
                    "horizon": h,
                    "y_t": yt,
                    "forecast": f,
                    "actual": a,
                    "error": a - f,
                })
        elif strategy == "refit":
            preds: List[float] = []
            acts: List[float] = []
            rows_local: List[Dict[str, object]] = []
            # For each test origin, refit using all available training origins up to that origin
            for d_cur in d_te:
                # Build cumulative train window: <= d_cur
                d_tr_c, X_tr_c, y_tr_c, _ = split_by_date(dates, X, y, y_t, train_start, d_cur)
                if not d_tr_c:
                    continue
                model: BaseModel = model_factory(model_params)
                model.fit(X_tr_c, y_tr_c)
                # Locate index of current origin
                idx = d_te.index(d_cur)
                x_row = X_te[idx]
                a = y_te[idx]
                f = model.predict_row(x_row)
                preds.append(f)
                acts.append(a)
                rows_local.append({
                    "origin_date": format_ymd(d_cur),
                    "target_date": format_ymd(advance_date(d_cur, freq=freq, steps=h)),
                    "horizon": h,
                    "y_t": ytr_te[idx],
                    "forecast": f,
                    "actual": a,
                    "error": a - f,
                })
            m = rmse_mae(acts, preds)
            metrics_by_h[h] = m
            all_rows.extend(rows_local)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    return metrics_by_h, all_rows
