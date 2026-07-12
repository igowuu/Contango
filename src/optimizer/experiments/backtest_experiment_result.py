from __future__ import annotations

from typing import NamedTuple

from execution.engine import ExecutionData

from optimizer.experiments.backtest_experiment import BacktestExperiment
from optimizer.analysis.metrics import Metrics


class BacktestExperimentResult(NamedTuple):
    """
    The results from a single backtest experiment.
    
    Attributes:
        experiment: The experiment object that was backtested.
        backtest_metrics: The metrics to analyze strategy effectiveness & results for the backtest.
        raw_backtest_data: The raw backtest events for the experiment.
    """
    experiment: BacktestExperiment
    backtest_metrics: Metrics
    raw_backtest_data: ExecutionData
