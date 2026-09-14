from __future__ import annotations

from enum import Enum
from datetime import timedelta


class Interval(Enum):
    """
    The interval type to determine how frequent of bars to derive from a data provider.
    """
    MINUTE_1 = timedelta(minutes=1)
    MINUTE_2 = timedelta(minutes=2)
    MINUTE_5 = timedelta(minutes=5)
    MINUTE_15 = timedelta(minutes=15)
    MINUTE_30 = timedelta(minutes=30)
    MINUTE_60 = timedelta(minutes=60)
    MINUTE_90 = timedelta(minutes=90)
    HOUR_1 = timedelta(hours=1)
    DAY_1 = timedelta(days=1)
    DAY_5 = timedelta(days=5)
    WEEK_1 = timedelta(weeks=1)
