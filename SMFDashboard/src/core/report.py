from __future__ import annotations

from typing import Dict, List, Tuple
import html
import math


def generate_comparison_report_html(
    title: str,
    metrics_rows: List[Dict[str, object]],
    horizons: List[int],
) -> str:
    """
    Build a tabular comparison report only (no charts).
    metrics_rows: list of rows each containing:
      - model_name, strategy, run_dir
      - rmse: {h: val}, mae: {h: val}  (optional)
      - ext: {h: {n, rmse, mae, r2, mape_pct, smape_pct, bias, direction_accuracy_pct, pct_up, pct_down, hit_rate_up_pct, hit_rate_down_pct}}
    """
    base_cols = ["Model", "Strategy", "Run Dir", "Features", "H1 Chart", "H1 Dir", "Total N", "BurnIn@H1"]
    metric_names = [
        ("rmse", "RMSE"),
        ("mae", "MAE"),
        ("r2", "R2"),
        ("mape_pct", "MAPE%"),
        ("smape_pct", "sMAPE%"),
        ("bias", "Bias"),
        ("direction_accuracy_pct", "DirAcc%"),
        ("pct_up", "%Up"),
        ("pct_down", "%Down"),
        ("hit_rate_up_pct", "HitUp%"),
        ("hit_rate_down_pct", "HitDown%"),
    ]
    head_cols: List[str] = base_cols[:]
    for h in horizons:
        for key, label in metric_names:
            head_cols.append(f"{label}@H={h}")

    def fmt(key: str, v: float) -> str:
        if not isinstance(v, (int, float)) or not math.isfinite(v):
            return ""
        if key.endswith("%") or key in {"mape_pct", "smape_pct", "direction_accuracy_pct", "pct_up", "pct_down", "hit_rate_up_pct", "hit_rate_down_pct"}:
            return f"{v:.2f}"
        return f"{v:.4f}"

    def cell(val, highlight: bool = False):
        style = "background:#e8f5e9" if highlight else ""
        return f"<td style='{style}'>{html.escape(str(val))}</td>"

    def cell_raw(html_str: str) -> str:
        return f"<td>{html_str}</td>"

    # Build best map for highlighting per metric/horizon
    def best_value(metric_key: str, values: List[float]):
        vals = [v for v in values if isinstance(v, (int, float)) and math.isfinite(v)]
        if not vals:
            return None
        if metric_key in ("rmse", "mae", "mape_pct", "smape_pct"):
            return min(vals)
        if metric_key in ("r2", "direction_accuracy_pct", "hit_rate_up_pct", "hit_rate_down_pct"):
            return max(vals)
        if metric_key == "bias":
            return min(vals, key=lambda x: abs(x))
        return None

    best_map: Dict[tuple, float] = {}
    for h in horizons:
        for key, _label in metric_names:
            vals = []
            for row in metrics_rows:
                ext = row.get("ext", {}) or {}
                e = ext.get(h, {}) if isinstance(ext, dict) else {}
                if key in ("rmse", "mae") and key not in e:
                    v = (row.get(key, {}) or {}).get(h)
                else:
                    v = e.get(key)
                if isinstance(v, (int, float)) and math.isfinite(v):
                    vals.append(v)
            b = best_value(key, vals)
            if b is not None:
                best_map[(key, h)] = b

    rows_html: List[str] = []
    for row in metrics_rows:
        tds: List[str] = []
        tds.append(cell(row.get("model_name", "")))
        tds.append(cell(row.get("strategy", "")))
        tds.append(cell(row.get("run_dir", "")))
        tds.append(cell(row.get("feature_desc", "")))
        # H1 sparkline
        def _spark(series_h1: Dict[str, object] | None) -> str:
            try:
                if not series_h1:
                    return ""
                actual = series_h1.get("actual") or []
                forecast = series_h1.get("forecast") or []
                if not actual or not forecast:
                    return ""
                # keep tail to limit size
                tail = 40
                actual = actual[-tail:]
                forecast = forecast[-tail:]
                # compute min/max
                vals = [v for v in actual + forecast if isinstance(v, (int, float)) and math.isfinite(v)]
                if not vals:
                    return ""
                mn = min(vals); mx = max(vals)
                if mx - mn < 1e-12:
                    mx = mn + 1.0
                width = 220; height = 60; pad = 6
                plot_w = width - 2 * pad; plot_h = height - 2 * pad
                n = max(len(actual), len(forecast))
                def xy(i: int, v: float):
                    x = pad + (plot_w * i) / max(1, n - 1)
                    y = pad + plot_h * (1 - (v - mn) / (mx - mn))
                    return f"{x:.1f},{y:.1f}"
                pts_a = " ".join(xy(i, float(v)) for i, v in enumerate(actual))
                pts_f = " ".join(xy(i, float(v)) for i, v in enumerate(forecast))
                svg = []
                svg.append(f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>")
                svg.append(f"<rect x='0' y='0' width='{width}' height='{height}' fill='#fff' stroke='#eee'/>")
                svg.append(f"<polyline fill='none' stroke='#2c7fb8' stroke-width='1.5' points='{pts_a}'/>")
                svg.append(f"<polyline fill='none' stroke='#de2d26' stroke-width='1.5' points='{pts_f}'/>")
                svg.append("</svg>")
                return "".join(svg)
            except Exception:
                return ""
        tds.append(cell_raw(_spark(row.get("series_h1"))))
        # H1 direction arrows grid (predicted direction colored by correctness vs actual)
        def _dirgrid(series_h1: Dict[str, object] | None) -> str:
            try:
                if not series_h1:
                    return ""
                yts = series_h1.get("y_t") or []
                actual = series_h1.get("actual") or []
                forecast = series_h1.get("forecast") or []
                n = min(len(yts), len(actual), len(forecast))
                if n == 0:
                    return ""
                tail = 30
                start = max(0, n - tail)
                items = []
                eps = 1e-9
                for i in range(start, n):
                    yt = float(yts[i]); a = float(actual[i]); f = float(forecast[i])
                    da = 1 if a - yt > eps else (-1 if yt - a > eps else 0)
                    dp = 1 if f - yt > eps else (-1 if yt - f > eps else 0)
                    ok = (da != 0 and dp == da)
                    items.append((dp, ok))
                # Render as small SVG with triangles per item
                cell_w = 8; cell_h = 10; pad = 2
                width = pad*2 + cell_w*len(items)
                height = cell_h + pad*2
                svg = [f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}'>",
                       f"<rect x='0' y='0' width='{width}' height='{height}' fill='#fff' stroke='#eee'/>"]
                for idx, (dp, ok) in enumerate(items):
                    cx = pad + idx*cell_w + cell_w/2
                    color = '#2ca02c' if ok else '#bbbbbb'
                    if dp > 0:
                        # up triangle
                        points = f"{cx},{pad} {cx-cell_w/2+1},{pad+cell_h-1} {cx+cell_w/2-1},{pad+cell_h-1}"
                        svg.append(f"<polygon points='{points}' fill='{color}' />")
                    elif dp < 0:
                        # down triangle
                        points = f"{cx},{pad+cell_h-1} {cx-cell_w/2+1},{pad} {cx+cell_w/2-1},{pad}"
                        svg.append(f"<polygon points='{points}' fill='{color}' />")
                    else:
                        # flat: small square
                        s = 3
                        svg.append(f"<rect x='{cx-s}' y='{pad + cell_h/2 - s}' width='{2*s}' height='{2*s}' fill='{color}' />")
                svg.append("</svg>")
                return "".join(svg)
            except Exception:
                return ""
        tds.append(cell_raw(_dirgrid(row.get("series_h1"))))
        # totals/burn-in
        tds.append(cell(row.get("total_periods", "")))
        tds.append(cell(row.get("burn_in_h1", "")))

        ext = row.get("ext", {}) or {}
        rm = row.get("rmse", {}) or {}
        ma = row.get("mae", {}) or {}
        for h in horizons:
            e = ext.get(h, {}) if isinstance(ext, dict) else {}
            rmse_v = e.get("rmse", rm.get(h))
            mae_v = e.get("mae", ma.get(h))
            values = {
                "rmse": rmse_v,
                "mae": mae_v,
                "r2": e.get("r2"),
                "mape_pct": e.get("mape_pct"),
                "smape_pct": e.get("smape_pct"),
                "bias": e.get("bias"),
                "direction_accuracy_pct": e.get("direction_accuracy_pct"),
                "pct_up": e.get("pct_up"),
                "pct_down": e.get("pct_down"),
                "hit_rate_up_pct": e.get("hit_rate_up_pct"),
                "hit_rate_down_pct": e.get("hit_rate_down_pct"),
            }
            for key, _label in metric_names:
                v = values.get(key)
                is_best = False
                b = best_map.get((key, h))
                if b is not None and isinstance(v, (int, float)) and math.isfinite(v):
                    if key == "bias":
                        is_best = (abs(v) == abs(b))
                    elif key in ("rmse", "mae", "mape_pct", "smape_pct", "r2", "direction_accuracy_pct", "hit_rate_up_pct", "hit_rate_down_pct"):
                        is_best = (v == b)
                tds.append(cell(fmt(key, v), highlight=is_best))
        rows_html.append("<tr>" + "".join(tds) + "</tr>")

    html_doc = f"""
<!DOCTYPE html>
<html><head>
  <meta charset='utf-8' />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: -apple-system, Segoe UI, Arial, sans-serif; margin: 20px; color: #222; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #eee; padding: 8px 10px; font-size: 13px; text-align: left; }}
    th {{ background: #fafafa; position: sticky; top: 0; }}
    .legend {{ color:#555; font-size:12px; margin: 6px 0 12px 0; }}
  </style>
  </head>
  <body>
    <h1>{html.escape(title)}</h1>
    <div class='legend'>H1 Chart: blue = Actual, red = Forecast. H1 Dir: arrows show predicted direction; green = matches actual, gray = mismatch.</div>
    <table>
      <tr>{''.join(f'<th>{html.escape(c)}</th>' for c in head_cols)}</tr>
      {''.join(rows_html)}
    </table>
  </body></html>
"""
    return html_doc
