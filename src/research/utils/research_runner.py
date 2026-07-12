from __future__ import annotations

import logging
from typing import NamedTuple, Any, Callable

import yfinance as yf  # type: ignore[missingTypeStubs]

import pandas as pd

from execution.backtester import BacktesterConfig, FillBehavior
from execution.engine import Strategy
from optimizer import (
    BacktestExperiment, 
    BacktestExperimentGrid, 
    BacktestExperimentRunner, 
    BacktestExperimentResult
)
from research.utils.data_normalization import normalize_yfinance_data


logger = logging.getLogger(__name__)

USD = float
percent = float
units = int


class RunConfig(NamedTuple):
    """
    Holds the possible configuration parameters for a `ResearchRunner`.
    
    Attributes:
        ticker: The ticker symbol (e.g. AAPL) to derive yfinance data from.
        start_date: The start date (YYYY-MM-DD) to derive yfinance data from.
        end_date: The end date (YYYY-MM-DD) to derive yfinance data from.
        interval: The trading interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo) to derive yfinance data from.

        strategy_factory: A callable that returns the underlying `Strategy` to test.
        param_space: A dictionary mapping each possible parameter in the strategy to a list of the desired parameters to test.

        initial_cash: The initial cash for the backtester to start with for every test.
        initial_position: The initial units for the backtester to start with for every test.
        fill_behavior: The behavior determining when trades will be filled across every backtest.

        slippage: The percent difference beteween the expected price & filled price.
        commission_per_unit: The price taxed per unit bought.
    """
    ticker: str
    start_date: str
    end_date: str
    interval: str

    strategy_factory: Callable[..., Strategy]
    param_space: dict[str, list[Any]]

    initial_cash: USD = 1000
    initial_position: units = 0
    fill_behavior: FillBehavior = FillBehavior.INSTANT

    slippage: percent = 0.0
    commission_per_unit: USD = 0.0


class ResearchRunner:
    """
    Runs backtest research & computes metrics for a `Strategy`.
    """
    @staticmethod
    def _load_data(config: RunConfig) -> pd.DataFrame:
        """
        Loads yfinance data from a `RunConfig`.
        
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

        return normalize_yfinance_data(data, config.ticker)

    @staticmethod
    def _create_experiments(data: pd.DataFrame, config: RunConfig) -> list[BacktestExperiment]:
        """
        Creates all of the experiments for a `Strategy` and a given parameter space.
        
        Args:
            data: The normalized yfinance data to use when backtesting.
            config: The Config, determining the strategy factory, initial cash, initial position, fill behavior, and parameter space.
        
        Returns:
            A list of all of the experiments generated.
        """
        backtester_config = BacktesterConfig(
            initial_cash=config.initial_cash,
            initial_position=config.initial_position,
            fill=config.fill_behavior,
            slippage=config.slippage,
            commission_per_unit=config.commission_per_unit
        )

        params = list(config.param_space.keys())
        experiment = BacktestExperiment(
            strategy_factory=config.strategy_factory,
            parameters={param: None for param in params},
            dataset=data,
            config=backtester_config,
        )

        return BacktestExperimentGrid(
            base_experiment=experiment,
            param_space=config.param_space
        ).generate()

    @staticmethod
    def run(config: RunConfig, verbose_iterating: bool = True) -> list[BacktestExperimentResult]:
        """
        Downloads data and runs experiments with the given config.
        
        Args:
            config: The configuration object to derive all data from when running experiments.
            verbose_iterating: Whether to print the experiments that are currently being processed.
        
        Returns:
            A list of experiment result instances for further analysis.
        """
        data = ResearchRunner._load_data(config)
        experiments = ResearchRunner._create_experiments(data, config)
        results = BacktestExperimentRunner.run(experiments, verbose_iterating=verbose_iterating)

        return results
