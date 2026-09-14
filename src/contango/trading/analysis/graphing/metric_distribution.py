from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import plotly.express as px  # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import register_graph


@dataclass(frozen=True, slots=True)
class MetricDistributionConfig(GraphConfig):
    """
    A graph configuration specific to the metric distribution graph.

    Attributes:
        group_by: The column to group by, including a parameter column, or a
                  version of one for continuous parameters with various
                  distinct values.
        target_metric: The name for the targeted metric to graph.
        plot_type: The distribution plot style, either "box" or "violin".
    """
    group_by: str
    target_metric: str = "total_return"
    plot_type: str = "box"


@register_graph("metric_distribution")
class MetricDistribution(GraphType[MetricDistributionConfig]):
    """
    A graph type that shows the distribution of a metric grouped by a parameter.
    """
    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds a distribution plot of target_metric grouped by group_by.

        Args:
            df: The experiment DataFrame.

        Returns:
            A plotly Figure.
        """
        plot_df = df.dropna(subset=[self.config.group_by, self.config.target_metric]).copy()
        plot_df[self.config.group_by] = plot_df[self.config.group_by].astype(str)

        fig_fn = px.box if self.config.plot_type == "box" else px.violin  # type: ignore[unknownMemberType]
        fig = fig_fn(
            plot_df,
            x=self.config.group_by,
            y=self.config.target_metric,
            points="all",
            title=f"Distribution of {self.config.target_metric} by {self.config.group_by}",
            labels={self.config.group_by: self.config.group_by, self.config.target_metric: self.config.target_metric},
        )
        fig.update_layout()  # type: ignore[unknownMemberType]
        return fig
