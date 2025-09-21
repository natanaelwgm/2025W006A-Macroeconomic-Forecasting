#!/usr/bin/env python3
"""
Unified Report Generator for Multi-Target Nowcasting Results

Generates a comprehensive report across all target variables with:
- Top models per target
- Forecast vs actual charts
- Comparative analysis
"""

import os
import sys
import json
import csv
import numpy as np
from datetime import datetime
import argparse
import warnings

warnings.filterwarnings('ignore')

# Add src to path
CUR_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CUR_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Import from report_v3 for reuse
from report_v3 import DataAggregator, MetricsCalculator, VisualizationEngine


class MultiTargetReportGenerator:
    """Generate unified report for multi-target runs."""

    def __init__(self, master_dir: str, verbose: bool = False):
        self.master_dir = master_dir
        self.verbose = verbose
        self.viz_dir = os.path.join(master_dir, "visualizations")
        os.makedirs(self.viz_dir, exist_ok=True)

    def load_runs_summary(self):
        """Load the summary of all target runs."""
        summary_path = os.path.join(self.master_dir, "runs_summary.json")
        if not os.path.exists(summary_path):
            # Fallback: scan for target directories
            return self._scan_for_targets()

        with open(summary_path, 'r') as f:
            return json.load(f)

    def _scan_for_targets(self):
        """Scan directory structure to find target runs."""
        runs = []
        for item in os.listdir(self.master_dir):
            if item.startswith("target_"):
                target_dir = os.path.join(self.master_dir, item)
                if os.path.isdir(target_dir):
                    # Extract target ID from directory name
                    target_id = item.replace("target_", "")

                    # Find all-* subdirectory
                    for subitem in os.listdir(target_dir):
                        if subitem.startswith("all-"):
                            runs.append({
                                "target_id": target_id,
                                "target_name": self._format_target_name(target_id),
                                "output_dir": os.path.join(target_dir, subitem)
                            })
                            break

        return {"runs": runs}

    def _format_target_name(self, target_id: str) -> str:
        """Format target ID into readable name."""
        names = {
            "cpi_yoy": "CPI Year-over-Year",
            "gdp_yoy": "GDP Year-over-Year",
            "usd_idr": "USD/IDR Exchange Rate",
            "policy_rate_7drr": "Policy Rate (7DRR)",
            "money_supply": "Money Supply",
            "jci": "Jakarta Composite Index"
        }
        return names.get(target_id, target_id.replace("_", " ").title())

    def generate_report(self):
        """Generate the unified multi-target report."""
        summary = self.load_runs_summary()
        runs = summary.get("runs", [])

        if not runs:
            print("No target runs found")
            return None

        # Start building report
        lines = []
        lines.append("# Indonesia Macroeconomic Nowcasting Report")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Master Run:** `{os.path.basename(self.master_dir)}`")
        lines.append("")

        # Executive Summary
        lines.append("## Executive Summary")
        lines.append("")
        lines.append(f"**Targets Analyzed:** {len(runs)}")

        # List targets
        lines.append("")
        lines.append("### Target Variables")
        for run in runs:
            lines.append(f"- {run['target_name']} (`{run['target_id']}`)")
        lines.append("")

        # Overall statistics
        total_models = 0
        total_estimations = 0

        for run in runs:
            if os.path.exists(run["output_dir"]):
                members_dir = os.path.join(run["output_dir"], "members")
                if os.path.exists(members_dir):
                    n_members = len([d for d in os.listdir(members_dir) if os.path.isdir(os.path.join(members_dir, d))])
                    total_models += n_members
                    total_estimations += n_members  # Each member is one estimation

        lines.append("### Overall Statistics")
        lines.append("")
        lines.append(f"- **Total Model Configurations:** {total_models:,}")
        lines.append(f"- **Total Estimations:** {total_estimations:,}")
        lines.append(f"- **Models per Target:** {total_models // len(runs) if runs else 0}")
        lines.append("")

        # Process each target
        for run_idx, run in enumerate(runs, 1):
            target_id = run["target_id"]
            target_name = run["target_name"]
            output_dir = run["output_dir"]

            lines.append(f"## {run_idx}. Predictions for {target_name}")
            lines.append("")

            if not os.path.exists(output_dir):
                lines.append(f"*No results found for {target_name}*")
                lines.append("")
                continue

            # Load data for this target
            aggregator = DataAggregator(output_dir, self.verbose)
            calculator = MetricsCalculator()

            all_results = aggregator.load_all_members()
            if not all_results:
                lines.append(f"*No model results found for {target_name}*")
                lines.append("")
                continue

            # Calculate metrics
            all_results = calculator.calculate_all_metrics(all_results)

            # Get top models for this target
            top_models = self._get_top_models(all_results, n=10)

            # Summary for this target
            lines.append(f"**Models Tested:** {len(all_results)}")
            lines.append("")

            # Top performers table
            lines.append("### Top 5 Models")
            lines.append("")
            lines.append("| Rank | Model Type | Config | RMSE (H=1) | MAE (H=1) | MAPE | Correlation |")
            lines.append("|------|------------|--------|------------|-----------|------|-------------|")

            for i, model in enumerate(top_models[:5], 1):
                model_type = model["model_name"]
                member = model["member_name"]

                # Get metrics
                rmse = mae = mape = corr = "N/A"
                if "extended_metrics" in model["data"] and "1" in model["data"]["extended_metrics"]:
                    m = model["data"]["extended_metrics"]["1"]
                    rmse = f"{m.get('rmse', 'N/A'):.4f}" if isinstance(m.get('rmse'), (int, float)) else "N/A"
                    mae = f"{m.get('mae', 'N/A'):.4f}" if isinstance(m.get('mae'), (int, float)) else "N/A"
                    mape = f"{m.get('mape', 'N/A'):.1f}%" if isinstance(m.get('mape'), (int, float)) else "N/A"
                    corr = f"{m.get('correlation', 'N/A'):.3f}" if isinstance(m.get('correlation'), (int, float)) else "N/A"

                # Short config description
                config = member.split("-")[2] if len(member.split("-")) > 2 else ""

                lines.append(f"| {i} | {model_type} | {config} | {rmse} | {mae} | {mape} | {corr} |")

            lines.append("")

            # Generate visualization for top 3
            chart_path = self._generate_target_chart(target_id, target_name, top_models[:3], output_dir)
            if chart_path:
                rel_path = os.path.relpath(chart_path, os.path.dirname(self.master_dir))
                lines.append("### Forecast vs Actual (Top 3 Models)")
                lines.append("")
                lines.append(f"![{target_name} Forecast]({rel_path})")
                lines.append("")

            # Best model details
            if top_models:
                best = top_models[0]
                lines.append("### Best Model Configuration")
                lines.append("")
                lines.append(f"**Model Type:** {best['model_name']}")
                lines.append(f"**Member:** `{best['member_name']}`")

                # Get feature details
                manifest = best["data"].get("manifest", {})
                if manifest:
                    lines.append("")
                    lines.append("**Features:**")
                    lines.append(f"- Feature Count: {manifest.get('columns_count', 'Unknown')}")
                    lines.append(f"- Normalization: {manifest.get('normalize', 'None')}")
                    lines.append(f"- Feature Pack: {manifest.get('pack', 'None')}")

                lines.append("")

            # Performance across horizons
            lines.append("### Performance Degradation Across Horizons")
            lines.append("")
            lines.append("| Model | H=1 RMSE | H=3 RMSE | H=6 RMSE | Degradation |")
            lines.append("|-------|----------|----------|----------|-------------|")

            for model in top_models[:3]:
                model_name = model["model_name"]
                rmse_h1 = rmse_h3 = rmse_h6 = degradation = "N/A"

                # Get metrics for each horizon
                metrics_data = model["data"].get("metrics", [])
                rmse_by_h = {}
                for m in metrics_data:
                    try:
                        h = int(m.get("horizon", 0))
                        rmse_by_h[h] = float(m.get("rmse", 0))
                    except:
                        continue

                if 1 in rmse_by_h:
                    rmse_h1 = f"{rmse_by_h[1]:.4f}"
                if 3 in rmse_by_h:
                    rmse_h3 = f"{rmse_by_h[3]:.4f}"
                if 6 in rmse_by_h:
                    rmse_h6 = f"{rmse_by_h[6]:.4f}"

                # Calculate degradation
                if 1 in rmse_by_h and 6 in rmse_by_h and rmse_by_h[1] > 0:
                    deg = ((rmse_by_h[6] - rmse_by_h[1]) / rmse_by_h[1]) * 100
                    degradation = f"+{deg:.1f}%"

                lines.append(f"| {model_name} | {rmse_h1} | {rmse_h3} | {rmse_h6} | {degradation} |")

            lines.append("")
            lines.append("---")
            lines.append("")

        # Comparative Analysis
        lines.append("## Comparative Analysis Across Targets")
        lines.append("")
        lines.append("### Best Models by Target")
        lines.append("")
        lines.append("| Target Variable | Best Model | RMSE (H=1) | Key Features |")
        lines.append("|-----------------|------------|------------|--------------|")

        for run in runs:
            target_name = run["target_name"]
            output_dir = run["output_dir"]

            if os.path.exists(output_dir):
                aggregator = DataAggregator(output_dir, False)
                calculator = MetricsCalculator()
                results = aggregator.load_all_members()
                if results:
                    results = calculator.calculate_all_metrics(results)
                    top = self._get_top_models(results, n=1)
                    if top:
                        best = top[0]
                        model_name = best["model_name"]
                        rmse = "N/A"
                        if "extended_metrics" in best["data"] and "1" in best["data"]["extended_metrics"]:
                            rmse_val = best["data"]["extended_metrics"]["1"].get("rmse")
                            if isinstance(rmse_val, (int, float)):
                                rmse = f"{rmse_val:.4f}"

                        # Get key features (simplified)
                        features = "Standard lags"
                        manifest = best["data"].get("manifest", {})
                        if manifest.get("pack") == "ta_basic":
                            features = "Technical indicators"

                        lines.append(f"| {target_name} | {model_name} | {rmse} | {features} |")

        lines.append("")

        # Appendix
        lines.append("## Appendix")
        lines.append("")
        lines.append("### Metrics Definitions")
        lines.append("")
        lines.append("- **RMSE**: Root Mean Square Error - measures average prediction error")
        lines.append("- **MAE**: Mean Absolute Error - average absolute difference")
        lines.append("- **MAPE**: Mean Absolute Percentage Error - error as percentage")
        lines.append("- **Correlation**: Linear relationship between forecast and actual")
        lines.append("- **H**: Horizon - number of periods ahead for prediction")
        lines.append("")

        lines.append("### Model Types")
        lines.append("")
        lines.append("- **AR1/ARp**: Autoregressive models")
        lines.append("- **Tree**: Decision tree")
        lines.append("- **RandomForest**: Ensemble of decision trees")
        lines.append("- **GradientBoosting**: Sequential boosting ensemble")
        lines.append("- **ExtraTrees**: Extremely randomized trees")
        lines.append("- **StochasticGB**: Stochastic gradient boosting")
        lines.append("")

        return "\n".join(lines)

    def _get_top_models(self, results: dict, n: int = 10) -> list:
        """Get top N models sorted by RMSE at horizon 1."""
        models_list = []

        for member_name, data in results.items():
            if not data.get("metrics"):
                continue

            # Get RMSE for horizon 1
            rmse_h1 = None
            for m in data["metrics"]:
                try:
                    if int(m.get("horizon", 0)) == 1:
                        rmse_h1 = float(m.get("rmse", float('inf')))
                        break
                except:
                    continue

            if rmse_h1 is not None and rmse_h1 != float('inf'):
                models_list.append({
                    "member_name": member_name,
                    "model_name": data.get("model_name", "Unknown"),
                    "rmse_h1": rmse_h1,
                    "data": data
                })

        # Sort by RMSE
        models_list.sort(key=lambda x: x["rmse_h1"])

        return models_list[:n]

    def _generate_target_chart(self, target_id: str, target_name: str, top_models: list, output_dir: str):
        """Generate forecast vs actual chart for a target."""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import matplotlib.dates as mdates
        except ImportError:
            if self.verbose:
                print("Matplotlib not available, skipping charts")
            return None

        if not top_models:
            return None

        fig, ax = plt.subplots(figsize=(14, 7))

        # Get actual values from first model
        first_model = top_models[0]["data"]
        if "extended_metrics" not in first_model or "1" not in first_model["extended_metrics"]:
            return None

        metrics = first_model["extended_metrics"]["1"]
        dates = [self._parse_date(d) for d in metrics.get("dates", [])]
        actual = metrics.get("actual", [])

        if not dates or not actual:
            return None

        # Plot actual
        ax.plot(dates, actual, 'k-', linewidth=2.5, label='Actual', alpha=0.8)

        # Plot top 3 models
        colors = ['#2E86AB', '#A23B72', '#F18F01']
        styles = ['-', '--', '-.']

        for i, model in enumerate(top_models[:3]):
            if "extended_metrics" in model["data"] and "1" in model["data"]["extended_metrics"]:
                m_metrics = model["data"]["extended_metrics"]["1"]
                forecast = m_metrics.get("forecast", [])
                if forecast:
                    model_label = f"{model['model_name']} (RMSE: {model['rmse_h1']:.3f})"
                    ax.plot(dates, forecast, color=colors[i], linestyle=styles[i],
                           linewidth=1.8, label=model_label, alpha=0.9)

        # Formatting
        ax.set_title(f'{target_name} - Forecast vs Actual (Top 3 Models)',
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Value', fontsize=12)
        ax.legend(loc='best', frameon=True, shadow=True, fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # Format dates
        try:
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        except:
            pass
        plt.xticks(rotation=45)

        # Add shaded region for test period
        if dates:
            test_start_idx = len(dates) // 3  # Approximate
            ax.axvspan(dates[test_start_idx], dates[-1], alpha=0.1, color='gray', label='Test Period')

        plt.tight_layout()

        # Save
        filename = f"{target_id}_forecast_comparison.png"
        filepath = os.path.join(self.viz_dir, filename)
        plt.savefig(filepath, dpi=120, bbox_inches='tight')
        plt.close()

        return filepath

    def _parse_date(self, date_str: str):
        """Parse date string."""
        try:
            from datetime import datetime
            return datetime.strptime(date_str, '%Y-%m-%d')
        except:
            return date_str


def main():
    parser = argparse.ArgumentParser(description="Generate unified report for multi-target nowcasting")
    parser.add_argument("master_dir", help="Master output directory from multi-target run")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if not os.path.exists(args.master_dir):
        print(f"Error: Directory not found: {args.master_dir}")
        sys.exit(1)

    # Generate report
    generator = MultiTargetReportGenerator(args.master_dir, args.verbose)
    report_content = generator.generate_report()

    if not report_content:
        print("Failed to generate report")
        sys.exit(1)

    # Save report
    report_path = os.path.join(args.master_dir, "UNIFIED_REPORT.md")
    with open(report_path, 'w') as f:
        f.write(report_content)

    print(f"Report saved to: {report_path}")

    # Generate HTML version
    try:
        import markdown
        html_content = markdown.markdown(report_content, extensions=['tables', 'fenced_code'])

        html_full = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Indonesia Macro Nowcasting Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        h1 {{
            color: #1a472a;
            border-bottom: 4px solid #2e7d32;
            padding-bottom: 15px;
        }}
        h2 {{
            color: #2e7d32;
            margin-top: 40px;
            background: white;
            padding: 10px;
            border-left: 5px solid #4caf50;
        }}
        h3 {{ color: #388e3c; }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        th {{
            background: linear-gradient(135deg, #4caf50, #2e7d32);
            color: white;
            padding: 12px;
            text-align: left;
        }}
        td {{
            border: 1px solid #ddd;
            padding: 10px;
        }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        tr:hover {{ background-color: #f0f8ff; }}
        code {{
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }}
        pre {{
            background-color: #263238;
            color: #aed581;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
            margin: 30px auto;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border-radius: 8px;
        }}
        .summary-box {{
            background: white;
            border: 2px solid #4caf50;
            border-radius: 8px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""

        html_path = os.path.join(args.master_dir, "unified_report.html")
        with open(html_path, 'w') as f:
            f.write(html_full)

        print(f"HTML report saved to: {html_path}")

    except ImportError:
        print("Note: Install 'markdown' package for HTML output")

    return report_path


if __name__ == "__main__":
    main()