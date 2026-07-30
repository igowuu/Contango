# trading/optimizer/experiments/backtest_experiment_grid.py — part of Contango, a parameterized backtesting & execution framework
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

from itertools import product
from typing import Any

from contango.trading.optimizer.experiments.backtest_experiment import BacktestExperiment


class BacktestExperimentGrid:
    """
    Allows for `BacktestExperiment` instances to be tested upon a variety of parameters without
    the use of nested loops.
    """
    def __init__(self, base_experiment: BacktestExperiment, param_space: dict[str, list[Any]]):
        """
        Initializes `BacktestExperimentGrid`.
        
        Args:
            base_experiment: The base experiment to test through the grid.
            param_space: A dictionary of parameter names matching to the desired values to test for the parameter.
        """
        self.base = base_experiment
        self.param_space = param_space

    def generate(self) -> list[BacktestExperiment]:
        """
        Generates a list of `BacktestExperiment` instances with the given parameter space at initialization.
        """
        keys = list(self.param_space.keys())
        values = list(self.param_space.values())

        experiments: list[BacktestExperiment] = []

        for combo in product(*values):
            params = dict(zip(keys, combo))

            experiments.append(
                BacktestExperiment(
                    strategy_factory=self.base.strategy_factory,
                    parameters=params,
                    dataset=self.base.dataset,
                    config=self.base.config
                )
            )

        return experiments
