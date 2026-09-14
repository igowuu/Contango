from __future__ import annotations

from dataclasses import dataclass

from contango.market.data_providers.config import Config


@dataclass
class YfinanceConfig(Config):
    """
    Holds the configuration for deriving data from the yfinance data provider.
    
    Attributes:
        ticker: The ticker symbol (e.g. AAPL) to derive yfinance data from.
        start_date: The start date in unix ms to derive yfinance data from.
        end_date: The end date in unix ms to derive yfinance data from.
        interval: The trading interval to derive yfinance data from.
    """
    pass
