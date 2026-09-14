from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import plotly.express as px  # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import register_graph


@dataclass(frozen=True, slots=True)
class ParallelCoordinatesConfig(GraphConfig):
    """
    A graph configuration specific to the parallel coordinates graph.

    Attributes:
        param_columns: The parameter columns to include as axes.
        target_metric: The name for the targeted metric used as the final axis
                       and the color scale.
        sample_size: The maximum amount of experiments to plot.
    """
    param_columns: list[str]
    target_metric: str = "calmar_ratio"
    sample_size: int | None = None


@register_graph("parallel_coordinates")
class ParallelCoordinates(GraphType[ParallelCoordinatesConfig]):
    """
    A graph type that shows parameter combinations across all swept parameters.
    """
    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds the parallel coordinates plot across all swept parameters.

        Args:
            df: The experiment DataFrame.

        Returns:
            A plotly Figure.
        """
        plot_df = df.dropna(subset=self.config.param_columns + [self.config.target_metric]).copy()

        if self.config.sample_size is not None and len(plot_df) > self.config.sample_size:
            plot_df = plot_df.sample(self.config.sample_size, random_state=42)

        dimensions = self.config.param_columns + [self.config.target_metric]

        fig = px.parallel_coordinates(  # type: ignore[unknownMemberType]
            plot_df,
            dimensions=dimensions,
            color=self.config.target_metric,
            color_continuous_scale=px.colors.diverging.RdYlGn,
            title=f"Parameter Combinations: Parallel Coordinates colored by {self.config.target_metric}",
        )
        fig.update_layout()  # type: ignore[unknownMemberType]
        return fig
