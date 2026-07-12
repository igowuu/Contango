"""
Chart 6: Trade Quality Scatter.

Answers: "Why did it make money?"

x = win_rate, y = profit_factor (or expectancy), bubble size = trade_count.
Trade count matters here — a great expectancy on a dozen trades is noise, not
edge. This reveals the mechanism behind the returns: grinding singles (high
win rate, low average win) vs. swinging for rare big wins (low win rate, high
profit factor). Two strategies can post identical total return with entirely
different, non-interchangeable risk profiles here.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]


def build_trade_quality_scatter(
    df: pd.DataFrame,
    y_metric: str = "profit_factor",
    color_by: str = "calmar_ratio",
) -> go.Figure:
    """
    Builds the trade-quality scatter plot.

    Args:
        df: Tidy experiment DataFrame.
        y_metric: Metric for the y-axis. "profit_factor" (default) or "expectancy"
            both work well alongside win_rate.
        color_by: Column to color points by. Defaults to "calmar_ratio".

    Returns:
        A plotly Figure.
    """
    plot_df = df.dropna(subset=["win_rate", y_metric, "trade_count", color_by]).copy()

    fig = px.scatter(   # type: ignore[unknownMemberType]
        plot_df,
        x="win_rate",
        y=y_metric,
        size="trade_count",
        color=color_by,
        hover_name="experiment_id",
        title=f"Trade Quality — Win Rate vs. {y_metric} (bubble size = trade count)",
        labels={"win_rate": "Win Rate"},
    )
    fig.update_layout(template="plotly_white", xaxis_tickformat=".0%")  # type: ignore[unknownMemberType]
    return fig
