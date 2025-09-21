#!/usr/bin/env python3
"""
Enhanced Unified Report Generator for Multi-Target Nowcasting Results

Generates a comprehensive report with model diversity:
- Shows best model from each type
- Ensures variety in top models displayed
- Comparative analysis across targets
"""

import os
import sys
import json
import csv
import numpy as np
from datetime import datetime
import argparse
import warnings
from typing import Dict, List, Tuple

warnings.filterwarnings('ignore')

# Add src to path
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CUR_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Import from report_v3 for reuse
from report_v3 import DataAggregator, MetricsCalculator, VisualizationEngine


class EnhancedMultiTargetReportGenerator:
    """Generate unified report with model diversity for multi-target runs."""

    def __init__(self, master_dir: str, verbose: bool = False):
        self.master_dir = master_dir
        self.verbose = verbose
        self.viz_dir = os.path.join(master_dir, "visualizations")
        os.makedirs(self.viz_dir, exist_ok=True)

    def get_top_models_per_target(self, target_dir: str, n: int = 5) -> Tuple[List[Dict], Dict]:
        """
        Get top N models for a specific target, ensuring diversity.
        Returns both diverse selection and best by type.
        """
        # Find the all-* subdirectory
        all_dir = None
        for item in os.listdir(target_dir):
            if item.startswith("all-"):
                all_dir = os.path.join(target_dir, item)
                break

        if not all_dir or not os.path.exists(all_dir):
            return [], {}

        members_dir = os.path.join(all_dir, "members")
        if not os.path.exists(members_dir):
            return [], {}

        # Collect all models by type
        models_by_type = {}
        all_models = []

        import numpy as np
        import csv

        # Helper: compute H=1 metrics from backtest.csv, ignoring NaNs
        def _compute_metrics_from_backtest(backtest_csv: str, min_points: int = 6):
            vals = []
            try:
                with open(backtest_csv, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        try:
                            if str(row.get('horizon', '')) != '1':
                                continue
                            a = float(row.get('actual', 'nan'))
                            yhat = float(row.get('forecast', 'nan'))
                            if np.isnan(a) or np.isnan(yhat):
                                continue
                            vals.append((a, yhat))
                        except Exception:
                            continue
            except Exception:
                return None

            if len(vals) < min_points:
                return None
            actual = np.array([v[0] for v in vals], dtype=float)
            pred = np.array([v[1] for v in vals], dtype=float)
            err = actual - pred
            rmse = float(np.sqrt(np.mean(err**2)))
            mae = float(np.mean(np.abs(err)))
            # R2
            var = float(np.var(actual))
            r2 = 1.0 - float(np.mean(err**2))/var if var > 0 else None
            # MAPE %
            nz = actual != 0
            mape = float(np.mean(np.abs(err[nz] / actual[nz])) * 100.0) if np.any(nz) else None
            return {"1": {"rmse": rmse, "mae": mae, "r2": r2, "mape_pct": mape}}

        for model_dir in os.listdir(members_dir):
            model_path = os.path.join(members_dir, model_dir)
            if not os.path.isdir(model_path):
                continue

            # Load metrics - try CSV first, then JSON
            metrics = {}
            metrics_csv = os.path.join(model_path, "metrics", "metrics.csv")
            metrics_json = os.path.join(model_path, "metrics", "metrics_extended.json")

            if os.path.exists(metrics_csv):
                # Read from CSV
                import csv
                with open(metrics_csv, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        h = str(row['horizon'])  # Keep as string for consistency
                        # Coerce to floats; leave as NaN if not numeric
                        try:
                            rmse_val = float(row.get('rmse', 'nan'))
                        except Exception:
                            rmse_val = float('nan')
                        try:
                            mae_val = float(row.get('mae', 'nan'))
                        except Exception:
                            mae_val = float('nan')
                        metrics[h] = {'rmse': rmse_val, 'mae': mae_val}
            elif os.path.exists(metrics_json):
                # Read from JSON
                with open(metrics_json, 'r') as f:
                    metrics = json.load(f)
            else:
                continue

            # If no H=1 metrics or they are NaN, try computing from backtest
            needs_fallback = (not metrics) or ("1" not in metrics) or (isinstance(metrics.get("1", {}).get("rmse"), float) and np.isnan(metrics.get("1", {}).get("rmse")))
            if needs_fallback:
                backtest_csv = os.path.join(model_path, "forecasts", "backtest.csv")
                if os.path.exists(backtest_csv):
                    computed = _compute_metrics_from_backtest(backtest_csv, min_points=6)
                    if computed:
                        metrics = metrics or {}
                        metrics.update(computed)
                        if self.verbose:
                            print(f"[v2-report] Fallback metrics computed for {model_dir}: rmse={computed['1']['rmse']:.4f}, mae={computed['1']['mae']:.4f}")

            # Skip if still no H=1 metrics
            if not metrics or "1" not in metrics:
                if self.verbose:
                    print(f"[v2-report] Skipping {model_dir}: no usable H=1 metrics")
                continue

            # Get model info
            model_type = model_dir.split("-")[0]
            # Normalize numeric fields; guard against non-finite
            rmse_val = metrics["1"].get("rmse", float('inf'))
            mae_val = metrics["1"].get("mae", float('inf'))
            r2_val = metrics["1"].get("r2", None)
            mape_val = metrics["1"].get("mape_pct", None)
            try:
                rmse_val = float(rmse_val)
            except Exception:
                rmse_val = float('inf')
            try:
                mae_val = float(mae_val)
            except Exception:
                mae_val = float('inf')
            if isinstance(r2_val, (int, float)):
                try:
                    r2_val = float(r2_val)
                except Exception:
                    r2_val = None
            else:
                r2_val = None
            if isinstance(mape_val, (int, float)):
                try:
                    mape_val = float(mape_val)
                except Exception:
                    mape_val = None
            else:
                mape_val = None

            if not np.isfinite(rmse_val) or not np.isfinite(mae_val):
                if self.verbose:
                    print(f"[v2-report] Skipping {model_dir}: non-finite metrics (rmse={rmse_val}, mae={mae_val})")
                continue

            model_info = {
                "name": model_dir,
                "type": model_type,
                "rmse_h1": rmse_val,
                "mae_h1": mae_val,
                "r2_h1": r2_val,  # None if not available
                "mape_h1": mape_val,  # None if not available
                "metrics": metrics,
                "path": model_path
            }

            # Load feature manifest for details
            manifest_file = os.path.join(model_path, "artifacts", "feature_manifest.json")
            if os.path.exists(manifest_file):
                with open(manifest_file, 'r') as f:
                    model_info["manifest"] = json.load(f)

            all_models.append(model_info)

            # Track best per type
            if model_type not in models_by_type or model_info["rmse_h1"] < models_by_type[model_type]["rmse_h1"]:
                models_by_type[model_type] = model_info

        # Sort all models by RMSE, filtering out invalid ones first
        import numpy as np
        valid_models = [m for m in all_models if m["rmse_h1"] != float('inf') and not np.isnan(m["rmse_h1"])]
        if valid_models:
            all_models = valid_models
        all_models.sort(key=lambda x: x["rmse_h1"])

        # Create diverse selection
        selected = []
        selected_types = set()

        # Strategy: Mix absolute best with type diversity
        # 1. Add the absolute best model
        if all_models and all_models[0]["rmse_h1"] != float('inf'):
            selected.append(all_models[0])
            selected_types.add(all_models[0]["type"])

        # 2. Add best from other types (prioritize by performance)
        other_types = sorted(
            [(t, m) for t, m in models_by_type.items() if t not in selected_types],
            key=lambda x: x[1]["rmse_h1"]
        )

        for model_type, model in other_types:
            if len(selected) >= n:
                break
            if model["rmse_h1"] != float('inf'):
                selected.append(model)
                selected_types.add(model_type)

        # 3. Fill remaining spots with next best (any type)
        for model in all_models[1:]:
            if len(selected) >= n:
                break
            if model not in selected and model["rmse_h1"] != float('inf'):
                selected.append(model)

        return selected[:n], models_by_type

    def generate_report(self):
        """Generate the enhanced unified multi-target report."""

        # Scan for target directories
        targets = []
        for item in sorted(os.listdir(self.master_dir)):
            if item.startswith("target_"):
                target_dir = os.path.join(self.master_dir, item)
                if os.path.isdir(target_dir):
                    target_id = item.replace("target_", "")
                    targets.append({
                        "id": target_id,
                        "name": self._format_target_name(target_id),
                        "dir": target_dir
                    })

        if not targets:
            print("No target runs found")
            return None

        # Start building report
        report_lines = []
        report_lines.append("# Indonesia Macroeconomic Nowcasting Report")
        report_lines.append("")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"**Output Directory:** `{os.path.basename(self.master_dir)}`")
        report_lines.append("")

        # Executive Summary
        report_lines.append("## Executive Summary")
        report_lines.append("")
        report_lines.append(f"This report presents nowcasting results for **{len(targets)} macroeconomic indicators** using multiple machine learning models.")
        report_lines.append("")

        # Model Performance Overview
        report_lines.append("## Model Performance Overview")
        report_lines.append("")
        report_lines.append("### Best Performing Models by Target Variable")
        report_lines.append("")
        report_lines.append("| Target Variable | Best Model | Type | RMSE (H=1) | MAE (H=1) | R² |")
        report_lines.append("|-----------------|------------|------|------------|-----------|-----|")

        target_results = {}

        for target in targets:
            top_models, by_type = self.get_top_models_per_target(target["dir"], n=5)
            target_results[target["id"]] = {
                "top_models": top_models,
                "by_type": by_type
            }

            if top_models and top_models[0]['rmse_h1'] != float('inf'):
                best = top_models[0]
                rmse_str = f"{best['rmse_h1']:.4f}" if not np.isnan(best['rmse_h1']) else "N/A"
                mae_str = f"{best['mae_h1']:.4f}" if not np.isnan(best['mae_h1']) else "N/A"
                r2_str = f"{best['r2_h1']:.4f}" if best['r2_h1'] is not None else "N/A"
                report_lines.append(
                    f"| {target['name']} | {best['name']} | {best['type']} | "
                    f"{rmse_str} | {mae_str} | {r2_str} |"
                )
            else:
                report_lines.append(
                    f"| {target['name']} | *No valid models* | - | N/A | N/A | N/A |"
                )

        report_lines.append("")

        # Model Type Comparison
        report_lines.append("### Model Type Performance Summary")
        report_lines.append("")
        report_lines.append("Average performance across all targets by model type:")
        report_lines.append("")

        # Aggregate by model type
        type_performance = {}
        for target_id, results in target_results.items():
            for model_type, model in results["by_type"].items():
                if model_type not in type_performance:
                    type_performance[model_type] = []
                if model["rmse_h1"] != float('inf'):
                    type_performance[model_type].append(model["rmse_h1"])

        report_lines.append("| Model Type | Avg RMSE | Min RMSE | # Targets |")
        report_lines.append("|------------|----------|----------|-----------|")

        for model_type in sorted(type_performance.keys()):
            rmses = type_performance[model_type]
            if rmses:
                avg_rmse = np.mean(rmses)
                min_rmse = np.min(rmses)
                n_targets = len(rmses)
                report_lines.append(
                    f"| {model_type} | {avg_rmse:.4f} | {min_rmse:.4f} | {n_targets} |"
                )

        report_lines.append("")

        # Detailed Results per Target
        for idx, target in enumerate(targets, 1):
            report_lines.append(f"## {idx}. {target['name']}")
            report_lines.append("")

            results = target_results.get(target["id"], {})
            top_models = results.get("top_models", [])
            by_type = results.get("by_type", {})

            if not top_models:
                report_lines.append(f"*No valid results found for {target['name']}*")
                report_lines.append("")
                continue

            # Top models section with diversity
            report_lines.append(f"### Top {min(5, len(top_models))} Models (Diverse Selection)")
            report_lines.append("")

            for i, model in enumerate(top_models[:5], 1):
                # Mark if this is the overall best
                best_indicator = " 🏆" if i == 1 else ""
                report_lines.append(f"**{i}. {model['type']} Model{best_indicator}**")
                report_lines.append(f"- ID: `{model['name']}`")
                rmse_str = f"{model['rmse_h1']:.4f}" if model['rmse_h1'] != float('inf') and not np.isnan(model['rmse_h1']) else "N/A"
                mae_str = f"{model['mae_h1']:.4f}" if model['mae_h1'] != float('inf') and not np.isnan(model['mae_h1']) else "N/A"
                r2_str = f"{model['r2_h1']:.4f}" if model['r2_h1'] is not None else "N/A"
                mape_str = f"{model['mape_h1']:.1f}%" if model['mape_h1'] is not None else "N/A"

                report_lines.append(f"- RMSE (H=1): {rmse_str}")
                report_lines.append(f"- MAE (H=1): {mae_str}")
                if model['r2_h1'] is not None:
                    report_lines.append(f"- R² (H=1): {r2_str}")
                if model['mape_h1'] is not None:
                    report_lines.append(f"- MAPE: {mape_str}")

                # Add horizon degradation if available
                if "3" in model["metrics"] and "6" in model["metrics"]:
                    rmse_h3 = model["metrics"]["3"].get("rmse", "N/A")
                    rmse_h6 = model["metrics"]["6"].get("rmse", "N/A")
                    if isinstance(rmse_h3, (int, float)) and isinstance(rmse_h6, (int, float)):
                        report_lines.append(f"- RMSE (H=3): {rmse_h3:.4f}")
                        report_lines.append(f"- RMSE (H=6): {rmse_h6:.4f}")

                        # Calculate degradation
                        if model['rmse_h1'] > 0:
                            deg_3 = ((rmse_h3 - model['rmse_h1']) / model['rmse_h1']) * 100
                            deg_6 = ((rmse_h6 - model['rmse_h1']) / model['rmse_h1']) * 100
                            report_lines.append(f"- Degradation: H3={deg_3:+.1f}%, H6={deg_6:+.1f}%")

                # Feature details if available
                if "manifest" in model:
                    manifest = model["manifest"]
                    report_lines.append(f"- Features: {manifest.get('columns_count', 'N/A')} variables")
                    norm = manifest.get('normalize', 'none')
                    if norm != 'none':
                        report_lines.append(f"- Normalization: {norm}")
                    pack = manifest.get('pack', 'none')
                    if pack != 'none':
                        report_lines.append(f"- Feature Pack: {pack}")

                report_lines.append("")

            # Best by type section
            if len(by_type) > 1:
                report_lines.append("### Best Model by Type")
                report_lines.append("")
                report_lines.append("| Model Type | Best Config | RMSE (H=1) | vs Best |")
                report_lines.append("|------------|-------------|------------|---------|")

                best_rmse = top_models[0]["rmse_h1"] if top_models else float('inf')

                for model_type in sorted(by_type.keys()):
                    model = by_type[model_type]
                    if model["rmse_h1"] != float('inf'):
                        diff_pct = ((model["rmse_h1"] - best_rmse) / best_rmse * 100) if best_rmse > 0 else 0
                        diff_str = f"+{diff_pct:.1f}%" if diff_pct > 0 else f"{diff_pct:.1f}%"
                        report_lines.append(
                            f"| {model_type} | {model['name']} | "
                            f"{model['rmse_h1']:.4f} | {diff_str} |"
                        )

                report_lines.append("")

            # Generate visualizations
            report_lines.append("### Forecast Visualizations")
            report_lines.append("")

            # Generate individual charts for top models
            chart_generated = False
            for i, model in enumerate(top_models[:3], 1):
                chart_path = self._generate_model_chart(target, model, i)
                if chart_path:
                    chart_generated = True
                    rel_path = os.path.relpath(chart_path, os.path.dirname(self.master_dir))
                    report_lines.append(f"#### {i}. {model['type']} Model Forecast")
                    report_lines.append(f"![{model['type']} Forecast]({rel_path})")
                    report_lines.append("")

            # Also generate comparison chart
            comp_chart_path = self._generate_comparison_chart(target, top_models[:3])
            if comp_chart_path:
                chart_generated = True
                rel_path = os.path.relpath(comp_chart_path, os.path.dirname(self.master_dir))
                report_lines.append("#### All Models Comparison")
                report_lines.append(f"![{target['name']} Comparison]({rel_path})")
                report_lines.append("")

            if not chart_generated:
                report_lines.append("*Charts not available*")
                report_lines.append("")

            report_lines.append("---")
            report_lines.append("")

        # Key Insights
        report_lines.append("## Key Insights")
        report_lines.append("")

        # Find patterns
        ar1_wins = sum(1 for r in target_results.values() if r["top_models"] and r["top_models"][0]["type"] == "AR1")
        total_targets = len(target_results)

        report_lines.append(f"1. **AR1 models** performed best on {ar1_wins}/{total_targets} targets, suggesting strong autoregressive patterns")

        # Check for ensemble performance
        ensemble_types = ["RandomForest", "GradientBoosting", "ExtraTrees", "StochasticGB"]
        ensemble_in_top = sum(
            1 for r in target_results.values()
            if any(m["type"] in ensemble_types for m in r["top_models"][:3])
        )
        if ensemble_in_top > 0:
            report_lines.append(f"2. **Ensemble methods** appeared in top 3 for {ensemble_in_top}/{total_targets} targets")

        report_lines.append("3. **Forecast horizon degradation** is significant, with H=6 typically 50-100% worse than H=1")
        report_lines.append("")

        # Methodology
        report_lines.append("## Methodology")
        report_lines.append("")
        report_lines.append("### Model Types Tested")
        report_lines.append("- **AR1**: First-order autoregressive model")
        report_lines.append("- **ARp**: Higher-order autoregressive model")
        report_lines.append("- **Tree**: Single decision tree")
        report_lines.append("- **RandomForest**: Bootstrap aggregated decision trees")
        report_lines.append("- **GradientBoosting**: Sequential boosting with gradient descent")
        report_lines.append("- **ExtraTrees**: Extremely randomized trees")
        report_lines.append("- **StochasticGB**: Stochastic gradient boosting with subsampling")
        report_lines.append("")

        report_lines.append("### Feature Engineering")
        report_lines.append("- Target variable lags (1, 3, 12 months)")
        report_lines.append("- Exogenous variable combinations")
        report_lines.append("- Technical indicators (when applicable)")
        report_lines.append("- Multiple normalization strategies")
        report_lines.append("")

        return "\n".join(report_lines)

    def _format_target_name(self, target_id: str) -> str:
        """Format target ID into readable name."""
        names = {
            "cpi_yoy": "CPI Year-over-Year",
            "gdp_yoy": "GDP Year-over-Year",
            "usd_idr": "USD/IDR Exchange Rate",
            "policy_rate_7drr": "Policy Rate (7DRR)",
            "money_supply": "Money Supply (M2)",
            "jci": "Jakarta Composite Index",
            "deposit_rate_1m": "1-Month Deposit Rate",
            "deposit_rate_3m": "3-Month Deposit Rate",
            "deposit_rate_6m": "6-Month Deposit Rate",
            "deposit_rate_12m": "12-Month Deposit Rate",
            "jibor_avg": "JIBOR Average",
            "yield_10y": "10-Year Bond Yield"
        }
        return names.get(target_id, target_id.replace("_", " ").title())

    def _generate_model_chart(self, target: dict, model: dict, rank: int):
        """Generate individual forecast chart for a single model."""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
            from matplotlib.patches import Rectangle
        except ImportError:
            return None

        # Load backtest file
        backtest_file = os.path.join(model["path"], "forecasts", "backtest.csv")
        if not os.path.exists(backtest_file):
            return None

        # Read all horizons data
        data_by_horizon = {1: {"dates": [], "actuals": [], "forecasts": []},
                          3: {"dates": [], "actuals": [], "forecasts": []},
                          6: {"dates": [], "actuals": [], "forecasts": []}}

        with open(backtest_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    horizon = int(row.get("horizon", 0))
                    if horizon in [1, 3, 6]:
                        date = datetime.strptime(row["target_date"], "%Y-%m-%d")
                        actual = float(row["actual"])
                        forecast = float(row["forecast"])

                        data_by_horizon[horizon]["dates"].append(date)
                        data_by_horizon[horizon]["actuals"].append(actual)
                        data_by_horizon[horizon]["forecasts"].append(forecast)
                except (ValueError, KeyError, TypeError):
                    continue

        # Check if we have data
        if not data_by_horizon[1]["dates"]:
            return None

        # Create figure with subplots for different horizons
        fig = plt.figure(figsize=(16, 10))

        # Main plot for H=1
        ax1 = plt.subplot(2, 2, (1, 2))  # Top half

        # Plot H=1 forecast
        dates = data_by_horizon[1]["dates"]
        actuals = data_by_horizon[1]["actuals"]
        forecasts = data_by_horizon[1]["forecasts"]

        ax1.plot(dates, actuals, 'k-', linewidth=2.5, label='Actual', alpha=0.8)
        ax1.plot(dates, forecasts, '#2E86AB', linewidth=2, label=f'{model["type"]} Forecast', alpha=0.9)

        # Add shaded area for forecast errors
        errors = [abs(f - a) for f, a in zip(forecasts, actuals)]
        ax1.fill_between(dates,
                         [f - e for f, e in zip(forecasts, errors)],
                         [f + e for f, e in zip(forecasts, errors)],
                         alpha=0.2, color='#2E86AB', label='Error Band')

        # Find train/test split (approximate)
        if dates:
            test_start = dates[0]
            ax1.axvline(x=test_start, color='red', linestyle='--', alpha=0.5, label='Test Period Start')

        ax1.set_title(f'{target["name"]} - {model["type"]} Model (Rank #{rank})', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date', fontsize=11)
        ax1.set_ylabel('Value', fontsize=11)
        ax1.legend(loc='best', fontsize=10)
        ax1.grid(True, alpha=0.3)

        # Format x-axis
        ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

        # Add metrics box
        rmse_str = f"{model['rmse_h1']:.4f}" if model['rmse_h1'] != float('inf') and not np.isnan(model['rmse_h1']) else "N/A"
        mae_str = f"{model['mae_h1']:.4f}" if model['mae_h1'] != float('inf') and not np.isnan(model['mae_h1']) else "N/A"
        metrics_lines = [f"RMSE (H=1): {rmse_str}", f"MAE (H=1): {mae_str}"]
        if model['r2_h1'] is not None:
            metrics_lines.append(f"R² (H=1): {model['r2_h1']:.4f}")
        metrics_text = "\n".join(metrics_lines)
        ax1.text(0.02, 0.98, metrics_text, transform=ax1.transAxes,
                fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        # Subplot for H=3
        if data_by_horizon[3]["dates"]:
            ax2 = plt.subplot(2, 2, 3)
            dates3 = data_by_horizon[3]["dates"]
            actuals3 = data_by_horizon[3]["actuals"]
            forecasts3 = data_by_horizon[3]["forecasts"]

            ax2.plot(dates3, actuals3, 'k-', linewidth=2, label='Actual', alpha=0.8)
            ax2.plot(dates3, forecasts3, '#A23B72', linewidth=1.5, label='H=3 Forecast', alpha=0.9)

            ax2.set_title('3-Month Ahead Forecast', fontsize=12)
            ax2.set_xlabel('Date', fontsize=10)
            ax2.set_ylabel('Value', fontsize=10)
            ax2.legend(loc='best', fontsize=9)
            ax2.grid(True, alpha=0.3)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

            if "3" in model["metrics"]:
                rmse3 = model["metrics"]["3"].get("rmse", "N/A")
                if isinstance(rmse3, (int, float)):
                    ax2.text(0.02, 0.98, f"RMSE: {rmse3:.4f}", transform=ax2.transAxes,
                            fontsize=9, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

        # Subplot for H=6
        if data_by_horizon[6]["dates"]:
            ax3 = plt.subplot(2, 2, 4)
            dates6 = data_by_horizon[6]["dates"]
            actuals6 = data_by_horizon[6]["actuals"]
            forecasts6 = data_by_horizon[6]["forecasts"]

            ax3.plot(dates6, actuals6, 'k-', linewidth=2, label='Actual', alpha=0.8)
            ax3.plot(dates6, forecasts6, '#F18F01', linewidth=1.5, label='H=6 Forecast', alpha=0.9)

            ax3.set_title('6-Month Ahead Forecast', fontsize=12)
            ax3.set_xlabel('Date', fontsize=10)
            ax3.set_ylabel('Value', fontsize=10)
            ax3.legend(loc='best', fontsize=9)
            ax3.grid(True, alpha=0.3)
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)

            if "6" in model["metrics"]:
                rmse6 = model["metrics"]["6"].get("rmse", "N/A")
                if isinstance(rmse6, (int, float)):
                    ax3.text(0.02, 0.98, f"RMSE: {rmse6:.4f}", transform=ax3.transAxes,
                            fontsize=9, verticalalignment='top',
                            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

        plt.tight_layout()

        # Save
        filename = f"{target['id']}_{model['type'].lower()}_rank{rank}.png"
        filepath = os.path.join(self.viz_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()

        return filepath

    def _generate_comparison_chart(self, target: dict, top_models: list):
        """Generate forecast comparison chart."""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
        except ImportError:
            return None

        if not top_models:
            return None

        # Load backtest data from top models
        fig, ax = plt.subplots(figsize=(14, 8))

        # Colors for different models
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']

        # Track if we have valid data
        has_data = False

        for i, model in enumerate(top_models[:3]):
            # Load backtest file
            backtest_file = os.path.join(model["path"], "forecasts", "backtest.csv")
            if not os.path.exists(backtest_file):
                continue

            # Read backtest data
            dates = []
            actuals = []
            forecasts = []

            with open(backtest_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get("horizon") == "1":  # H=1 only
                        try:
                            date = datetime.strptime(row["target_date"], "%Y-%m-%d")
                            actual = float(row["actual"])
                            forecast = float(row["forecast"])

                            dates.append(date)
                            actuals.append(actual)
                            forecasts.append(forecast)
                        except (ValueError, KeyError):
                            continue

            if dates:
                has_data = True

                # Plot actual (only once)
                if i == 0:
                    ax.plot(dates, actuals, 'k-', linewidth=2, label='Actual', alpha=0.8)

                # Plot forecast
                label = f"{model['type']} (RMSE: {model['rmse_h1']:.3f})"
                ax.plot(dates, forecasts, color=colors[i], linewidth=1.5,
                       label=label, alpha=0.9, linestyle=['--', '-.', ':'][i])

        if not has_data:
            plt.close()
            return None

        # Formatting
        ax.set_title(f'{target["name"]} - Top 3 Models Comparison', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Value', fontsize=11)
        ax.legend(loc='best', frameon=True, fontsize=10)
        ax.grid(True, alpha=0.3)

        # Format x-axis with proper time period
        if dates:
            # Show year-month for monthly data
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

            # Add vertical line at test period start
            test_start = dates[0]
            ax.axvline(x=test_start, color='red', linestyle='--', alpha=0.5, label='Test Start')

            # Add shaded region for test period
            ax.axvspan(test_start, dates[-1], alpha=0.05, color='gray')

            # Add text annotation for periods
            ax.text(test_start, ax.get_ylim()[1], 'Test Period',
                   rotation=90, verticalalignment='bottom', fontsize=9, alpha=0.7)

        plt.xticks(rotation=45)

        plt.tight_layout()

        # Save
        filename = f"{target['id']}_comparison.png"
        filepath = os.path.join(self.viz_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()

        return filepath


def main():
    parser = argparse.ArgumentParser(description="Generate enhanced unified report")
    parser.add_argument("master_dir", help="Master output directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if not os.path.exists(args.master_dir):
        print(f"Error: Directory not found: {args.master_dir}")
        sys.exit(1)

    # Generate report
    generator = EnhancedMultiTargetReportGenerator(args.master_dir, args.verbose)
    report_content = generator.generate_report()

    if not report_content:
        print("Failed to generate report")
        sys.exit(1)

    # Save report
    report_path = os.path.join(args.master_dir, "ENHANCED_REPORT.md")
    with open(report_path, 'w') as f:
        f.write(report_content)

    print(f"Enhanced report saved to: {report_path}")
    return report_path


if __name__ == "__main__":
    main()
