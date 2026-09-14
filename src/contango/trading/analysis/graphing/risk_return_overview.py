from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import plotly.express as px  # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import register_graph


@dataclass(frozen=True, slots=True)
class RiskReturnOverviewConfig(GraphConfig):
    """
    A graph configuration specific to the risk/return overview graph.

    Attributes:
        color_by: The column to color points by.
    """
    color_by: str = "calmar_ratio"


@register_graph("risk_return_overview")
class RiskReturnOverview(GraphType[RiskReturnOverviewConfig]):
    """
    A graph type that shows the risk/return overview scatter plot.
    """
    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds the risk/return overview scatter plot.

        Args:
            df: The experiment DataFrame.

        Returns:
            A plotly Figure.
        """
        plot_df = df.dropna(subset=["annual_return", "sharpe_ratio", "max_drawdown", self.config.color_by]).copy()
        plot_df["drawdown_severity"] = plot_df["max_drawdown"].abs()

        is_numeric_color = pd.api.types.is_numeric_dtype(plot_df[self.config.color_by])

        fig = px.scatter(   # type: ignore[unknownMemberType]
            plot_df,
            x="annual_return",
            y="sharpe_ratio",
            size="drawdown_severity",
            color=self.config.color_by,
            hover_name="name",
            hover_data={
                "max_drawdown": ":.2%",
                "calmar_ratio": ":.2f",
                "trade_count": True,
                "drawdown_severity": False,
            },
            color_continuous_scale="Viridis" if is_numeric_color else None,
            title="Risk return overview: annual return vs. sharpe ratio, bubble size = drawdown severity",
            labels={"annual_return": "Annual Return (CAGR)", "sharpe_ratio": "Sharpe Ratio"},
        )
        fig.update_layout(xaxis_tickformat=".1%")  # type: ignore[unknownMemberType]
        return fig
