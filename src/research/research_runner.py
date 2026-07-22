# research/research_runner.py — part of Contango, a parameterized backtesting & execution framework
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

import logging
from typing import NamedTuple, Any, Callable, TypeVar, Generic

from trading.execution.backtester import BacktesterConfig, FillBehavior
from trading.execution.engine import Strategy, MarketDataEvent
from trading.optimizer.experiments import (
    BacktestExperiment, 
    BacktestExperimentGrid, 
    BacktestExperimentRunner, 
    BacktestExperimentResult
)

from broker.historical_brokers import HistoricalBroker, Config

from data.data_repository import DataRepository


logger = logging.getLogger(__name__)

TConfig = TypeVar("TConfig", bound=Config)

USD = float
percent = float
units = int


class RunConfig(NamedTuple, Generic[TConfig]):
    """
    Holds the configuration parameters for a `ResearchRunner`.
    
    Attributes:
        broker: The historical broker to use when polling for OHLCV data.
        broker_config: The config matching to the broker to determine what type of data to derive.

        strategy_factory: A callable that returns the underlying `Strategy` to test.
        param_space: A dictionary mapping each possible parameter in the strategy to a list of the desired parameters to test.

        initial_cash: The initial cash for the backtester to start with for every test.
        initial_position: The initial units for the backtester to start with for every test.
        fill_behavior: The behavior determining when trades will be filled across every backtest.

        slippage: The percent difference beteween the expected price & filled price.
        commission_per_unit: The price taxed per unit bought.
    """
    broker: HistoricalBroker[TConfig]
    broker_config: TConfig

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
    def _load_data(run_config: RunConfig[TConfig]) -> list[MarketDataEvent]:
        """
        Loads broker data from a `RunConfig` & stores it into the database.
        
        Args:
            config: The determiner for the broker & config when downloading data from it.
        
        Returns:
            A normalized pandas dataframe representation of the broker data.
        """
        data = DataRepository[TConfig].get_data_and_store(
            broker=run_config.broker,
            config=run_config.broker_config,
            expected_timestamps=run_config.broker.get_expected_timestamps(run_config.broker_config)
        )
        return data

    @staticmethod
    def _create_experiments(data: list[MarketDataEvent], config: RunConfig[TConfig]) -> list[BacktestExperiment]:
        """
        Creates all of the experiments for a `Strategy` and a given parameter space.
        
        Args:
            data: The broker data to use when backtesting.
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
    def run(config: RunConfig[TConfig], verbose_iterating: bool = True) -> list[BacktestExperimentResult]:
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
