#!/usr/bin/env python3
"""
Multi-Target Runner for Nowcasting

Runs models for multiple target variables and organizes results in a unified structure.
"""

import os
import sys
import json
import time
import shutil
from datetime import datetime
import subprocess

def load_recipe(path):
    with open(path, 'r') as f:
        return json.load(f)

def build_run_id(prefix="run"):
    ts = time.strftime("%Y%m%d-%H%M%S")
    return f"{prefix}-{ts}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_multi_targets.py <recipe.json> [--verbose]")
        sys.exit(1)

    recipe_path = sys.argv[1]
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    # Load multi-target recipe
    recipe = load_recipe(recipe_path)

    # Get targets configuration
    targets = recipe.get("targets", [])
    if not targets:
        print("Error: No targets defined in recipe")
        sys.exit(1)

    # Create unified output directory
    run_name = recipe.get("run_name", "multi_target")
    master_run_id = build_run_id(run_name)
    master_output_dir = os.path.join("outputs", master_run_id)
    os.makedirs(master_output_dir, exist_ok=True)

    # Save master metadata
    master_metadata = {
        "run_id": master_run_id,
        "timestamp": datetime.now().isoformat(),
        "recipe_path": recipe_path,
        "targets": [t["id"] for t in targets],
        "n_targets": len(targets)
    }

    with open(os.path.join(master_output_dir, "master_metadata.json"), "w") as f:
        json.dump(master_metadata, f, indent=2)

    print(f"{'='*60}")
    print(f"Multi-Target Nowcasting Run")
    print(f"Targets: {len(targets)}")
    print(f"Output: {master_output_dir}")
    print(f"{'='*60}\n")

    # Track all runs
    all_runs = []

    # Process each target
    for idx, target_config in enumerate(targets, 1):
        target_id = target_config["id"]
        target_name = target_config.get("name", target_id)
        target_horizons = target_config.get("horizons", recipe.get("horizons", [1, 3, 6]))

        print(f"\n[{idx}/{len(targets)}] Processing: {target_name}")
        print(f"Target variable: {target_id}")
        print(f"Horizons: {target_horizons}")
        print("-" * 40)

        # Create target-specific recipe
        target_recipe = dict(recipe)
        target_recipe["target_id"] = target_id
        target_recipe["horizons"] = target_horizons

        # Remove targets list from single-target recipe
        if "targets" in target_recipe:
            del target_recipe["targets"]

        # Override output to go to master directory
        target_recipe["output"] = {"dir": os.path.join(master_output_dir, f"target_{target_id}")}

        # Save temporary recipe
        temp_recipe_path = f"/tmp/recipe_{target_id}_{master_run_id}.json"
        with open(temp_recipe_path, "w") as f:
            json.dump(target_recipe, f, indent=2)

        # Run models for this target
        cmd = [
            "python3", "run_v2.py",
            temp_recipe_path,
            "--all"  # Run all models
        ]

        if verbose:
            cmd.append("--verbose")

        print(f"Running command: {' '.join(cmd)}")

        try:
            # Don't capture output if verbose - let it stream to console
            if verbose:
                result = subprocess.run(cmd, text=True)
            else:
                result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✓ Successfully completed {target_name}")

                # Find the output directory (should be an all-* directory)
                target_output_base = os.path.join(master_output_dir, f"target_{target_id}")
                if os.path.exists(target_output_base):
                    # Find the all-* subdirectory
                    for item in os.listdir(target_output_base):
                        if item.startswith("all-"):
                            all_runs.append({
                                "target_id": target_id,
                                "target_name": target_name,
                                "output_dir": os.path.join(target_output_base, item)
                            })
                            break
            else:
                print(f"✗ Failed to run {target_name}")
                if not verbose:
                    print(f"Error: {result.stderr}")

        except Exception as e:
            print(f"✗ Exception running {target_name}: {e}")

        # Clean up temp recipe
        if os.path.exists(temp_recipe_path):
            os.remove(temp_recipe_path)

    # Save summary of all runs
    summary = {
        "master_run_id": master_run_id,
        "timestamp": datetime.now().isoformat(),
        "n_targets": len(targets),
        "completed_runs": len(all_runs),
        "runs": all_runs
    }

    summary_path = os.path.join(master_output_dir, "runs_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n{'='*60}")
    print(f"Multi-Target Run Complete!")
    print(f"Completed: {len(all_runs)}/{len(targets)} targets")
    print(f"Results: {master_output_dir}")
    print(f"Summary: {summary_path}")
    print(f"{'='*60}\n")

    # Generate unified report
    print("\nGenerating unified report...")

    # Try to use the same Python that works for other scripts
    python_exe = sys.executable  # Use the same Python interpreter

    report_cmd = [
        python_exe, "report_multi_targets_v2.py",
        master_output_dir
    ]

    if verbose:
        report_cmd.append("--verbose")

    try:
        # Stream output if verbose
        if verbose:
            subprocess.run(report_cmd)
        else:
            subprocess.run(report_cmd, capture_output=True)
        print(f"Report generated: {master_output_dir}/UNIFIED_REPORT.md")
    except Exception as e:
        print(f"Note: Run 'python3 report_multi_targets_v2.py {master_output_dir}' to generate the unified report")
        print(f"Error: {e}")

    return master_output_dir

if __name__ == "__main__":
    main()