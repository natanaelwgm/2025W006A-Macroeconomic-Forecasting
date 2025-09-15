#!/usr/bin/env python3
"""
Advanced Report Generator for Nowcasting Results

Generates comprehensive markdown and HTML reports with:
- Top model identification
- Performance visualizations
- Advanced metrics
- Auto-generated insights
- Caching for fast regeneration
"""

import os
import sys
import json
import csv
import hashlib
import time
import argparse
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import numpy as np
from pathlib import Path
import warnings

# Suppress numpy warnings for divide by zero in correlation calculations
warnings.filterwarnings('ignore', category=RuntimeWarning, module='numpy')

# Add src to path
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CUR_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)


class DataAggregator:
    """Aggregates data from all model runs in a batch."""

    def __init__(self, run_dir: str, verbose: bool = False):
        self.run_dir = run_dir
        self.verbose = verbose
        self.members_dir = os.path.join(run_dir, "members")
        self.summary_csv = os.path.join(run_dir, "metrics_summary.csv")

    def load_all_members(self) -> Dict[str, Dict]:
        """Load all member results."""
        if self.verbose:
            print(f"Loading members from {self.members_dir}")

        results = {}

        # Check if members directory exists
        if not os.path.exists(self.members_dir):
            print(f"Warning: No members directory found at {self.members_dir}")
            return results

        # Iterate through each member
        for member_name in sorted(os.listdir(self.members_dir)):
            member_path = os.path.join(self.members_dir, member_name)
            if not os.path.isdir(member_path):
                continue

            # Parse member name to extract model info
            parts = member_name.split("-")
            model_name = parts[0] if parts else "Unknown"

            # Load backtest results
            backtest_path = os.path.join(member_path, "forecasts", "backtest.csv")
            backtest_data = self._load_csv(backtest_path)

            # Load metrics
            metrics_path = os.path.join(member_path, "metrics", "metrics.csv")
            metrics_data = self._load_csv(metrics_path)

            # Load feature manifest if exists
            manifest_path = os.path.join(member_path, "artifacts", "feature_manifest.json")
            manifest_data = self._load_json(manifest_path)

            results[member_name] = {
                "model_name": model_name,
                "backtest": backtest_data,
                "metrics": metrics_data,
                "manifest": manifest_data,
                "path": member_path
            }

        if self.verbose:
            print(f"Loaded {len(results)} members")

        return results

    def _load_csv(self, path: str) -> List[Dict]:
        """Load CSV file as list of dicts."""
        if not os.path.exists(path):
            return []

        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            if self.verbose:
                print(f"Error loading {path}: {e}")
            return []

    def _load_json(self, path: str) -> Dict:
        """Load JSON file."""
        if not os.path.exists(path):
            return {}

        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            if self.verbose:
                print(f"Error loading {path}: {e}")
            return {}

    def get_top_n_per_target(self, results: Dict, n: int = 3, metric: str = "rmse", horizon: int = 1) -> Dict[str, List]:
        """Get top N models per target variable."""
        # Try to extract target from lineage or recipe
        target = "cpi_yoy"  # Default for your current run

        # Check if we can find lineage.json to get actual target
        lineage_path = os.path.join(self.run_dir, "lineage.json")
        if os.path.exists(lineage_path):
            try:
                with open(lineage_path, 'r') as f:
                    lineage = json.load(f)
                    target = lineage.get("target_id", "cpi_yoy")
            except:
                pass

        # Group all models for this target
        targets = {target: []}

        for member_name, data in results.items():
            if not data["metrics"]:
                continue

            # Get metric value for horizon - handle both string and int
            metric_value = None
            for m in data["metrics"]:
                h = m.get("horizon")
                # Convert horizon to int for comparison
                try:
                    if int(h) == horizon:
                        metric_value = float(m.get(metric, float('inf')))
                        break
                except (ValueError, TypeError):
                    continue

            if metric_value is not None and metric_value != float('inf'):
                # Parse member name to get variant info
                parts = member_name.split("-")
                variant = parts[2] if len(parts) > 2 else "v00"

                targets[target].append({
                    "member_name": member_name,
                    "model_name": data["model_name"],
                    "variant": variant,
                    "metric_value": metric_value,
                    "data": data
                })

        # Sort and get top N for each target
        top_models = {}
        for target, models in targets.items():
            sorted_models = sorted(models, key=lambda x: x["metric_value"])
            top_models[target] = sorted_models[:n]

        return top_models


class MetricsCalculator:
    """Calculate advanced metrics from forecast and actual values."""

    def calculate_all_metrics(self, results: Dict) -> Dict:
        """Calculate comprehensive metrics for all models."""
        enriched = {}

        for member_name, data in results.items():
            if not data["backtest"]:
                enriched[member_name] = data
                continue

            # Parse backtest data
            backtest = data["backtest"]

            # Group by horizon
            by_horizon = {}
            for row in backtest:
                h = row.get("horizon", "1")
                if h not in by_horizon:
                    by_horizon[h] = {"forecast": [], "actual": [], "dates": []}

                try:
                    by_horizon[h]["forecast"].append(float(row.get("forecast", 0)))
                    by_horizon[h]["actual"].append(float(row.get("actual", 0)))
                    by_horizon[h]["dates"].append(row.get("target_date", ""))
                except (ValueError, TypeError):
                    continue

            # Calculate metrics per horizon
            extended_metrics = {}
            for h, values in by_horizon.items():
                if len(values["forecast"]) > 0 and len(values["actual"]) > 0:
                    extended_metrics[h] = self._calculate_metrics(
                        np.array(values["forecast"]),
                        np.array(values["actual"])
                    )
                    extended_metrics[h]["dates"] = values["dates"]
                    extended_metrics[h]["forecast"] = values["forecast"]
                    extended_metrics[h]["actual"] = values["actual"]

            enriched[member_name] = {
                **data,
                "extended_metrics": extended_metrics
            }

        return enriched

    def _calculate_metrics(self, forecast: np.ndarray, actual: np.ndarray) -> Dict:
        """Calculate comprehensive metrics."""
        metrics = {}

        # Basic metrics
        errors = actual - forecast
        metrics["rmse"] = np.sqrt(np.mean(errors ** 2))
        metrics["mae"] = np.mean(np.abs(errors))
        metrics["bias"] = np.mean(errors)

        # MAPE (handle zeros)
        non_zero = actual != 0
        if np.any(non_zero):
            metrics["mape"] = np.mean(np.abs(errors[non_zero] / actual[non_zero])) * 100
        else:
            metrics["mape"] = np.nan

        # Correlation
        if len(forecast) > 1:
            try:
                corr = np.corrcoef(forecast, actual)[0, 1]
                metrics["correlation"] = corr if not np.isnan(corr) else 0.0
            except:
                metrics["correlation"] = 0.0

            # Directional accuracy
            if len(forecast) > 1:
                forecast_dir = np.diff(forecast) > 0
                actual_dir = np.diff(actual) > 0
                metrics["direction_accuracy"] = np.mean(forecast_dir == actual_dir) * 100

            # First difference correlation
            forecast_diff = np.diff(forecast)
            actual_diff = np.diff(actual)
            if len(forecast_diff) > 1:
                try:
                    diff_corr = np.corrcoef(forecast_diff, actual_diff)[0, 1]
                    metrics["diff_correlation"] = diff_corr if not np.isnan(diff_corr) else 0.0
                except:
                    metrics["diff_correlation"] = 0.0

        # Theil's U
        if len(forecast) > 1:
            naive_forecast = actual[:-1]  # Use previous value as naive forecast
            naive_errors = actual[1:] - naive_forecast
            naive_rmse = np.sqrt(np.mean(naive_errors ** 2))
            if naive_rmse > 0:
                metrics["theil_u"] = metrics["rmse"] / naive_rmse

        return metrics


class VisualizationEngine:
    """Generate visualizations for the report."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.viz_dir = os.path.join(output_dir, "visualizations")
        os.makedirs(self.viz_dir, exist_ok=True)

    def generate_all_charts(self, top_models: Dict, all_results: Dict) -> Dict[str, str]:
        """Generate all visualizations."""
        charts = {}

        # Import matplotlib only when needed
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            from matplotlib.figure import Figure
        except ImportError:
            print("Warning: matplotlib not installed. Skipping visualizations.")
            return charts

        # Generate charts for each target
        for target, models in top_models.items():
            # Get top 3 DIFFERENT models for visualization
            unique_models = []
            seen_model_types = set()
            for m in models:
                if m["model_name"] not in seen_model_types:
                    unique_models.append(m)
                    seen_model_types.add(m["model_name"])
                    if len(unique_models) >= 3:
                        break

            # Top 3 forecast comparison
            chart_path = self._generate_forecast_comparison(target, unique_models[:3], plt)
            if chart_path:
                charts[f"{target}_forecast"] = chart_path

            # Error distribution
            if models:
                chart_path = self._generate_error_distribution(target, models[0], plt)
                if chart_path:
                    charts[f"{target}_errors"] = chart_path

        return charts

    def _generate_forecast_comparison(self, target: str, models: List[Dict], plt) -> Optional[str]:
        """Generate forecast vs actual comparison chart."""
        if not models:
            return None

        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot actual (from first model, since actual is same for all)
        first_model = models[0]["data"]
        if "extended_metrics" in first_model and "1" in first_model["extended_metrics"]:
            metrics = first_model["extended_metrics"]["1"]
            dates = [self._parse_date(d) for d in metrics["dates"]]
            actual = metrics["actual"]

            ax.plot(dates, actual, 'k-', linewidth=2, label='Actual', alpha=0.8)

            # Plot top 3 models
            colors = ['blue', 'green', 'red']
            for i, model in enumerate(models[:3]):
                if "extended_metrics" in model["data"] and "1" in model["data"]["extended_metrics"]:
                    m_metrics = model["data"]["extended_metrics"]["1"]
                    forecast = m_metrics["forecast"]
                    model_label = f"{model['model_name']} (RMSE: {model['metric_value']:.3f})"
                    ax.plot(dates, forecast, colors[i], linewidth=1.5, label=model_label, alpha=0.7)

        ax.set_title(f'Forecast Comparison - {target}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)

        # Format x-axis
        try:
            import matplotlib.dates as mdates
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        except:
            # Fallback if dates formatting fails
            pass
        plt.xticks(rotation=45)

        plt.tight_layout()

        # Save
        filename = f"{target}_forecast_comparison.png"
        filepath = os.path.join(self.viz_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()

        return filepath

    def _generate_error_distribution(self, target: str, model: Dict, plt) -> Optional[str]:
        """Generate error distribution plot."""
        if not model or "extended_metrics" not in model["data"]:
            return None

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Get errors
        if "1" in model["data"]["extended_metrics"]:
            metrics = model["data"]["extended_metrics"]["1"]
            forecast = np.array(metrics["forecast"])
            actual = np.array(metrics["actual"])
            errors = actual - forecast

            # Histogram
            axes[0].hist(errors, bins=20, edgecolor='black', alpha=0.7)
            axes[0].set_title('Error Distribution')
            axes[0].set_xlabel('Error')
            axes[0].set_ylabel('Frequency')
            axes[0].axvline(x=0, color='red', linestyle='--', alpha=0.5)

            # Q-Q plot
            try:
                from scipy import stats
                stats.probplot(errors, dist="norm", plot=axes[1])
                axes[1].set_title('Q-Q Plot')
                axes[1].grid(True, alpha=0.3)
            except ImportError:
                # Fallback if scipy not available
                axes[1].scatter(errors, errors, alpha=0.5)
                axes[1].set_title('Error Scatter')
                axes[1].grid(True, alpha=0.3)

        plt.suptitle(f'Error Analysis - {model["model_name"]} ({target})', fontsize=14, fontweight='bold')
        plt.tight_layout()

        # Save
        filename = f"{target}_error_distribution.png"
        filepath = os.path.join(self.viz_dir, filename)
        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        plt.close()

        return filepath

    def _parse_date(self, date_str: str):
        """Parse date string to datetime."""
        try:
            from datetime import datetime
            return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return date_str


class InsightGenerator:
    """Generate automated insights from results."""

    def analyze(self, results: Dict) -> List[str]:
        """Generate insights from results."""
        insights = []

        # Model performance comparison
        model_scores = {}
        for member_name, data in results.items():
            model = data.get("model_name", "Unknown")
            if "extended_metrics" in data and "1" in data["extended_metrics"]:
                rmse = data["extended_metrics"]["1"].get("rmse", float('inf'))
                if model not in model_scores:
                    model_scores[model] = []
                model_scores[model].append(rmse)

        # Average performance per model type
        model_avg = {}
        for model, scores in model_scores.items():
            if scores:
                model_avg[model] = np.mean(scores)

        if model_avg:
            best_model = min(model_avg, key=model_avg.get)
            worst_model = max(model_avg, key=model_avg.get)

            if best_model != worst_model:
                improvement = ((model_avg[worst_model] - model_avg[best_model]) / model_avg[worst_model]) * 100
                insights.append(f"**{best_model}** models outperform **{worst_model}** by {improvement:.1f}% on average")

        # Feature engineering impact
        normalized_count = 0
        non_normalized_count = 0
        normalized_rmse = []
        non_normalized_rmse = []

        for member_name, data in results.items():
            manifest = data.get("manifest", {})
            if manifest and isinstance(manifest, dict):
                normalize_cfg = manifest.get("normalize", {})
                if isinstance(normalize_cfg, dict) and normalize_cfg.get("method") == "zscore":
                    normalized_count += 1
                    if "extended_metrics" in data and "1" in data["extended_metrics"]:
                        normalized_rmse.append(data["extended_metrics"]["1"].get("rmse", float('inf')))
                else:
                    non_normalized_count += 1
                    if "extended_metrics" in data and "1" in data["extended_metrics"]:
                        non_normalized_rmse.append(data["extended_metrics"]["1"].get("rmse", float('inf')))
            else:
                non_normalized_count += 1
                if "extended_metrics" in data and "1" in data["extended_metrics"]:
                    non_normalized_rmse.append(data["extended_metrics"]["1"].get("rmse", float('inf')))

        if normalized_rmse and non_normalized_rmse:
            norm_avg = np.mean(normalized_rmse)
            non_norm_avg = np.mean(non_normalized_rmse)
            if non_norm_avg > 0:
                impact = ((non_norm_avg - norm_avg) / non_norm_avg) * 100
                if abs(impact) > 5:
                    if impact > 0:
                        insights.append(f"Z-score normalization improves performance by {impact:.1f}% on average")
                    else:
                        insights.append(f"Models without normalization perform {-impact:.1f}% better on average")

        # Horizon analysis
        horizon_rmse = {}
        for member_name, data in results.items():
            if "extended_metrics" in data:
                for h, metrics in data["extended_metrics"].items():
                    if h not in horizon_rmse:
                        horizon_rmse[h] = []
                    horizon_rmse[h].append(metrics.get("rmse", float('inf')))

        if horizon_rmse:
            horizon_avg = {h: np.mean(scores) for h, scores in horizon_rmse.items() if scores}
            if len(horizon_avg) > 1:
                sorted_horizons = sorted(horizon_avg.items(), key=lambda x: int(x[0]))
                if sorted_horizons:
                    best_h = sorted_horizons[0]
                    worst_h = sorted_horizons[-1]
                    degradation = ((worst_h[1] - best_h[1]) / best_h[1]) * 100
                    insights.append(f"Performance degrades by {degradation:.1f}% from {best_h[0]}-step to {worst_h[0]}-step horizon")

        # Directional accuracy
        dir_acc_values = []
        for member_name, data in results.items():
            if "extended_metrics" in data and "1" in data["extended_metrics"]:
                dir_acc = data["extended_metrics"]["1"].get("direction_accuracy")
                if dir_acc is not None:
                    dir_acc_values.append(dir_acc)

        if dir_acc_values:
            avg_dir_acc = np.mean(dir_acc_values)
            insights.append(f"Average directional accuracy across all models: {avg_dir_acc:.1f}%")

        return insights


class MarkdownGenerator:
    """Generate markdown report."""

    def create_report(self, top_models: Dict, charts: Dict, insights: List[str],
                     all_results: Dict, run_dir: str) -> str:
        """Generate comprehensive markdown report."""

        # Start report
        lines = []
        lines.append("# Nowcasting Model Performance Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Run Directory:** `{os.path.basename(run_dir)}`")
        lines.append(f"**Total Models Tested:** {len(all_results)}")
        lines.append("")

        # Executive Summary
        lines.append("## Executive Summary")
        lines.append("")

        if insights:
            lines.append("### Key Insights")
            for insight in insights:
                lines.append(f"- {insight}")
            lines.append("")

        # Overall statistics
        lines.append("### Overall Statistics")
        lines.append("")

        # Count models by type
        model_counts = {}
        for member_name, data in all_results.items():
            model = data.get("model_name", "Unknown")
            model_counts[model] = model_counts.get(model, 0) + 1

        lines.append("| Model Type | Count | Percentage |")
        lines.append("|------------|-------|------------|")
        total = sum(model_counts.values())
        for model, count in sorted(model_counts.items()):
            pct = (count / total) * 100 if total > 0 else 0
            lines.append(f"| {model} | {count} | {pct:.1f}% |")
        lines.append("")

        # Results by target
        for target, models in top_models.items():
            lines.append(f"## Target: {target}")
            lines.append("")

            if not models:
                lines.append("*No models found for this target*")
                lines.append("")
                continue

            # Top performers table
            lines.append("### Top Models Performance")
            lines.append("")
            lines.append("| Rank | Model | Variant | RMSE | MAE | MAPE | Correlation | Dir Acc | Features |")
            lines.append("|------|-------|---------|------|-----|------|-------------|---------|----------|")

            for i, model in enumerate(models[:10], 1):  # Show top 10 instead of 3
                model_name = model["model_name"]
                variant = model.get("variant", "")
                member_name = model["member_name"]

                # Get extended metrics
                rmse = mae = mape = corr = dir_acc = "N/A"
                if "extended_metrics" in model["data"] and "1" in model["data"]["extended_metrics"]:
                    m = model["data"]["extended_metrics"]["1"]
                    rmse = f"{m.get('rmse', 'N/A'):.4f}" if isinstance(m.get('rmse'), (int, float)) else "N/A"
                    mae = f"{m.get('mae', 'N/A'):.4f}" if isinstance(m.get('mae'), (int, float)) else "N/A"
                    mape = f"{m.get('mape', 'N/A'):.2f}%" if isinstance(m.get('mape'), (int, float)) else "N/A"
                    corr = f"{m.get('correlation', 'N/A'):.3f}" if isinstance(m.get('correlation'), (int, float)) else "N/A"
                    dir_acc = f"{m.get('direction_accuracy', 'N/A'):.1f}%" if isinstance(m.get('direction_accuracy'), (int, float)) else "N/A"

                # Get feature info
                manifest = model["data"].get("manifest", {})
                feature_count = manifest.get("columns_count", "?")
                feature_desc = f"{feature_count} features"

                lines.append(f"| {i} | {model_name} | {variant} | {rmse} | {mae} | {mape} | {corr} | {dir_acc} | {feature_desc} |")

            lines.append("")

            # Add visualization if exists
            forecast_chart = charts.get(f"{target}_forecast")
            if forecast_chart:
                rel_path = os.path.relpath(forecast_chart, os.path.dirname(run_dir))
                lines.append("### Forecast Comparison")
                lines.append("")
                lines.append(f"![Forecast vs Actual]({rel_path})")
                lines.append("")

            error_chart = charts.get(f"{target}_errors")
            if error_chart:
                rel_path = os.path.relpath(error_chart, os.path.dirname(run_dir))
                lines.append("### Error Analysis")
                lines.append("")
                lines.append(f"![Error Distribution]({rel_path})")
                lines.append("")

            # Feature configuration of best model
            if models:
                best_model = models[0]
                manifest = best_model["data"].get("manifest", {})

                lines.append("### Best Model Details")
                lines.append("")
                lines.append(f"**Model:** {best_model['model_name']} (variant {best_model.get('variant', '')})")
                lines.append(f"**Member:** `{best_model['member_name']}`")

                if manifest:
                    lines.append("")
                    lines.append("**Configuration:**")
                    lines.append("```json")
                    config_data = {
                        "model": best_model["model_name"],
                        "variant": best_model.get("variant", ""),
                        "feature_count": manifest.get("columns_count", "Unknown"),
                        "normalize": manifest.get("normalize", {}),
                        "pack": manifest.get("pack", "none"),
                    }

                    # Add feature list if available
                    if "features_used" in manifest:
                        config_data["features_sample"] = manifest["features_used"][:5] if isinstance(manifest["features_used"], list) else manifest["features_used"]

                    lines.append(json.dumps(config_data, indent=2))
                    lines.append("```")

                lines.append("")

        # Appendix
        lines.append("## Appendix")
        lines.append("")
        lines.append("### Metrics Definitions")
        lines.append("")
        lines.append("- **RMSE**: Root Mean Square Error (lower is better)")
        lines.append("- **MAE**: Mean Absolute Error (lower is better)")
        lines.append("- **MAPE**: Mean Absolute Percentage Error (lower is better)")
        lines.append("- **Correlation**: Pearson correlation between forecast and actual (higher is better)")
        lines.append("- **Direction Acc**: Percentage of correct directional predictions (higher is better)")
        lines.append("")

        return "\n".join(lines)


class ReportCache:
    """Cache manager for reports."""

    def __init__(self, cache_dir: str):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_cache_key(self, run_dir: str) -> str:
        """Generate cache key for run directory."""
        # Get latest modification time
        latest_mtime = 0
        for root, dirs, files in os.walk(run_dir):
            for file in files:
                path = os.path.join(root, file)
                mtime = os.path.getmtime(path)
                latest_mtime = max(latest_mtime, mtime)

        # Create hash
        key_data = f"{run_dir}_{latest_mtime}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def is_cached(self, cache_key: str) -> bool:
        """Check if report is cached."""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        return os.path.exists(cache_file)

    def save(self, cache_key: str, data: Dict):
        """Save to cache."""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        with open(cache_file, 'w') as f:
            json.dump(data, f)

    def load(self, cache_key: str) -> Dict:
        """Load from cache."""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                return json.load(f)
        return {}


def generate_report(run_dir: str, output_dir: Optional[str] = None,
                   use_cache: bool = True, verbose: bool = False, skip_viz: bool = False) -> str:
    """Main function to generate report."""

    if not os.path.exists(run_dir):
        raise ValueError(f"Run directory not found: {run_dir}")

    # Setup output directory
    if output_dir is None:
        output_dir = run_dir

    # Initialize components
    aggregator = DataAggregator(run_dir, verbose)
    calculator = MetricsCalculator()
    viz_engine = VisualizationEngine(output_dir)
    insight_gen = InsightGenerator()
    md_generator = MarkdownGenerator()

    # Check cache
    cache = ReportCache(os.path.join(output_dir, ".report_cache"))
    cache_key = cache.get_cache_key(run_dir)

    if use_cache and cache.is_cached(cache_key):
        if verbose:
            print("Loading from cache...")
        cached_data = cache.load(cache_key)
        report_content = cached_data.get("report", "")
    else:
        if verbose:
            print("Generating new report...")

        # Load all data
        all_results = aggregator.load_all_members()

        if not all_results:
            print("No results found to generate report")
            return ""

        # Calculate extended metrics
        all_results = calculator.calculate_all_metrics(all_results)

        # Get top models
        top_models = aggregator.get_top_n_per_target(all_results, n=3)

        # Generate visualizations
        if skip_viz:
            charts = {}
        else:
            charts = viz_engine.generate_all_charts(top_models, all_results)

        # Generate insights
        insights = insight_gen.analyze(all_results)

        # Create report
        report_content = md_generator.create_report(
            top_models, charts, insights, all_results, run_dir
        )

        # Cache the report
        if use_cache:
            cache.save(cache_key, {
                "report": report_content,
                "generated": datetime.now().isoformat()
            })

    # Save report
    report_path = os.path.join(output_dir, "REPORT.md")
    with open(report_path, 'w') as f:
        f.write(report_content)

    if verbose:
        print(f"Report saved to: {report_path}")

    # Generate HTML version
    try:
        import markdown
        html_content = markdown.markdown(report_content, extensions=['tables', 'fenced_code'])

        # Add CSS styling
        html_full = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Nowcasting Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        h3 {{ color: #7f8c8d; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th {{ background-color: #3498db; color: white; padding: 10px; text-align: left; }}
        td {{ border: 1px solid #ddd; padding: 8px; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; }}
        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; }}
        .insight {{ background-color: #e8f6f3; padding: 15px; border-left: 4px solid #16a085; margin: 20px 0; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

        html_path = os.path.join(output_dir, "report.html")
        with open(html_path, 'w') as f:
            f.write(html_full)

        if verbose:
            print(f"HTML report saved to: {html_path}")

    except ImportError:
        if verbose:
            print("Note: Install 'markdown' package for HTML output")

    return report_path


def main():
    """Command line interface."""
    parser = argparse.ArgumentParser(description="Generate comprehensive report for nowcasting results")
    parser.add_argument("run_dir", help="Path to run directory (e.g., outputs/all-20250915-204332)")
    parser.add_argument("--output", "-o", help="Output directory (default: same as run_dir)")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--no-viz", action="store_true", help="Skip visualization generation")

    args = parser.parse_args()

    # Generate report
    report_path = generate_report(
        run_dir=args.run_dir,
        output_dir=args.output,
        use_cache=not args.no_cache,
        verbose=args.verbose,
        skip_viz=args.no_viz
    )

    print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()