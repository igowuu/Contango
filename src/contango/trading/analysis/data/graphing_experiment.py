from __future__ import annotations

from typing import NamedTuple, Mapping, Any

from contango.trading.metrics.metrics import Metrics
from contango.runners.grid.grid_search_runner import ExperimentResult


class GraphingExperiment(NamedTuple):
    """
    A single experiment when graphing.

    Attributes:
        name: The name for the experiment.
        metrics: The metrics for the experiment.
        parameters: A dict mapping strings to the parameters for the experiment.
    """
    name: str
    metrics: Metrics
    parameters: Mapping[str, Any]


    @classmethod
    def from_experiment_result(cls, result: ExperimentResult) -> GraphingExperiment:
        """
        Returns a `GraphingExperiment` from an `ExperimentResult`.
        """
        return GraphingExperiment(result.label, result.metrics, result.kwargs)

    @classmethod
    def from_experiment_results(cls, results: list[ExperimentResult]) -> list[GraphingExperiment]:
        """
        Returns a list of `GraphingExperiment` instances from a list of `ExperimentResult` instances.
        """
        return [cls.from_experiment_result(result) for result in results]

    def __repr__(self) -> str:
        """
        Returns a string representation of the experiment.
        """
        return (
            f"Name: {self.name}\n"
            f"Parameters: {dict(self.parameters)}\n"
            f"Metrics: \n{self.metrics}\n"
        )
