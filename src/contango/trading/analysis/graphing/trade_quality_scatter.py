from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import plotly.express as px  # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import register_graph


@dataclass(frozen=True, slots=True)
class TradeQualityScatterConfig(GraphConfig):
    """
    A graph configuration specific to the trade quality scatter graph.

    Attributes:
        y_metric: The metric for the y-axis.
        color_by: The column to color points by, defaults to "calmar_ratio".
    """
    y_metric: str = "profit_factor"
    color_by: str = "calmar_ratio"


@register_graph("trade_quality_scatter")
class TradeQualityScatter(GraphType[TradeQualityScatterConfig]):
    """
    A graph type that shows the trade-quality scatter plot.
    """
    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds the trade-quality scatter plot.

        Args:
            df: The experiment DataFrame.

        Returns:
            A plotly Figure.
        """
        plot_df = df.dropna(subset=["win_rate", self.config.y_metric, "trade_count", self.config.color_by]).copy()

        fig = px.scatter(   # type: ignore[unknownMemberType]
            plot_df,
            x="win_rate",
            y=self.config.y_metric,
            size="trade_count",
            color=self.config.color_by,
            hover_name="name",
            title=f"Trade quality: win rate vs. {self.config.y_metric}, bubble size = trade count",
            labels={"win_rate": "Win Rate"},
        )
        fig.update_layout(xaxis_tickformat=".0%")  # type: ignore[unknownMemberType]
        return fig
