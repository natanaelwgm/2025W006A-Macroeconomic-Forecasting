from __future__ import annotations

import csv
from datetime import datetime
from typing import Dict, List, Optional

from .utils import parse_ymd


class TimeSeriesFrame:
    def __init__(self, dates: List[datetime], columns: Dict[str, List[float]]):
        self.dates = dates
        self.columns = columns

    @staticmethod
    def from_csv(path: str, date_col: str, select_cols: Optional[List[str]] = None, as_of_date: Optional[datetime] = None) -> "TimeSeriesFrame":
        dates: List[datetime] = []
        cols: Dict[str, List[float]] = {}
        with open(path, "r", newline="") as f:
            r = csv.DictReader(f)
            if select_cols is None:
                select_cols = [c for c in r.fieldnames if c != date_col]
            for c in select_cols:
                cols[c] = []
            for row in r:
                dt = parse_ymd(row[date_col])
                if as_of_date is not None and dt > as_of_date:
                    break
                dates.append(dt)
                for c in select_cols:
                    try:
                        v = float(row[c])
                    except Exception:
                        v = float('nan')
                    cols[c].append(v)
        return TimeSeriesFrame(dates, cols)

    def subset(self, keep_cols: List[str]) -> "TimeSeriesFrame":
        return TimeSeriesFrame(self.dates[:], {c: self.columns[c][:] for c in keep_cols})

