# trading/optimizer/experiments/backtest_experiment_runner.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.execution.backtester import StrategyBacktester

from contango.trading.optimizer.experiments.backtest_experiment import BacktestExperiment
from contango.trading.optimizer.experiments.backtest_experiment_result import BacktestExperimentResult
from contango.trading.optimizer.analysis.calculate_metrics import calculate_metrics


logger = logging.getLogger(__name__)


class BacktestExperimentRunner:
    """
    Runs `BacktestExperiment` objects with the backtester.
    """
    @staticmethod
    def run(experiments: list[BacktestExperiment], verbose_iterating: bool = True) -> list[BacktestExperimentResult]:
        """
        Runs experiment objects with the backtester.

        Args:
            experiments: The `BacktestExperiment` instances to backtest.
            verbose_iterating: Whether to print the name of the experiment currently being processed.
        
        Returns:
            'list[BacktestExperimentResult]': The underlying `Experiment` & `BacktestData` instances for the experiments.
        """
        results: list[BacktestExperimentResult] = []

        for experiment in experiments:
            if verbose_iterating:
                print(f"Processing experiment with params: {experiment.parameters}")

            strategy = experiment.strategy_factory(
                **experiment.parameters
            )
            data = StrategyBacktester.backtest(
                ohlcv_data=experiment.dataset,
                strategy=strategy,
                config=experiment.config
            )
            metrics = calculate_metrics(data)

            results.append(BacktestExperimentResult(
                experiment=experiment,
                backtest_metrics=metrics,
                raw_backtest_data=data
            ))
        
        return results
