#!/usr/bin/env python3
"""
Enhanced Nowcasting Runner with Intelligent Caching

This is the main entry point for v2 that includes:
- Model result caching to avoid redundant training
- Backward compatibility with original run.py
- Cache management utilities
"""

from __future__ import annotations

import sys
import os
import json
import time
from datetime import datetime
import argparse

# Make v2/src importable
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CUR_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from core.utils import parse_ymd, format_ymd
from core.data import TimeSeriesFrame
from core.registry import discover_plugins
from core.backtest import backtest_direct
from core.output import OutputManager
from core.features import build_feature_manifest, assemble_supervised_v2
from core.report import generate_comparison_report_html
from core.cache import CacheManager


def load_recipe(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def build_run_id(prefix: str = "run") -> str:
    ts = time.strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{ts}"


def main():
    parser = argparse.ArgumentParser(description="Enhanced Nowcasting with Caching")
    parser.add_argument("recipe", help="Path to recipe JSON file")
    parser.add_argument("--mode", choices=["train", "predict"], default="train",
                        help="Execution mode")
    parser.add_argument("--all", action="store_true",
                        help="Run all models in batch")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Verbose output")
    parser.add_argument("--cache", choices=["use", "ignore", "rebuild"], default="use",
                        help="Cache mode: use (default), ignore, or rebuild")
    parser.add_argument("--cache-stats", action="store_true",
                        help="Show cache statistics and exit")
    parser.add_argument("--clear-cache", action="store_true",
                        help="Clear all cache entries and exit")

    args = parser.parse_args()

    # Initialize cache manager
    cache_mgr = CacheManager(
        base_dir=os.path.join(CUR_DIR, "model_library"),
        verbose=args.verbose
    )

    # Handle cache management commands
    if args.cache_stats:
        stats = cache_mgr.get_cache_stats()
        print("\n=== Cache Statistics ===")
        print(f"Total entries: {stats['total_entries']}")
        print(f"Total models: {stats['total_models']}")
        print(f"Cache size: {stats['cache_size_mb']:.2f} MB")
        if stats['oldest_entry']:
            print(f"Oldest entry: {stats['oldest_entry']}")
        if stats['newest_entry']:
            print(f"Newest entry: {stats['newest_entry']}")
        return

    if args.clear_cache:
        confirm = input("Are you sure you want to clear all cache? (yes/no): ")
        if confirm.lower() == "yes":
            cache_mgr.clear_cache()
            print("Cache cleared successfully")
        return

    # Load recipe
    recipe_path = args.recipe
    recipe = load_recipe(recipe_path)

    # Extract configuration
    target_id = recipe["target_id"]
    freq = recipe.get("frequency", "M")
    horizons = recipe.get("horizons", [1])
    strategy = recipe.get("strategy", "frozen")
    mode = args.mode
    all_mode = args.all
    verbose = args.verbose

    def vprint(msg):
        if verbose:
            print(msg)

    t0_total = time.time()

    # Load data
    data_cfg = recipe.get("data", {})
    data_path = data_cfg.get("path")
    if not data_path:
        print("Error: data.path not specified in recipe")
        sys.exit(1)

    # Handle synthetic data generation
    if data_cfg.get("synthetic", {}).get("enabled"):
        from run import ensure_synthetic_if_missing
        ensure_synthetic_if_missing(
            data_path,
            data_cfg.get("date_col", "date"),
            seed=data_cfg.get("synthetic", {}).get("seed", 42),
            synth_cfg=data_cfg.get("synthetic", {})
        )

    # Load data frame
    date_col = data_cfg.get("date_col", "date")
    as_of_date = parse_ymd(recipe.get("as_of_date")) if recipe.get("as_of_date") else None

    # Determine columns to load
    plugins = discover_plugins("models")
    model_name = recipe.get("model", {}).get("name")

    if not all_mode and model_name:
        features_cfg = recipe.get("features", {})
        exog_cfg = (features_cfg.get("exog", {}) or {})
        if "__all__" in exog_cfg:
            select_cols = None
        else:
            select_cols = [target_id] + sorted(exog_cfg.keys())
    else:
        # ALL mode: union of exog across plugins
        exog_union = set()
        for name, (_create, spec) in plugins.items():
            if "features" in recipe and recipe["features"]:
                exog_union.update((recipe["features"].get("exog", {}) or {}).keys())
            else:
                exog_union.update((spec.get("input", {}).get("exog", {}) or {}).keys())
        has_all = False
        if isinstance((recipe.get("features", {}) or {}).get("exog"), dict) and "__all__" in (recipe.get("features", {}) or {}).get("exog", {}):
            has_all = True
        sweep_cfg = (recipe.get("features", {}) or {}).get("sweep") or {}
        if isinstance(sweep_cfg, dict) and sweep_cfg.get("exog_combo_k"):
            has_all = True
        select_cols = None if has_all else ([target_id] + sorted(exog_union))

    # Load data frame
    frame = TimeSeriesFrame.from_csv(data_path, date_col=date_col, select_cols=select_cols, as_of_date=as_of_date)

    # Compute data fingerprint for cache validation
    data_fingerprint = cache_mgr.compute_data_fingerprint(frame)

    out_dir = recipe.get("output", {}).get("dir", os.path.join(CUR_DIR, "outputs"))

    if mode == "train":
        train_cfg = recipe.get("train", {})
        test_cfg = recipe.get("test", {})
        train_start = parse_ymd(train_cfg.get("start")) if train_cfg.get("start") else None
        train_end = parse_ymd(train_cfg.get("end")) if train_cfg.get("end") else None
        test_start = parse_ymd(test_cfg.get("start")) if test_cfg.get("start") else None
        test_end = parse_ymd(test_cfg.get("end")) if test_cfg.get("end") else None

        if all_mode:
            # Run all models with caching support
            _run_all_models_cached(
                recipe, frame, target_id, freq, horizons, strategy,
                train_start, train_end, test_start, test_end,
                data_fingerprint, out_dir, cache_mgr, args.cache, verbose,
                recipe_path
            )
        else:
            # Single model training with caching
            _run_single_model_cached(
                recipe, frame, target_id, freq, horizons, strategy,
                train_start, train_end, test_start, test_end,
                data_fingerprint, out_dir, cache_mgr, args.cache, verbose,
                recipe_path
            )

    else:  # predict mode
        # Prediction mode - use latest cached or trained model
        _run_predict_cached(
            recipe, frame, target_id, freq, out_dir, verbose
        )

    vprint(f"Total elapsed: {time.time()-t0_total:.2f}s")


def _run_single_model_cached(
    recipe, frame, target_id, freq, horizons, strategy,
    train_start, train_end, test_start, test_end,
    data_fingerprint, out_dir, cache_mgr, cache_mode, verbose,
    recipe_path
):
    """Run single model training with cache support."""

    def vprint(msg):
        if verbose:
            print(msg)

    plugins = discover_plugins("models")
    model_name = recipe.get("model", {}).get("name")
    model_params = recipe.get("model", {}).get("params", {})
    features_cfg = recipe.get("features", {})

    if model_name not in plugins:
        print(f"Model '{model_name}' not found")
        sys.exit(1)

    create_fn, _ = plugins[model_name]

    # Generate cache key
    cache_key = cache_mgr.generate_cache_key(
        model_name=model_name,
        model_params=model_params,
        target_id=target_id,
        features_cfg=features_cfg,
        horizons=horizons,
        train_range=(train_start, train_end),
        test_range=(test_start, test_end),
        data_fingerprint=data_fingerprint,
        frequency=freq,
        strategy=strategy
    )

    vprint(f"Cache key: {cache_key}")

    # Check cache
    use_cache = False
    if cache_mode == "use":
        cache_entry = cache_mgr.check_cache(cache_key)
        if cache_entry:
            vprint(f"[Cache HIT] Found cached results from {cache_entry['created']}")
            use_cache = True
    elif cache_mode == "rebuild":
        vprint("[Cache] Rebuild mode - ignoring existing cache")

    run_id = build_run_id(model_name)
    om = OutputManager(base_dir=out_dir, run_id=run_id)

    if use_cache:
        # Load from cache
        cached_models = cache_mgr.load_cached_models(cache_key)
        cached_results = cache_mgr.load_cached_results(cache_key)

        # Save cached models to output directory
        for h, model_data in cached_models.items():
            om.save_model_params(h, model_data["plugin"], model_data["params"])

        # Save cached metrics
        if "metrics" in cached_results:
            om.save_metrics_csv(cached_results["metrics"])

        # Save cached backtest results
        if "backtest" in cached_results:
            om.save_backtest_csv(cached_results["backtest"])

        vprint(f"[Cache] Loaded cached results to: {om.run_dir}")

    else:
        # Train from scratch
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

        # Train final models and collect for caching
        models_for_cache = {}
        for h in sorted(horizons):
            d_tr, X_tr, y_tr, _ = assemble_supervised_v2(
                frame=frame,
                target_id=target_id,
                features_cfg=features_cfg,
                horizon=h,
            )

            # Filter by train window
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
                models_for_cache[h] = {
                    "plugin": model_name,
                    "params": m.get_params()
                }

        # Save lineage
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
            "cache_key": cache_key
        }
        om.save_lineage(lineage)
        om.save_backtest_csv(rows)
        om.save_metrics_csv(metrics_by_h)

        # Save feature manifest
        try:
            manifest = build_feature_manifest(frame, target_id, features_cfg)
            os.makedirs(om.artifacts_dir, exist_ok=True)
            with open(os.path.join(om.artifacts_dir, "feature_manifest.json"), "w") as mf:
                json.dump(manifest, mf, indent=2)
        except Exception:
            pass

        # Run extended evaluation
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("v2_eval", os.path.join(CUR_DIR, "eval.py"))
            mod = importlib.util.module_from_spec(spec)
            assert spec and spec.loader
            spec.loader.exec_module(mod)
            mod.evaluate_run(om.run_dir)
        except Exception:
            pass

        # Save to cache
        if cache_mode != "ignore":
            cache_mgr.save_to_cache(
                cache_key=cache_key,
                models=models_for_cache,
                metrics=metrics_by_h,
                backtest_rows=rows,
                metadata={
                    "model_name": model_name,
                    "strategy": strategy,
                    "horizons": horizons,
                    "train_window": [format_ymd(train_start), format_ymd(train_end)],
                    "test_window": [format_ymd(test_start), format_ymd(test_end)],
                }
            )
            vprint(f"[Cache] Saved results to cache: {cache_key}")

    print(f"Training complete. Outputs written to: {om.run_dir}")


def _run_all_models_cached(
    recipe, frame, target_id, freq, horizons, strategy,
    train_start, train_end, test_start, test_end,
    data_fingerprint, out_dir, cache_mgr, cache_mode, verbose,
    recipe_path
):
    """Run all models in batch with cache support."""

    def vprint(msg):
        if verbose:
            print(msg)

    from run import _advance_date_safe
    plugins = discover_plugins("models")

    # Filter models if specified
    models_filter = recipe.get("models_filter", [])
    if models_filter:
        filtered_plugins = {}
        for name, plugin in plugins.items():
            # Check if model name matches any filter (case-insensitive partial match)
            name_lower = name.lower()
            for filter_name in models_filter:
                if filter_name.lower() in name_lower or name_lower in filter_name.lower():
                    filtered_plugins[name] = plugin
                    break
        plugins = filtered_plugins
        vprint(f"Filtered to {len(plugins)} models: {sorted(plugins.keys())}")

    batch_id = build_run_id("all")
    group = OutputManager(base_dir=out_dir, run_id=batch_id)
    summary_rows = []

    # Build feature variants
    features_sweep = []
    sweep_cfg = (recipe.get("features", {}) or {}).get("sweep") or {}
    packs = sweep_cfg.get("packs") or [(recipe.get("features", {}) or {}).get("pack")]
    norms = sweep_cfg.get("normalize") or [(recipe.get("features", {}) or {}).get("normalize")]
    maxfeats = sweep_cfg.get("max_features") or [(recipe.get("features", {}) or {}).get("max_features")]

    if not packs:
        packs = [(recipe.get("features", {}) or {}).get("pack")]
    if not norms:
        norms = [(recipe.get("features", {}) or {}).get("normalize")]
    if not maxfeats:
        maxfeats = [(recipe.get("features", {}) or {}).get("max_features")]

    def feature_variants(base_features):
        from typing import Dict
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

    # Handle exog combinations
    try:
        import itertools
        exog_combo_k = (sweep_cfg.get("exog_combo_k") if isinstance(sweep_cfg, dict) else None)
        exog_combo_limit = (sweep_cfg.get("exog_combo_limit") if isinstance(sweep_cfg, dict) else None)
        exog_combo_names = (sweep_cfg.get("exog_combo_names") if isinstance(sweep_cfg, dict) else None)

        if exog_combo_k and int(exog_combo_k) > 0:
            k = int(exog_combo_k)
            expanded_variants = []
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

    cache_hits = 0
    cache_misses = 0

    for name in sorted(plugins.keys()):
        create_fn_i, spec_i = plugins[name]

        # Choose base features
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

            # Generate cache key
            cache_key = cache_mgr.generate_cache_key(
                model_name=name,
                model_params={},
                target_id=target_id,
                features_cfg=fv,
                horizons=horizons,
                train_range=(train_start, train_end),
                test_range=(test_start, test_end),
                data_fingerprint=data_fingerprint,
                frequency=freq,
                strategy=strategy
            )

            # Check cache
            use_cache = False
            if cache_mode == "use":
                cache_entry = cache_mgr.check_cache(cache_key)
                if cache_entry:
                    cache_hits += 1
                    use_cache = True
                    vprint(f"[{iter_idx}/{total_iters}] model={name} variant={var_count}/{total_variants} [CACHE HIT]")
                else:
                    cache_misses += 1

            if use_cache:
                # Load from cache
                cached_results = cache_mgr.load_cached_results(cache_key)
                metrics_by_h = cached_results.get("metrics", {})
                rows = cached_results.get("backtest", [])
            else:
                # Train from scratch
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

                # Save to cache if not in ignore mode
                if cache_mode != "ignore":
                    # Train final models for caching
                    models_for_cache = {}
                    for h in sorted(horizons):
                        d_tr, X_tr, y_tr, _ = assemble_supervised_v2(
                            frame=frame,
                            target_id=target_id,
                            features_cfg=fv,
                            horizon=h,
                        )

                        # Filter by train window
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
                            m = create_fn_i({})
                            m.fit(X_fit, y_fit)
                            models_for_cache[h] = {
                                "plugin": name,
                                "params": m.get_params()
                            }

                    cache_mgr.save_to_cache(
                        cache_key=cache_key,
                        models=models_for_cache,
                        metrics=metrics_by_h,
                        backtest_rows=rows,
                        metadata={
                            "model_name": name,
                            "strategy": strategy,
                            "horizons": horizons,
                            "variant": var_count,
                        }
                    )

            vprint(f"  OK in {time.time()-_iter_start:.2f}s")

            # Save under members
            run_suffix = f"{name}-{iter_idx:03d}-v{var_count:02d}-{time.strftime('%H%M%S')}"
            om = OutputManager(base_dir=os.path.join(group.run_dir, "members"), run_id=run_suffix)
            om.save_backtest_csv(rows)
            om.save_metrics_csv(metrics_by_h)

            # Compute burn-in
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
    vprint(f"[Cache] Hits: {cache_hits}, Misses: {cache_misses}, Hit Rate: {cache_hits/(cache_hits+cache_misses)*100:.1f}%")

    # Write comparison outputs
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

    # HTML report
    report_dir = os.path.join(group.run_dir, "report")
    os.makedirs(report_dir, exist_ok=True)
    html_doc = generate_comparison_report_html(
        title=f"All Models Comparison — {batch_id}", metrics_rows=summary_rows, horizons=all_h
    )
    with open(os.path.join(report_dir, "index.html"), "w") as f:
        f.write(html_doc)

    print(f"All-model run complete. Summary: {csv_path}\nReport: {os.path.join(report_dir, 'index.html')}")


def _run_predict_cached(recipe, frame, target_id, freq, out_dir, verbose):
    """Run prediction mode with cached models."""

    def vprint(msg):
        if verbose:
            print(msg)

    from run import _advance_date_safe, format_ymd

    model_name = recipe.get("model", {}).get("name")

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

    # Discover plugins
    plugins = discover_plugins("models")

    # Build features at the last available origin
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
    as_of_date = parse_ymd(recipe.get("as_of_date")) if recipe.get("as_of_date") else None
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


if __name__ == "__main__":
    main()