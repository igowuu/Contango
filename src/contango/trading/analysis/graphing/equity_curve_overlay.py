from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graphing.downsample import downsample_curve
from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import register_graph


@dataclass(frozen=True, slots=True)
class EquityCurveConfig(GraphConfig):
    """
    A graph configuration specific to the equity curve graph.
    
    Attributes:
        target_metric: The name for the targeted metric to graph.
        top_n: The top amount of values to keep for the graph.
        max_downsample_points: The maximum amount of downsample points to graph.
                               Changing this value directly alters performance; however,
                               it should usually not be changed for most uses.
    """
    target_metric: str
    top_n: int
    max_downsample_points: int = 1500


@register_graph("equity_curve_overlay")
class EquityCurveOverlay(GraphType[EquityCurveConfig]):
    """
    A graph type that shows the equity over time for a specified metric.
    """
    def __init__(self, config: EquityCurveConfig) -> None:
        super().__init__(config)

    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds an equity curve overlay for the top top_n experiments.

        Args:
            df: The experiment DataFrame.

        Returns:
            A plotly Figure.
        """
        plot_df = (
            df.dropna(subset=["equity_curve"])
            .sort_values(self.config.target_metric, ascending=False)
            .head(self.config.top_n)
            .reset_index(drop=True)
        )

        fig = go.Figure()
        for _, row in plot_df.iterrows():
            curve = downsample_curve(row["equity_curve"], self.config.max_downsample_points)
            timestamps: list[pd.Timestamp] = [pd.to_datetime(t, unit="ms") for t, _ in curve]
            values = [v for _, v in curve]
            fig.add_trace(  # type: ignore[unknownMemberType]
                go.Scatter(
                    x=timestamps,
                    y=values,
                    mode="lines",
                    name=f"{row['name']} ({self.config.target_metric}={row[self.config.target_metric]:.2f})",
                )
            )

        fig.update_layout(  # type: ignore[unknownMemberType]
            title=f"Equity Curve Overlay: top {len(plot_df)} by {self.config.target_metric}",
            xaxis_title="Time",
            yaxis_title="Account Value (USD)",
        )
        return fig
