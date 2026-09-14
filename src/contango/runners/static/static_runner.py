from __future__ import annotations

from pathlib import Path
from typing import Generic, TypeVar, Mapping

from contango.data.data_repository import DataRepository

from contango.market.data_providers.historical_data_provider import HistoricalDataProvider
from contango.market.data_providers.config import Config

from contango.strategy.strategy import Strategy

from contango.trading.execution.backtest import StrategyBacktester, BacktesterConfig
from contango.trading.metrics.metrics import Metrics
from contango.trading.metrics.calculate import calculate_metrics
from contango.trading.execution.engine.events.types import MarketDataEvent


TConfig = TypeVar("TConfig", bound=Config)


class StaticRunner(Generic[TConfig]):
    """
    Runner for fetching data and executing a singular, unchanging `Strategy` implementation.
    """
    @staticmethod
    def fetch_data(
        provider: HistoricalDataProvider[TConfig],
        config: TConfig,
        database_path: str | Path | None = None,
    ) -> list[MarketDataEvent]:
        """
        Fetches and stores data into the database.
                
        Args:
            provider: The historical data provider (i.e. Yfinance) implementation.
            config: The configuration that matches the data provider (i.e. YfinanceConfig).
            database_path: The optional database path; if not provided, defaults to the OS-standard user data directory.
        
        Returns:
            list[MarketDataEvent]: The OHLCV data from the database and/or historical data provider.
        """
        return DataRepository[config].get_data_and_store(
            provider=provider,
            config=config,
            expected_timestamps=provider.get_expected_timestamps(config),
            database_path=database_path,
        )

    @staticmethod
    def fetch_data_multi(
        provider: HistoricalDataProvider[TConfig],
        configs: Mapping[str, TConfig],
        database_path: str | Path | None = None,
    ) -> dict[str, list[MarketDataEvent]]:
        """
        Fetches and stores data for multiple symbols, keyed by the same
        symbol strings intend to use in param_grid["symbol"].

        Args:
            provider: The historical data provider (i.e. Yfinance) implementation.
            configs: A mapping of symbol -> config for the symbol (e.g. {"AAPL": YfinanceConfig(ticker="AAPL", ...)}).
            database_path: The optional database path. if not provided, defaults to the OS-standard user data directory.

        Returns:
            dict[str, list[MarketDataEvent]]: OHLCV data per symbol.
        """
        return {
            symbol: StaticRunner[TConfig].fetch_data(provider=provider, config=config, database_path=database_path)
            for symbol, config in configs.items()
        }

    @staticmethod
    def run(
        ohlcv_data: list[MarketDataEvent], 
        strategy: Strategy, 
        backtester_config: BacktesterConfig
    ) -> Metrics:
        """
        Runs a backtest for a static, singular strategy.
        
        Args:
            ohlcv_data: A list of historical market data events to use for the backtest.
            strategy: The singular strategy implementation to backtest.
            backtester_config: The configuration for the backtester.
        
        Returns:
            Metrics: The metrics for the backtest.
        """
        raw_results = StrategyBacktester.backtest(
            ohlcv_data=ohlcv_data, strategy=strategy, config=backtester_config
        )
        return calculate_metrics(raw_results)
