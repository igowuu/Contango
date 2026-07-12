from __future__ import annotations

from itertools import product
from typing import Any

from optimizer.experiments.backtest_experiment import BacktestExperiment


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
