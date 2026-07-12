from __future__ import annotations

import logging

from execution.backtester import StrategyBacktester

from optimizer.experiments.backtest_experiment import BacktestExperiment
from optimizer.experiments.backtest_experiment_result import BacktestExperimentResult
from optimizer.analysis.calculate_metrics import calculate_metrics


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
