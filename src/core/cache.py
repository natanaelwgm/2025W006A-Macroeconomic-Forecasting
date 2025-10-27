#!/usr/bin/env python3
"""
Cache Management System for Nowcasting Models

This module provides intelligent caching for model training and results,
avoiding redundant computations by storing and reusing previous runs
with identical configurations.
"""

from __future__ import annotations

import os
import json
import hashlib
import shutil
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import pickle


class CacheManager:
    """Manages model and result caching for nowcasting runs."""

    def __init__(self, base_dir: str = "v2-claude/model_library", verbose: bool = False):
        """
        Initialize the cache manager.

        Args:
            base_dir: Base directory for the model library
            verbose: Enable verbose logging
        """
        self.base_dir = base_dir
        self.models_dir = os.path.join(base_dir, "models")
        self.results_dir = os.path.join(base_dir, "results")
        self.index_path = os.path.join(base_dir, "index.json")
        self.verbose = verbose

        # Create directories if they don't exist
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.results_dir, exist_ok=True)

        # Load or initialize index
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """Load the cache index from disk."""
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r') as f:
                return json.load(f)
        return {"entries": {}, "metadata": {"created": datetime.now().isoformat()}}

    def _save_index(self):
        """Save the cache index to disk."""
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)

    def generate_cache_key(
        self,
        model_name: str,
        model_params: Dict,
        target_id: str,
        features_cfg: Dict,
        horizons: List[int],
        train_range: Tuple[Optional[datetime], Optional[datetime]],
        test_range: Tuple[Optional[datetime], Optional[datetime]],
        data_fingerprint: str,
        frequency: str,
        strategy: str
    ) -> str:
        """
        Generate a unique cache key for a model configuration.

        Returns:
            A hexadecimal hash string uniquely identifying this configuration
        """
        # Create a deterministic representation of the configuration
        config = {
            "model_name": model_name,
            "model_params": self._normalize_params(model_params),
            "target_id": target_id,
            "features_cfg": self._normalize_features(features_cfg),
            "horizons": sorted(horizons),
            "train_range": [
                train_range[0].isoformat() if train_range[0] else None,
                train_range[1].isoformat() if train_range[1] else None
            ],
            "test_range": [
                test_range[0].isoformat() if test_range[0] else None,
                test_range[1].isoformat() if test_range[1] else None
            ],
            "data_fingerprint": data_fingerprint,
            "frequency": frequency,
            "strategy": strategy
        }

        # Convert to canonical JSON string for consistent hashing
        config_str = json.dumps(config, sort_keys=True, separators=(',', ':'))

        # Generate SHA256 hash
        return hashlib.sha256(config_str.encode()).hexdigest()[:16]

    def _normalize_params(self, params: Dict) -> Dict:
        """Normalize model parameters for consistent hashing."""
        if not params:
            return {}
        # Sort keys and ensure consistent representation
        return {k: v for k, v in sorted(params.items())}

    def _normalize_features(self, features: Dict) -> Dict:
        """Normalize feature configuration for consistent hashing."""
        if not features:
            return {}

        normalized = {}

        # Handle target lags
        if "target_lags" in features:
            normalized["target_lags"] = sorted(features["target_lags"])

        # Handle exogenous variables
        if "exog" in features and features["exog"]:
            exog = {}
            for var_name in sorted(features["exog"].keys()):
                var_cfg = features["exog"][var_name]
                if isinstance(var_cfg, dict) and "lags" in var_cfg:
                    exog[var_name] = {"lags": sorted(var_cfg["lags"])}
                else:
                    exog[var_name] = var_cfg
            normalized["exog"] = exog

        # Handle other feature settings
        for key in ["pack", "normalize", "max_features"]:
            if key in features:
                normalized[key] = features[key]

        return normalized

    def compute_data_fingerprint(self, frame) -> str:
        """
        Compute a fingerprint of the data frame for change detection.

        Args:
            frame: TimeSeriesFrame object

        Returns:
            A hash string representing the data content
        """
        # Create a fingerprint based on shape, columns, and sample of data
        fingerprint_data = {
            "shape": (len(frame.dates), len(frame.columns)),
            "columns": sorted(frame.columns.keys()),
            "date_range": [
                frame.dates[0].isoformat() if frame.dates else None,
                frame.dates[-1].isoformat() if frame.dates else None
            ],
            # Sample first and last few rows for change detection
            "sample_checksum": self._compute_data_sample_checksum(frame)
        }

        fingerprint_str = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.md5(fingerprint_str.encode()).hexdigest()

    def _compute_data_sample_checksum(self, frame) -> str:
        """Compute checksum of data samples for fingerprinting."""
        sample_size = min(5, len(frame.dates))
        if sample_size == 0:
            return ""

        # Sample first and last rows
        sample_data = []
        for i in list(range(sample_size)) + list(range(-sample_size, 0)):
            if 0 <= i < len(frame.dates):
                row = []
                for col in sorted(frame.columns.keys()):
                    val = frame.columns[col][i] if i < len(frame.columns[col]) else None
                    row.append(str(val))
                sample_data.append(",".join(row))

        return hashlib.md5("\n".join(sample_data).encode()).hexdigest()

    def check_cache(self, cache_key: str) -> Optional[Dict]:
        """
        Check if a cache entry exists for the given key.

        Returns:
            Cache entry metadata if exists, None otherwise
        """
        return self.index["entries"].get(cache_key)

    def load_cached_models(self, cache_key: str) -> Dict[int, Dict]:
        """
        Load cached model parameters for all horizons.

        Returns:
            Dictionary mapping horizon to model parameters
        """
        models = {}
        model_dir = os.path.join(self.models_dir, cache_key)

        if not os.path.exists(model_dir):
            return models

        for filename in os.listdir(model_dir):
            if filename.startswith("model_h") and filename.endswith(".json"):
                horizon = int(filename.split("model_h")[1].split(".")[0])
                with open(os.path.join(model_dir, filename), 'r') as f:
                    models[horizon] = json.load(f)

        return models

    def load_cached_results(self, cache_key: str) -> Dict:
        """
        Load cached results (metrics, forecasts, etc.).

        Returns:
            Dictionary containing cached results
        """
        results = {}
        result_dir = os.path.join(self.results_dir, cache_key)

        if not os.path.exists(result_dir):
            return results

        # Load metrics
        metrics_path = os.path.join(result_dir, "metrics.json")
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                results["metrics"] = json.load(f)

        # Load backtest results
        backtest_path = os.path.join(result_dir, "backtest.json")
        if os.path.exists(backtest_path):
            with open(backtest_path, 'r') as f:
                results["backtest"] = json.load(f)

        return results

    def save_to_cache(
        self,
        cache_key: str,
        models: Dict[int, Dict],
        metrics: Dict,
        backtest_rows: List[Dict],
        metadata: Dict
    ):
        """
        Save models and results to cache.

        Args:
            cache_key: Unique cache key
            models: Dictionary of model parameters by horizon
            metrics: Metrics dictionary
            backtest_rows: Backtest result rows
            metadata: Additional metadata about the run
        """
        # Save models
        model_dir = os.path.join(self.models_dir, cache_key)
        os.makedirs(model_dir, exist_ok=True)

        for horizon, model_data in models.items():
            model_path = os.path.join(model_dir, f"model_h{horizon}.json")
            with open(model_path, 'w') as f:
                json.dump(model_data, f, indent=2)

        # Save metadata
        metadata_path = os.path.join(model_dir, "metadata.json")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        # Save results
        result_dir = os.path.join(self.results_dir, cache_key)
        os.makedirs(result_dir, exist_ok=True)

        # Save metrics
        metrics_path = os.path.join(result_dir, "metrics.json")
        with open(metrics_path, 'w') as f:
            json.dump(metrics, f, indent=2)

        # Save backtest results
        backtest_path = os.path.join(result_dir, "backtest.json")
        with open(backtest_path, 'w') as f:
            json.dump(backtest_rows, f, indent=2)

        # Update index
        self.index["entries"][cache_key] = {
            "created": datetime.now().isoformat(),
            "metadata": metadata,
            "horizons": list(models.keys()),
            "metrics_summary": {
                h: {"rmse": metrics.get(h, {}).get("rmse"), "mae": metrics.get(h, {}).get("mae")}
                for h in models.keys()
            }
        }
        self._save_index()

        if self.verbose:
            print(f"[Cache] Saved to cache: {cache_key}")

    def copy_from_cache(self, cache_key: str, output_dir: str):
        """
        Copy cached results to output directory.

        Args:
            cache_key: Cache key to copy from
            output_dir: Destination directory
        """
        # Copy models
        src_model_dir = os.path.join(self.models_dir, cache_key)
        dst_model_dir = os.path.join(output_dir, "models")
        if os.path.exists(src_model_dir):
            os.makedirs(dst_model_dir, exist_ok=True)
            for filename in os.listdir(src_model_dir):
                if filename.endswith(".json"):
                    shutil.copy2(
                        os.path.join(src_model_dir, filename),
                        os.path.join(dst_model_dir, filename)
                    )

        # Copy results
        src_result_dir = os.path.join(self.results_dir, cache_key)
        if os.path.exists(src_result_dir):
            # Copy metrics
            for filename in ["metrics.json", "backtest.json"]:
                src_path = os.path.join(src_result_dir, filename)
                if os.path.exists(src_path):
                    if filename == "metrics.json":
                        dst_dir = os.path.join(output_dir, "metrics")
                        os.makedirs(dst_dir, exist_ok=True)
                        # Convert to CSV format for compatibility
                        with open(src_path, 'r') as f:
                            metrics = json.load(f)
                        # The OutputManager will handle CSV conversion
                    elif filename == "backtest.json":
                        dst_dir = os.path.join(output_dir, "forecasts")
                        os.makedirs(dst_dir, exist_ok=True)
                        # Convert to CSV format for compatibility

        if self.verbose:
            print(f"[Cache] Loaded from cache: {cache_key}")

    def get_cache_stats(self) -> Dict:
        """Get statistics about the cache."""
        total_entries = len(self.index["entries"])
        total_models = sum(
            len(entry.get("horizons", []))
            for entry in self.index["entries"].values()
        )

        # Calculate cache size
        cache_size = 0
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                cache_size += os.path.getsize(os.path.join(root, file))

        return {
            "total_entries": total_entries,
            "total_models": total_models,
            "cache_size_mb": cache_size / (1024 * 1024),
            "oldest_entry": min(
                (e["created"] for e in self.index["entries"].values()),
                default=None
            ),
            "newest_entry": max(
                (e["created"] for e in self.index["entries"].values()),
                default=None
            )
        }

    def clear_cache(self, older_than_days: Optional[int] = None):
        """
        Clear cache entries.

        Args:
            older_than_days: Only clear entries older than this many days
        """
        if older_than_days is None:
            # Clear everything
            shutil.rmtree(self.models_dir)
            shutil.rmtree(self.results_dir)
            os.makedirs(self.models_dir, exist_ok=True)
            os.makedirs(self.results_dir, exist_ok=True)
            self.index = {"entries": {}, "metadata": {"created": datetime.now().isoformat()}}
            self._save_index()
            if self.verbose:
                print("[Cache] Cleared all cache entries")
        else:
            # Clear old entries
            cutoff = datetime.now().timestamp() - (older_than_days * 24 * 3600)
            keys_to_remove = []

            for key, entry in self.index["entries"].items():
                created = datetime.fromisoformat(entry["created"]).timestamp()
                if created < cutoff:
                    keys_to_remove.append(key)

            for key in keys_to_remove:
                # Remove from disk
                model_dir = os.path.join(self.models_dir, key)
                result_dir = os.path.join(self.results_dir, key)
                if os.path.exists(model_dir):
                    shutil.rmtree(model_dir)
                if os.path.exists(result_dir):
                    shutil.rmtree(result_dir)
                # Remove from index
                del self.index["entries"][key]

            self._save_index()
            if self.verbose:
                print(f"[Cache] Cleared {len(keys_to_remove)} old cache entries")