from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List


class BaseModel(ABC):
    """
    Minimal plugin model API for v2.

    Models receive a numeric feature matrix X and target vector y to fit.
    Prediction uses a single feature row (same column order used at fit-time).
    Parameters are persisted via get_params/set_params by the engine.
    """

    @abstractmethod
    def fit(self, X: List[List[float]], y: List[float]) -> None:
        ...

    @abstractmethod
    def predict_row(self, x_row: List[float]) -> float:
        ...

    @abstractmethod
    def get_params(self) -> Dict:
        ...

    @abstractmethod
    def set_params(self, params: Dict) -> None:
        ...


class ModelSpec:
    """
    Describes a model's default input expectations and capabilities.

    Fields (all optional; used for defaults/validation):
    - frequency: list[str] or "any"
    - input: {"target": {"lags": [int, ...]}, "exog": {name: {"lags": [...]}}}
    - strategies: list[str] subset of {"frozen", "refit"}
    - supports_horizons: "any" or list[int]
    """

    def __init__(self, spec: Dict | None = None):
        self.spec = spec or {}

    def get(self, key: str, default=None):
        return self.spec.get(key, default)

