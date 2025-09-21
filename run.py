#!/usr/bin/env python3
from __future__ import annotations

import sys
import os
import json
import time
from datetime import datetime
import math

# Make v2/src importable when running from repo root
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CUR_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from core.utils import parse_ymd, format_ymd
from core.data import TimeSeriesFrame
from core.registry import discover_plugins
from core.backtest import backtest_direct
from core.output import OutputManager
from core.features import build_feature_manifest
from core.features import assemble_supervised_v2
from core.report import generate_comparison_report_html


def load_recipe(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def build_run_id(prefix: str = "run") -> str:
    ts = time.strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{ts}"


def ensure_synthetic_if_missing(data_path: str, date_col: str = "date", seed: int = 42, synth_cfg: dict | None = None):
    # Only create if path does not exist
    if os.path.isfile(data_path):
        return
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    # Generate monthly dates and simple AR-like process
    from datetime import datetime
    start = datetime(2010, 1, 31)
    end = datetime(2025, 8, 31)
    dates = []
    cur = start
    while cur <= end:
        dates.append(cur)
        y = cur.year + (1 if cur.month == 12 else 0)
        m = 1 if cur.month == 12 else cur.month + 1
        cur = datetime(y, m, 28)
    import random
    random.seed(seed)
    cfg = synth_cfg or {}
    n_exog = int(cfg.get("n_exog", 3))
    mode = (cfg.get("mode") or "mixed").lower()  # 'random' | 'ar' | 'mixed'
    seasonal = bool(cfg.get("seasonal", True))
    break_at = cfg.get("break_at")
    missing_pct = float(cfg.get("missing_pct", 0.0))
    outliers_pct = float(cfg.get("outliers_pct", 0.0))

    # Generate exogenous variables
    T = len(dates)
    exogs = []  # list of lists
    for j in range(n_exog):
        series = [0.0] * T
        m = mode
        if mode == "mixed":
            m = random.choice(["random", "ar"])  # simple mix
        phi = random.uniform(0.2, 0.9)
        sigma = random.uniform(0.5, 1.5)
        seas_amp = random.uniform(0.0, 1.0)
        value = 0.0
        for t in range(T):
            noise = random.gauss(0.0, sigma)
            if m == "random":
                value = noise
            else:  # AR(1)
                value = phi * value + noise
            if seasonal:
                # simple annual cycle on monthly data
                omega = 2 * 3.1415926535 / 12.0
                value += seas_amp * math.sin(omega * t)
            series[t] = value
        exogs.append(series)

    # Build target y from AR(1) + a few exog effects (lag 0 or 1)
    yvals = [0.0] * T
    py = 0.0
    # choose subset of exogs to influence y
    k_use = min(3, n_exog)
    idxs = random.sample(range(n_exog), k_use) if n_exog > 0 else []
    weights = [random.uniform(-0.5, 0.5) for _ in idxs]
    lags = [random.choice([0, 1]) for _ in idxs]
    break_idx = None
    if break_at:
        try:
            from core.utils import parse_ymd
            bdt = parse_ymd(break_at)
            if bdt:
                break_idx = next((i for i, d in enumerate(dates) if d >= bdt), None)
        except Exception:
            break_idx = None
    for t in range(T):
        noise_y = random.gauss(0.0, 0.8)
        val = 0.5 * py
        for kk, (j_idx, w, lag) in enumerate(zip(idxs, weights, lags)):
            tt = t - lag
            if tt >= 0:
                # regime change: flip sign after break
                w_eff = w
                if break_idx is not None and t >= break_idx and kk % 2 == 0:
                    w_eff = -w
                val += w_eff * exogs[j_idx][tt]
        val += noise_y
        yvals[t] = val
        py = val

    # Inject missing values and outliers into exogs (optional)
    if missing_pct > 0:
        total_cells = n_exog * T
        mcount = int(missing_pct * total_cells)
        for _ in range(mcount):
            j = random.randrange(n_exog); t = random.randrange(T)
            exogs[j][t] = float('nan')
    if outliers_pct > 0:
        ocount = int(outliers_pct * n_exog * T)
        for _ in range(ocount):
            j = random.randrange(n_exog); t = random.randrange(T)
            exogs[j][t] += random.gauss(0.0, 6.0)

    # Write CSV: date, y, x1..xN
    import csv
    with open(data_path, "w", newline="") as f:
        w = csv.writer(f)
        headers = [date_col, "y"] + [f"x{j+1}" for j in range(n_exog)]
        w.writerow(headers)
        for i, d in enumerate(dates):
            row = [d.strftime("%Y-%m-%d"), f"{yvals[i]:.6f}"]
            for j in range(n_exog):
                v = exogs[j][i]
                row.append("" if v != v else f"{v:.6f}")  # NaN check: v!=v
            w.writerow(row)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 v2/run.py v2/recipes/<recipe>.json [predict]")
        sys.exit(1)

    recipe_path = sys.argv[1]
    args_tail = sys.argv[2:]
    mode = "predict" if (len(args_tail) >= 1 and args_tail[0].lower().startswith("pred")) else "train"
    recipe = load_recipe(recipe_path)

    # Verbose flag
    verbose = any((a.lower() in ("--verbose", "-v")) for a in args_tail)
    def vprint(msg: str):
        if verbose:
            print(msg)
    t0_total = time.time()

    data_path = recipe["data"]["path"]
    date_col = recipe["data"].get("date_col", "date")
    as_of_date = parse_ymd(recipe.get("as_of_date"))
    synth_cfg = (recipe.get("data", {}) or {}).get("synthetic", {}) if isinstance(recipe.get("data"), dict) else {}
    ensure_synthetic_if_missing(data_path, date_col, synth_cfg=synth_cfg)

    target_id = recipe["target_id"]
    freq = recipe.get("frequency", "M")
    horizons = recipe.get("horizons", [1])
    strategy = recipe.get("strategy", "frozen")

    # Discover plugins and choose model
    plugins = discover_plugins("models")
    model_cfg = recipe.get("model", {})
    model_name = (model_cfg.get("name") or "").strip() if isinstance(model_cfg, dict) else ""
    model_params = model_cfg.get("params", {}) if isinstance(model_cfg, dict) else {}
    all_mode = ("--all" in args_tail) or (model_name.upper() == "ALL")
    if not all_mode:
        if model_name not in plugins:
            print(f"Unknown model: {model_name}. Available: {sorted(list(plugins.keys()))} or use model.name=ALL or --all to run all")
            sys.exit(1)
        create_fn, model_spec = plugins[model_name]

    # Prepare features config and data loading
    if not all_mode:
        # Features: use recipe features if provided; else default from model spec
        if "features" in recipe and recipe["features"]:
            features_cfg = recipe["features"]
        else:
            # derive from model spec
            input_spec = (model_spec or {}).get("input", {})
            features_cfg = {
                "target_lags": list(input_spec.get("target", {}).get("lags", [0])),
                "exog": input_spec.get("exog", {}),
            }
        exog_cfg = (features_cfg.get("exog", {}) or {})
        if "__all__" in exog_cfg:
            select_cols = None  # load all to expand later
        else:
            select_cols = [target_id] + sorted(exog_cfg.keys())
    else:
        # ALL mode: union of exog across plugins (using recipe features if present, else plugin defaults)
        exog_union = set()
        for name, (_create, spec) in plugins.items():
            if "features" in recipe and recipe["features"]:
                exog_union.update((recipe["features"].get("exog", {}) or {}).keys())
            else:
                exog_union.update((spec.get("input", {}).get("exog", {}) or {}).keys())
        # If any recipe variant uses __all__, load all columns
        has_all = False
        if isinstance((recipe.get("features", {}) or {}).get("exog"), dict) and "__all__" in (recipe.get("features", {}) or {}).get("exog", {}):
            has_all = True
        # If exog combination sweep requested, we need all columns available
        sweep_cfg = (recipe.get("features", {}) or {}).get("sweep") or {}
        if isinstance(sweep_cfg, dict) and sweep_cfg.get("exog_combo_k"):
            has_all = True
        select_cols = None if has_all else ([target_id] + sorted(exog_union))
    # Load data frame once with necessary columns
    frame = TimeSeriesFrame.from_csv(data_path, date_col=date_col, select_cols=select_cols, as_of_date=as_of_date)

    out_dir = recipe.get("output", {}).get("dir", os.path.join(CUR_DIR, "outputs"))

    if mode == "train" and all_mode:
        # Run all discovered models and build a comparison report (similar to batch)
        batch_id = build_run_id("all")
        group = OutputManager(base_dir=out_dir, run_id=batch_id)
        summary_rows = []
        # train/test windows
        train_cfg = recipe.get("train", {})
        test_cfg = recipe.get("test", {})
        train_start = parse_ymd(train_cfg.get("start")) if train_cfg.get("start") else None
        train_end = parse_ymd(train_cfg.get("end")) if train_cfg.get("end") else None
        test_start = parse_ymd(test_cfg.get("start")) if test_cfg.get("start") else None
        test_end = parse_ymd(test_cfg.get("end")) if test_cfg.get("end") else None

        idx = 0
        # Build feature variants (sweep) if specified
        features_sweep = []
        sweep_cfg = (recipe.get("features", {}) or {}).get("sweep") or {}
        packs = sweep_cfg.get("packs") or [ (recipe.get("features", {}) or {}).get("pack") ]
        norms = sweep_cfg.get("normalize") or [ (recipe.get("features", {}) or {}).get("normalize") ]
        maxfeats = sweep_cfg.get("max_features") or [ (recipe.get("features", {}) or {}).get("max_features") ]
        # ensure at least one combination (all None means base)
        if not packs:
            packs = [ (recipe.get("features", {}) or {}).get("pack") ]
        if not norms:
            norms = [ (recipe.get("features", {}) or {}).get("normalize") ]
        if not maxfeats:
            maxfeats = [ (recipe.get("features", {}) or {}).get("max_features") ]

        def feature_variants(base_features: Dict):
            base = dict(base_features or {})
            base_target_lags = list(base.get("target_lags", []))
            base_exog = base.get("exog", {}) or {}
            variants = []
            for pk in packs:
                for nm in norms:
                    for mf in maxfeats:
                        v = {"target_lags": base_target_lags, "exog": base_exog}
                        if pk not in (None, "none"):
                            v["pack"] = pk
                        if isinstance(nm, dict) and (nm.get("method") not in (None, "none")):
                            v["normalize"] = nm
                        if isinstance(mf, int):
                            v["max_features"] = mf
                        variants.append(v)
            return variants or [base]

        features_variants = feature_variants(recipe.get("features", {}))
        # Optionally expand exog combinations (choose-k)
        try:
            import itertools
            exog_combo_k = (sweep_cfg.get("exog_combo_k") if isinstance(sweep_cfg, dict) else None)
            exog_combo_limit = (sweep_cfg.get("exog_combo_limit") if isinstance(sweep_cfg, dict) else None)
            exog_combo_names = (sweep_cfg.get("exog_combo_names") if isinstance(sweep_cfg, dict) else None)
            if exog_combo_k and int(exog_combo_k) > 0:
                k = int(exog_combo_k)
                expanded_variants = []
                # Determine candidate exog names from data
                all_cols = list(frame.columns.keys())
                cand = [c for c in all_cols if c != target_id]
                if isinstance(exog_combo_names, list) and exog_combo_names:
                    cand = [c for c in cand if c in exog_combo_names]
                cand = sorted(cand)
                combos = list(itertools.combinations(cand, k))
                if isinstance(exog_combo_limit, int) and exog_combo_limit > 0 and len(combos) > exog_combo_limit:
                    combos = combos[:exog_combo_limit]
                for fv in features_variants:
                    exog_cfg_fv = (fv.get("exog", {}) or {})
                    # infer lags template
                    lags_all = None
                    if "__all__" in exog_cfg_fv:
                        lags_all = list((exog_cfg_fv.get("__all__") or {}).get("lags", []))
                    for combo in combos:
                        fv2 = dict(fv)
                        exog_new = {}
                        for name in combo:
                            lags = None
                            if name in exog_cfg_fv:
                                lags = list((exog_cfg_fv.get(name) or {}).get("lags", []))
                            if lags is None:
                                lags = list(lags_all or [0])
                            exog_new[name] = {"lags": lags}
                        fv2["exog"] = exog_new
                        expanded_variants.append(fv2)
                features_variants = expanded_variants
        except Exception:
            pass

        total_models = len(plugins)
        total_variants = len(features_variants) if isinstance(features_variants, list) else 1
        total_iters = total_models * (total_variants or 1)
        iter_idx = 0
        start_all = time.time()
        vprint(f"[ALL] models={total_models}, variants={total_variants}, total={total_iters}")

        for name in sorted(plugins.keys()):
            idx += 1
            create_fn_i, spec_i = plugins[name]
            # choose base features for this model if recipe lacks
            if not ("features" in recipe and recipe["features"]):
                input_spec = (spec_i or {}).get("input", {})
                base_features = {
                    "target_lags": list(input_spec.get("target", {}).get("lags", [0])),
                    "exog": input_spec.get("exog", {}),
                }
            else:
                base_features = recipe["features"]
            # Iterate variants
            var_count = 0
            for fv in features_variants:
                var_count += 1
                iter_idx += 1
                _iter_start = time.time()
                vprint(f"[{iter_idx}/{total_iters}] model={name} variant={var_count}/{total_variants} strategy={strategy}")
                metrics_by_h, rows = backtest_direct(
                    model_factory=create_fn_i,
                    model_params={},
                    frame=frame,
                    target_id=target_id,
                    freq=freq,
                    features_cfg=fv,
                    horizons=horizons,
                    train_range=(train_start, train_end),
                    test_range=(test_start, test_end),
                    strategy=strategy,
                )
                vprint(f"  OK in {time.time()-_iter_start:.2f}s")
                # Save under members
                run_suffix = f"{name}-{idx:02d}-v{var_count:02d}-{time.strftime('%H%M%S')}"
                om = OutputManager(base_dir=os.path.join(group.run_dir, "members"), run_id=run_suffix)
                om.save_backtest_csv(rows)
                om.save_metrics_csv(metrics_by_h)
                # Compute burn-in (H=1): first used origin index
                total_periods = len(frame.dates)
                try:
                    d1, _X1, _y1, _yt1 = assemble_supervised_v2(frame, target_id, fv, 1)
                    burn_in_h1 = frame.dates.index(d1[0]) if d1 else None
                except Exception:
                    burn_in_h1 = None
                # Save feature manifest
                manifest = build_feature_manifest(frame, target_id, fv)
                try:
                    os.makedirs(om.artifacts_dir, exist_ok=True)
                    with open(os.path.join(om.artifacts_dir, "feature_manifest.json"), "w") as mf:
                        json.dump(manifest, mf, indent=2)
                except Exception:
                    pass
                # Evaluate extended metrics
                try:
                    import importlib.util
                    spec = importlib.util.spec_from_file_location("v2_eval", os.path.join(CUR_DIR, "eval.py"))
                    mod = importlib.util.module_from_spec(spec)
                    assert spec and spec.loader
                    spec.loader.exec_module(mod)
                    ext_i = mod.evaluate_run(om.run_dir)
                except Exception:
                    ext_i = None
                # Collect series for H=1 chart
                try:
                    rows_h1 = [r for r in rows if r.get("horizon") == 1]
                    rows_h1 = sorted(rows_h1, key=lambda r: r.get("target_date", r.get("origin_date", "")))
                    series_h1 = {
                        "dates": [r.get("target_date", r.get("origin_date", "")) for r in rows_h1],
                        "y_t": [float(r.get("y_t")) for r in rows_h1],
                        "actual": [float(r.get("actual")) for r in rows_h1],
                        "forecast": [float(r.get("forecast")) for r in rows_h1],
                    }
                except Exception:
                    series_h1 = None

                # Short feature description
                desc_parts = []
                if fv.get("pack"):
                    desc_parts.append(f"pack={fv.get('pack')}")
                norm = fv.get("normalize", {}) or {}
                if isinstance(norm, dict) and norm.get("method") and norm.get("method") != "none":
                    if norm.get("method") == "zscore":
                        desc_parts.append(f"norm=z({norm.get('window', '')})")
                    else:
                        desc_parts.append(f"norm={norm.get('method')}")
                t_lags = fv.get("target_lags", [])
                if t_lags:
                    desc_parts.append(f"t_lags={t_lags}")
                exog_desc = []
                for exn in sorted((fv.get("exog", {}) or {}).keys()):
                    l = (fv.get("exog", {}) or {}).get(exn, {}).get("lags", [])
                    if l:
                        exog_desc.append(f"{exn}{l}")
                if exog_desc:
                    desc_parts.append("exog=" + ",".join(exog_desc))
                if isinstance(fv.get("max_features"), int):
                    desc_parts.append(f"maxF={fv.get('max_features')}")
                feature_desc = "; ".join(desc_parts) if desc_parts else "lags-only"

                summary_rows.append({
                    "model_name": name,
                    "strategy": strategy,
                    "run_dir": om.run_dir,
                    "rmse": {h: metrics_by_h.get(h, {}).get("rmse") for h in horizons},
                    "mae": {h: metrics_by_h.get(h, {}).get("mae") for h in horizons},
                    "series_h1": series_h1,
                    "ext": ext_i or {},
                    "feature_desc": feature_desc,
                    "total_periods": total_periods,
                    "burn_in_h1": burn_in_h1,
                })

        vprint(f"[ALL] complete | elapsed={time.time()-start_all:.2f}s")

        # Write comparison outputs
        # CSV
        import csv as _csv
        csv_path = os.path.join(group.run_dir, "metrics_summary.csv")
        all_h = sorted({h for row in summary_rows for h in (row.get("rmse", {}) or {}).keys()}) or sorted(horizons)
        with open(csv_path, "w", newline="") as f:
            w = _csv.writer(f)
            w.writerow(["model_name", "strategy", "run_dir"] + [f"rmse_h{h}" for h in all_h] + [f"mae_h{h}" for h in all_h])
            for row in summary_rows:
                rmse_vals = [row.get("rmse", {}).get(h, "") for h in all_h]
                mae_vals = [row.get("mae", {}).get(h, "") for h in all_h]
                w.writerow([row.get("model_name"), row.get("strategy"), row.get("run_dir")] + rmse_vals + mae_vals)
        # HTML
        report_dir = os.path.join(group.run_dir, "report")
        os.makedirs(report_dir, exist_ok=True)
        html_doc = generate_comparison_report_html(
            title=f"All Models Comparison — {batch_id}", metrics_rows=summary_rows, horizons=all_h
        )
        with open(os.path.join(report_dir, "index.html"), "w") as f:
            f.write(html_doc)
        print(f"All-model run complete. Summary: {csv_path}\nReport: {os.path.join(report_dir, 'index.html')}")
        return

    if mode == "train":
        run_id = build_run_id(model_name)
        om = OutputManager(base_dir=out_dir, run_id=run_id)

        train_cfg = recipe.get("train", {})
        test_cfg = recipe.get("test", {})
        train_start = parse_ymd(train_cfg.get("start")) if train_cfg.get("start") else None
        train_end = parse_ymd(train_cfg.get("end")) if train_cfg.get("end") else None
        test_start = parse_ymd(test_cfg.get("start")) if test_cfg.get("start") else None
        test_end = parse_ymd(test_cfg.get("end")) if test_cfg.get("end") else None
        vprint(f"Training model={model_name} | horizons={horizons} | strategy={strategy}")
        try:
            _mf = build_feature_manifest(frame, target_id, features_cfg)
            vprint(f"Features={_mf.get('columns_count')}")
        except Exception:
            pass
        _t_bt = time.time()
        # Backtest
        metrics_by_h, rows = backtest_direct(
            model_factory=create_fn,
            model_params=model_params,
            frame=frame,
            target_id=target_id,
            freq=freq,
            features_cfg=features_cfg,
            horizons=horizons,
            train_range=(train_start, train_end),
            test_range=(test_start, test_end),
            strategy=strategy,
        )
        vprint(f"Backtest done in {time.time()-_t_bt:.2f}s")

        # Train final models on full train range and save params per horizon
        from core.features import assemble_supervised
        for h in sorted(horizons):
            d_tr, X_tr, y_tr, _ = assemble_supervised_v2(
                frame=frame,
                target_id=target_id,
                features_cfg=features_cfg,
                horizon=h,
            )
            # filter by train window
            def _filter_by_date(dates, X, y, start, end):
                out_d, out_X, out_y = [], [], []
                for d, xr, yr in zip(dates, X, y):
                    if start is not None and d < start:
                        continue
                    if end is not None and d > end:
                        continue
                    out_d.append(d); out_X.append(xr); out_y.append(yr)
                return out_d, out_X, out_y
            _, X_fit, y_fit = _filter_by_date(d_tr, X_tr, y_tr, train_start, train_end)
            if X_fit and y_fit:
                m = create_fn(model_params)
                m.fit(X_fit, y_fit)
                om.save_model_params(h, model_name, m.get_params())

        lineage = {
            "model_name": model_name,
            "model_params": model_params,
            "target_id": target_id,
            "frequency": freq,
            "horizons": horizons,
            "strategy": strategy,
            "features": features_cfg,
            "train_window": {"start": format_ymd(train_start), "end": format_ymd(train_end)},
            "test_window": {"start": format_ymd(test_start), "end": format_ymd(test_end)},
            "recipe_path": recipe_path,
        }
        om.save_lineage(lineage)
        om.save_backtest_csv(rows)
        om.save_metrics_csv(metrics_by_h)
        # Save feature manifest for single run
        try:
            manifest = build_feature_manifest(frame, target_id, features_cfg)
            os.makedirs(om.artifacts_dir, exist_ok=True)
            with open(os.path.join(om.artifacts_dir, "feature_manifest.json"), "w") as mf:
                json.dump(manifest, mf, indent=2)
        except Exception:
            pass
        # Also run extended evaluation (RMSE, MAE, R2, MAPE, sMAPE, bias, direction metrics)
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("v2_eval", os.path.join(CUR_DIR, "eval.py"))
            mod = importlib.util.module_from_spec(spec)
            assert spec and spec.loader
            spec.loader.exec_module(mod)
            mod.evaluate_run(om.run_dir)
        except Exception:
            pass

        print(f"Training complete. Outputs written to: {om.run_dir}")
        vprint(f"Total elapsed: {time.time()-t0_total:.2f}s")

    else:  # predict mode
        # Find latest trained run for this model
        om_probe = OutputManager(base_dir=out_dir, run_id="probe")
        latest_dir = om_probe.find_latest_with_models(prefix=model_name)
        if latest_dir is None:
            print("No existing trained model found for predict. Train first.")
            sys.exit(1)

        # Load per-horizon model params
        models_dir = os.path.join(latest_dir, "models")
        model_files = [f for f in os.listdir(models_dir) if f.startswith("model_h") and f.endswith(".json")]
        if not model_files:
            print("No saved models in latest run.")
            sys.exit(1)

        # Discover plugins again (fresh mapping)
        plugins = discover_plugins("models")

        # Build features at the last available origin (as_of_date capped)
        preds_rows = []
        for f in sorted(model_files):
            with open(os.path.join(models_dir, f), "r") as fp:
                obj = json.load(fp)
            plugin = obj.get("plugin")
            params = obj.get("params", {})
            if plugin not in plugins:
                print(f"Missing plugin '{plugin}' for saved model {f}")
                continue
            create_fn, _ = plugins[plugin]
            h_str = f.split("model_h")[-1].split(".")[0]
            try:
                h = int(h_str)
            except Exception:
                continue
            dates, X, y, y_t = assemble_supervised_v2(
                frame=frame,
                target_id=target_id,
                features_cfg=recipe.get("features", {}),
                horizon=h,
            )
            if not dates:
                continue
            # Use last origin row
            m = create_fn(params)
            m.set_params(params)
            x_last = X[-1]
            d_last = dates[-1]
            yhat = m.predict_row(x_last)
            preds_rows.append({
                "origin_date": format_ymd(d_last),
                "target_date": format_ymd(_advance_date_safe(d_last, freq=freq, steps=h)),
                "horizon": h,
                "y_t": y_t[-1],
                "forecast": yhat,
            })

        # Write predict.csv under a new run dir
        run_id = build_run_id(f"{model_name}-predict")
        om = OutputManager(base_dir=out_dir, run_id=run_id)
        # Save minimal lineage
        om.save_lineage({
            "model_name": model_name,
            "source_model_dir": latest_dir,
            "target_id": target_id,
            "frequency": freq,
            "horizons": sorted([r["horizon"] for r in preds_rows]),
            "features": recipe.get("features", {}),
            "as_of_date": format_ymd(as_of_date),
        })
        # Save predict.csv
        pred_path = os.path.join(om.forecasts_dir, "predict.csv")
        with open(pred_path, "w", newline="") as f:
            w = __import__("csv").writer(f)
            w.writerow(["origin_date", "target_date", "horizon", "y_t", "forecast"])
            for r in sorted(preds_rows, key=lambda z: z["horizon"]):
                w.writerow([r["origin_date"], r["target_date"], r["horizon"], r["y_t"], r["forecast"]])
        print(f"Prediction complete. Outputs written to: {om.run_dir}")
        vprint(f"Total elapsed: {time.time()-t0_total:.2f}s")


def _advance_date_safe(d: datetime, freq: str, steps: int):
    from core.utils import advance_date
    return advance_date(d, freq=freq, steps=steps)


if __name__ == "__main__":
    main()
