from __future__ import annotations

import pandas as pd
import yfinance as yf   # type: ignore[missingTypeStubs]

from typing import Iterable
from datetime import datetime, timezone

from contango.market.data_providers.historical_data_provider import HistoricalDataProvider
from contango.market.data_providers.yfinance.yfinance_config import YfinanceConfig
from contango.market.data_providers.config import Interval

from contango.market.calendar.calendar import Calendar

from contango.trading.execution.engine.events import MarketDataEvent


USD = float
time_unix_ms = int
units = int

# Map interval values from the Enum to the expected str values via yfinance.download.
INTERVAL_MAP: dict[Interval, str] = {
    Interval.MINUTE_1: "1m",
    Interval.MINUTE_2: "2m",
    Interval.MINUTE_5: "5m",
    Interval.MINUTE_15: "15m",
    Interval.MINUTE_30: "30m",
    Interval.MINUTE_60: "60m",
    Interval.MINUTE_90: "90m",
    Interval.HOUR_1: "1h",
    Interval.DAY_1: "1d",
    Interval.DAY_5: "5d",
    Interval.WEEK_1: "1wk"
}


class Yfinance(HistoricalDataProvider[YfinanceConfig]):
    """
    The yfinance data provider.
    Data is limited in large quantities, some data may be innacurate, and rate limiting may be enforced with usage.
    """
    def __init__(self, calendar: Calendar) -> None:
        """
        Initializes `Yfinance`.
        
        Args:
            calendar: The calender type to follow (i.e. NYSE).
        """
        self._calendar = calendar

    def _load_data(self, config: YfinanceConfig) -> pd.DataFrame:
        """
        Loads yfinance data from a `YfinanceConfig`.
        
        Args:
            config: The determiner for the ticker, start, end, and interval when downloading yfinance data.
        
        Returns:
            A normalized pandas dataframe representation of the yfinance data.
        
        Raises:
            RuntimeError: If no data was returned for the given config.
        """
        start = datetime.fromtimestamp(config.start_timestamp / 1000, tz=timezone.utc).strftime('%Y-%m-%d')
        end = datetime.fromtimestamp(config.end_timestamp / 1000, tz=timezone.utc).strftime('%Y-%m-%d')
        interval = INTERVAL_MAP.get(config.interval, None)

        if interval is None:
            raise RuntimeError("Interval type provided was not in the interval map for yfinance!")

        data = yf.download( # type: ignore[unknownMemberType]
            tickers=config.ticker,
            start=start,
            end=end,
            interval=interval,
        )

        if data is None or data.empty:
            raise RuntimeError(f"No data returned for {config.ticker}")

        return data

    def get_bars(self, config: YfinanceConfig) -> list[MarketDataEvent]:
        """
        Returns a list of the bars for the given period.
        
        Args:
            config: The yfinance config to derive bars from.
        
        Raises:
            RuntimeError: Upon yfinance not returning any data.
        """
        data = self._load_data(config)

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        bars: list[MarketDataEvent] = []
        for timestamp, row in data.iterrows():
            bars.append(
                MarketDataEvent(
                    timestamp=int(pd.Timestamp(timestamp).timestamp() * 1000),  # type: ignore[argumentType]
                    symbol=config.ticker,
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=int(row["Volume"]),
                )
            )

        return bars

    def get_expected_timestamps(
        self,
        config: YfinanceConfig,
    ) -> Iterable[datetime]:
        """
        Returns the expected yfinance timestamps for the given calendar at initialization.

        Args:
            config: The configuration, in which the start timestamp, end timestamp, & interval will be used to 
                    derive the valid timestamps from.
        
        Returns:
            Iterable[datetime]: An iterable of valid datetime objects.
        """
        return self._calendar.get_expected_timestamps(
            start_timestamp=config.start_timestamp,
            end_timestamp=config.end_timestamp,
            interval=config.interval,
        )
