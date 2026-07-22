# trading/optimizer/experiments/backtest_experiment_result.py — part of Contango, a parameterized backtesting & execution framework
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

from typing import NamedTuple

from trading.execution.engine import ExecutionData

from trading.optimizer.experiments.backtest_experiment import BacktestExperiment
from trading.optimizer.analysis.metrics import Metrics


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
