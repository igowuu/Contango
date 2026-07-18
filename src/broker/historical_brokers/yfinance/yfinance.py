from __future__ import annotations

import pandas as pd
import yfinance as yf   # type: ignore[missingTypeStubs]

from broker.historical_brokers.historical_broker import HistoricalBroker
from broker.historical_brokers.yfinance.yfinance_config import YfinanceConfig

from execution.engine.events import MarketDataEvent


USD = float
time_unix_ms = int
units = int


class Yfinance(HistoricalBroker[YfinanceConfig]):
    """
    The yfinance data provider (not an official broker).
    Data is limited in large quantities, some data may be innacurate, and rate limiting may be enforced with usage.
    """
    @staticmethod
    def _load_data(config: YfinanceConfig) -> pd.DataFrame:
        """
        Loads yfinance data from a `YfinanceConfig`.
        
        Args:
            config: The determiner for the ticker, start, end, and interval when downloading yfinance data.
        
        Returns:
            A normalized pandas dataframe representation of the yfinance data.
        
        Raises:
            RuntimeError: If no data was returned for the given config.
        """
        data = yf.download( # type: ignore[unknownMemberType]
            tickers=config.ticker,
            start=config.start_date,
            end=config.end_date,
            interval=config.interval,
        )

        if data is None or data.empty:
            raise RuntimeError(f"No data returned for {config.ticker}")

        return data

    def get_bars(self, config: YfinanceConfig) -> list[MarketDataEvent]:
        """
        Returns a list of the bars for the given period.
        
        Args:
            period: The yfinance period to derive bars from.
        
        Raises:
            RuntimeError: Upon yfinance not returning any data.
        """
        data = Yfinance._load_data(config)

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
