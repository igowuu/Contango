from __future__ import annotations

from dataclasses import dataclass

from contango.market.data_providers.interval import Interval


@dataclass
class Config:
    """
    Marks a dataclass as a configurator for a historical data provider when deriving data from it.

    Attributes:
        ticker: The ticker symbol for a data provider call.
        interval: The interval for a data provider call.
        start_timestamp: The start time in unix ms to derive data from.
        end_timestamp: The end time in unix ms to derive data from.
    """
    ticker: str
    interval: Interval
    start_timestamp: int
    end_timestamp: int
