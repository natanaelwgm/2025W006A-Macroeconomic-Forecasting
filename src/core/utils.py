from __future__ import annotations

from datetime import datetime


def parse_ymd(s: str | None) -> datetime | None:
    if s is None:
        return None
    s = s.strip()
    if len(s) == 8 and s.isdigit():
        return datetime.strptime(s, "%Y%m%d")
    return datetime.strptime(s, "%Y-%m-%d")


def format_ymd(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d")


def advance_date(dt: datetime, freq: str = "M", steps: int = 1) -> datetime:
    if freq == "M":
        y, m = dt.year, dt.month
        total = (y * 12 + (m - 1)) + steps
        new_y = total // 12
        new_m = (total % 12) + 1
        return datetime(new_y, new_m, 28)
    return dt

