from __future__ import annotations

import os
import json
import csv
from typing import Dict, List


class OutputManager:
    def __init__(self, base_dir: str, run_id: str):
        self.base_dir = base_dir
        self.run_id = run_id
        self.run_dir = os.path.join(self.base_dir, self.run_id)
        self.artifacts_dir = os.path.join(self.run_dir, "artifacts")
        self.models_dir = os.path.join(self.run_dir, "models")
        self.forecasts_dir = os.path.join(self.run_dir, "forecasts")
        self.metrics_dir = os.path.join(self.run_dir, "metrics")
        for d in [self.base_dir, self.run_dir, self.artifacts_dir, self.models_dir, self.forecasts_dir, self.metrics_dir]:
            os.makedirs(d, exist_ok=True)

    def save_lineage(self, obj: Dict):
        with open(os.path.join(self.run_dir, "lineage.json"), "w") as f:
            json.dump(obj, f, indent=2)

    def save_model_params(self, horizon: int, plugin_name: str, params: Dict):
        path = os.path.join(self.models_dir, f"model_h{horizon}.json")
        with open(path, "w") as f:
            json.dump({"plugin": plugin_name, "params": params}, f, indent=2)

    def save_backtest_csv(self, rows: List[Dict]):
        path = os.path.join(self.forecasts_dir, "backtest.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["origin_date", "target_date", "horizon", "y_t", "forecast", "actual", "error"])
            for r in rows:
                w.writerow([
                    r.get("origin_date", ""),
                    r.get("target_date", ""),
                    r.get("horizon", ""),
                    r.get("y_t", ""),
                    r.get("forecast", ""),
                    r.get("actual", ""),
                    r.get("error", ""),
                ])

    def save_metrics_csv(self, metrics_by_h: Dict[int, Dict[str, float]]):
        path = os.path.join(self.metrics_dir, "metrics.csv")
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["horizon", "rmse", "mae"])  # header
            for h in sorted(metrics_by_h.keys()):
                m = metrics_by_h[h]
                w.writerow([h, m.get("rmse", ""), m.get("mae", "")])

    def find_latest_with_models(self, prefix: str) -> str | None:
        if not os.path.isdir(self.base_dir):
            return None
        candidates = []
        for name in os.listdir(self.base_dir):
            if not name.startswith(prefix):
                continue
            full = os.path.join(self.base_dir, name)
            if os.path.isdir(os.path.join(full, "models")):
                candidates.append((os.path.getmtime(full), full))
        if not candidates:
            return None
        candidates.sort()
        return candidates[-1][1]

