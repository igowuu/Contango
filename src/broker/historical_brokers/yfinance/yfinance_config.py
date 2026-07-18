from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from broker.historical_brokers.config_type import Config


class YfinanceInterval(StrEnum):
    """
    The valid intervals for deriving yfinance data from.
    """
    ONE_MINUTE = "1m"
    TWO_MINUTE = "2m"
    FIVE_MINUTE = "5m"
    FIFTEEN_MINUTE = "15m"
    THIRTY_MINUTE = "30m"
    SIXTY_MINUTE = "60m"
    NINETY_MINUTE = "90m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    FIVE_DAY = "5d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTH = "3mo"


@dataclass
class YfinanceConfig(Config):
    """
    Holds the configuration for deriving data from the yfinance broker.
    
    Attributes:
        ticker: The ticker symbol (e.g. AAPL) to derive yfinance data from.
        start_date: The start date (YYYY-MM-DD) to derive yfinance data from.
        end_date: The end date (YYYY-MM-DD) to derive yfinance data from.
        interval: The trading interval to derive yfinance data from.
    """
    ticker: str
    start_date: str
    end_date: str
    interval: YfinanceInterval
