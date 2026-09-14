from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Generic, Mapping, Sequence, TypeVar, NamedTuple

from contango.data.data_repository import DataRepository

from contango.market.data_providers.historical_data_provider import HistoricalDataProvider
from contango.market.data_providers.config import Config

from contango.strategy.strategy import Strategy
from contango.strategy.rule_based.cartesian_search import cartesian_search

from contango.trading.execution.backtest import StrategyBacktester, BacktesterConfig
from contango.trading.metrics.metrics import Metrics
from contango.trading.metrics.calculate import calculate_metrics
from contango.trading.execution.engine.events.types import MarketDataEvent


logger = logging.getLogger(__name__)

TConfig = TypeVar("TConfig", bound=Config)
StrategyT = TypeVar("StrategyT", bound=Strategy)


class ExperimentResult(NamedTuple):
    """
    The resulting experiment of backtesting a single strategy variant from a grid search.

    Attributes: 
        label: The name for the experiment result.
        kwargs: A dictionary mapping strings to the parameters tested for the experiment.
        metrics: The metrics resulting from the experiment.
    """
    label: str
    kwargs: dict[str, Any]
    metrics: Metrics


class GridSearchRunner(Generic[TConfig]):
    """
    Runner for fetching data and executing every strategy variant produced
    by a Cartesian parameter grid search.
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
            symbol: GridSearchRunner[TConfig].fetch_data(provider=provider, config=config, database_path=database_path)
            for symbol, config in configs.items()
        }

    @staticmethod
    def _varying_keys(param_grid: Mapping[str, Sequence[Any]]) -> set[str]:
        return {key for key, values in param_grid.items() if len(values) > 1}

    @staticmethod
    def _format_kwargs(kwargs: Mapping[str, Any], varying_keys: set[str]) -> str:
        varying = [(key, kwargs[key]) for key in kwargs if key in varying_keys]
        if len(varying) == 1:
            return str(varying[0][1])
        return ", ".join(f"{key}={value}" for key, value in varying)

    @staticmethod
    def run(
        ohlcv_data: Mapping[str, list[MarketDataEvent]],
        strategy_cls: type[StrategyT],
        param_grid: Mapping[str, Sequence[Any]],
        backtester_config: BacktesterConfig,
        base_label: str | None = None,
        verbose: bool = True
    ) -> list[ExperimentResult]:
        """
        Runs a backtest for multiple instances of a strategy, against
        per-symbol data.
                
        Args:
            ohlcv_data: A mapping of symbol -> historical market data events for the symbol.
                        Every value that appears in param_grid["symbol"] must be a key here.
            strategy_cls: The strategy class that will be parameterized.
            param_grid: A mapping of strings (parameter names) to sequences of the kwargs to test.
                        Must include a "symbol" key whose values are all present in ohlcv_data.
            base_label: The base label for each result.
            backtester_config: The configuration for the backtester.
            verbose: Whether to print the current strategy being tested to terminal.
        
        Returns:
            list[ExperimentResult]: The metrics along with parameters & labels that were tested.
        """
        if "symbol" not in param_grid:
            raise ValueError('param_grid must include a "symbol" key to select data from ohlcv_data')

        results: list[ExperimentResult] = []
        base_label = base_label if base_label is not None else strategy_cls.__name__
        varying_keys = GridSearchRunner._varying_keys(param_grid)
        for factory, kwargs in cartesian_search(strategy_cls, param_grid):
            symbol = kwargs["symbol"]
            if symbol not in ohlcv_data:
                raise KeyError(f"No fetched data for symbol {symbol!r}; available symbols: {sorted(ohlcv_data)}")

            name = f"{base_label}({GridSearchRunner._format_kwargs(kwargs, varying_keys)})"

            if verbose:
                logger.info(f"Testing {name}")

            raw_results = StrategyBacktester.backtest(
                ohlcv_data=ohlcv_data[symbol], strategy=factory(), config=backtester_config
            )
            results.append(
                ExperimentResult(
                    label=name, 
                    kwargs=dict(kwargs), 
                    metrics=calculate_metrics(raw_results)
                )
            )
        return results
