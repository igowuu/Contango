# broker/historical_brokers/config_type.py — part of Contango, a parameterized backtesting & execution framework
# Copyright (C) 2026  Jacob Taylor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

from enum import Enum
from datetime import timedelta
from dataclasses import dataclass


class Interval(Enum):
    """
    The interval type to determine how frequent of bars to derive from a broker.
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


@dataclass
class Config:
    """
    Marks a dataclass as a configurator for a historical broker when deriving data from it.

    Attributes:
        ticker: The ticker symbol for a broker call.
        interval: The interval for a broker call.
        start_timestamp: The start time in unix ms to derive data from.
        end_timestamp: The end time in unix ms to derive data from.
    """
    ticker: str
    interval: Interval
    start_timestamp: int
    end_timestamp: int
