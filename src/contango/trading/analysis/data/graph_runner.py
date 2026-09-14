# graph_runner.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Union
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import GRAPH_REGISTRY
from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graphing.equity_curve_overlay import EquityCurveConfig
from contango.trading.analysis.graphing.pairwise_heatmap_grid import PairwiseHeatmapGridConfig
from contango.trading.analysis.graphing.parallel_coordinates import ParallelCoordinatesConfig
from contango.trading.analysis.graphing.parameter_importance import ParameterImportanceConfig
from contango.trading.analysis.graphing.risk_return_overview import RiskReturnOverviewConfig
from contango.trading.analysis.graphing.trade_quality_scatter import TradeQualityScatterConfig
from contango.trading.analysis.graphing.underwater_drawdown import UnderwaterDrawdownConfig

from contango.trading.analysis.data.graphing_experiment import GraphingExperiment
from contango.trading.analysis.data.data_prep import results_to_dataframe, get_param_columns
from contango.trading.analysis.graphing.parameter_importance import compute_parameter_importance


GraphConfigFactory = Callable[[pd.DataFrame], GraphConfig]


@dataclass(frozen=True, slots=True)
class GraphSpec:
    """
    A named graph type paired with its config — either a concrete config, or a
    factory that builds one once the experiment DataFrame is available.
    """
    name: str
    config: Union[GraphConfig, GraphConfigFactory]


def _resolve(config: Union[GraphConfig, GraphConfigFactory], df: pd.DataFrame) -> GraphConfig:
    if isinstance(config, GraphConfig):
        return config
    return config(df)

def _default_heatmap_grid_config(df: pd.DataFrame) -> PairwiseHeatmapGridConfig:
    target_metric = "calmar_ratio"
    param_columns = get_param_columns(df)

    if len(param_columns) < 3:
        raise ValueError(
            f"pairwise_heatmap_grid needs at least 3 swept parameters, found {len(param_columns)}: {param_columns}"
        )

    importance_df = compute_parameter_importance(df, target_metric, param_columns)
    top_3 = importance_df["parameter"].head(3).tolist()

    return PairwiseHeatmapGridConfig(
        param_x=top_3[0],
        param_y=top_3[1],
        facet_param=top_3[2],
        target_metric=target_metric,
    )


DEFAULT_GRAPH_SPECS: list[GraphSpec] = [
    GraphSpec("equity_curve_overlay", EquityCurveConfig(target_metric="calmar_ratio", top_n=10)),
    GraphSpec("risk_return_overview", RiskReturnOverviewConfig()),
    GraphSpec("trade_quality_scatter", TradeQualityScatterConfig()),
    GraphSpec("underwater_drawdown", UnderwaterDrawdownConfig()),
    GraphSpec(
        "parameter_importance",
        lambda df: ParameterImportanceConfig(param_columns=get_param_columns(df)),
    ),
    GraphSpec(
        "parallel_coordinates",
        lambda df: ParallelCoordinatesConfig(param_columns=get_param_columns(df)),
    ),
    GraphSpec(
        "pairwise_heatmap_grid",
        _default_heatmap_grid_config,
    ),
]

DARK_GRAY_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#252526",
        font=dict(color="#d4d4d4"),
        xaxis=dict(gridcolor="#444444", zerolinecolor="#666666"),
        yaxis=dict(gridcolor="#444444", zerolinecolor="#666666"),
    )
)


class GraphRunner:
    """
    Manages a set of graph specs, instantiating them once the experiment
    DataFrame is available.
    """
    def __init__(
        self, 
        specs: list[GraphSpec] = DEFAULT_GRAPH_SPECS,
        template: go.layout.Template | None = DARK_GRAY_TEMPLATE
    ) -> None:
        """
        Initializes `GraphRunner`.
        
        Args:
            specs: A list of specs for each graph type.
            template: The plotly template for all graphs to follow.
        """
        self._specs: list[GraphSpec] = list(specs)
        self._graphs: list[GraphType[Any]] = []
        self._template = template

    @property
    def graphs(self) -> list[GraphType[Any]]:
        """
        The currently active graph instances (empty until `build_all` has run
        at least once, since some configs depend on the data).
        """
        return list(self._graphs)

    def add_graph(self, name: str, config: Union[GraphConfig, GraphConfigFactory]) -> None:
        """
        Registers a graph spec to be instantiated on the next `build_all`.
        """
        if name not in GRAPH_REGISTRY:
            raise KeyError(f"No graph registered under '{name}'. Known: {list(GRAPH_REGISTRY)}")
        self._specs.append(GraphSpec(name, config))

    def remove_graph(self, graph: GraphType[Any]) -> None:
        """
        Removes all graphs by instance.
        """
        self._graphs.remove(graph)
        self._specs = [s for s in self._specs if s.name != graph.graph_name]

    def remove_by_name(self, name: str) -> None:
        """
        Removes all graphs with the same name.
        """
        self._specs = [s for s in self._specs if s.name != name]
        self._graphs = [g for g in self._graphs if g.graph_name != name]

    def build_all(self, experiments: list[GraphingExperiment]) -> dict[str, go.Figure]:
        """
        Resolves every spec's config against the data, instantiates the
        graphs, and builds all of their figures.
        """
        df = results_to_dataframe(experiments)

        self._graphs = []
        for spec in self._specs:
            config = _resolve(spec.config, df)
            graph_cls = GRAPH_REGISTRY[spec.name]
            self._graphs.append(graph_cls(config))

        figures = {graph.graph_name: graph.build(df) for graph in self._graphs}

        if self._template is not None:
            for fig in figures.values():
                fig.update_layout(template=self._template)  # type: ignore[unknownMemberType]

        return figures

    def write_to_html(self, figures: dict[str, go.Figure], output_dir: Path | str) -> dict[str, Path]:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        written: dict[str, Path] = {}
        for name, fig in figures.items():
            file_path = output_path / f"{name}.html"
            fig.write_html(file_path)   # type: ignore[unknownMemberType]
            written[name] = file_path

        return written
