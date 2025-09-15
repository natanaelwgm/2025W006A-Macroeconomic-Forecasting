from __future__ import annotations

from typing import Dict, List

from core.base import BaseModel


NAME = "SeasonalNaive"

# Default period=12 via features: require y__lag12 as the only feature
SPEC = {
    "frequency": ["M"],
    "input": {"target": {"lags": [12]}, "exog": {}},
    "strategies": ["frozen", "refit"],
    "supports_horizons": "any",
    "params_schema": {"period": {"type": "int", "default": 12, "min": 1}}
}


class _SeasonalNaive(BaseModel):
    def __init__(self, period: int = 12):
        self.period = int(period)

    def fit(self, X: List[List[float]], y: List[float]) -> None:
        # no parameters to learn
        return

    def predict_row(self, x_row: List[float]) -> float:
        # The feature builder must provide y__lagP as the first column for convenience
        return 0.0 if not x_row else float(x_row[0])

    def get_params(self) -> Dict:
        return {"period": self.period}

    def set_params(self, params: Dict) -> None:
        self.period = int(params.get("period", self.period))


def create(params: Dict) -> BaseModel:
    period = int(params.get("period", SPEC["params_schema"]["period"]["default"]))
    return _SeasonalNaive(period=period)

