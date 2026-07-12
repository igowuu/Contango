"""
Chart 1: Risk/Return Overview Scatter.

Answers: "Is anything here even worth looking at?"

Every experiment is one point: annualized return vs. Sharpe ratio, with bubble
size showing drawdown severity (bigger = worse) and color showing a chosen
grouping. This is the triage step — you're looking for a cluster in the
upper-right with small bubbles. Scattered points with no cluster mean this
strategy family likely has no real edge; stop here for those before spending
time downstream.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]


def build_risk_return_overview(
    df: pd.DataFrame,
    color_by: str = "calmar_ratio",
) -> go.Figure:
    """
    Builds the risk/return overview scatter plot.

    Args:
        df: Experiment DataFrame from `data_prep.results_to_dataframe`.
        color_by: Column to color points by. Defaults to "calmar_ratio" so
            warmer colors highlight the best risk-adjusted performers. Pass a
            parameter column name instead to color by a swept parameter.

    Returns:
        A plotly Figure.
    """
    plot_df = df.dropna(subset=["annual_return", "sharpe_ratio", "max_drawdown", color_by]).copy()
    plot_df["drawdown_severity"] = plot_df["max_drawdown"].abs()

    is_numeric_color = pd.api.types.is_numeric_dtype(plot_df[color_by])

    fig = px.scatter(   # type: ignore[unknownMemberType]
        plot_df,
        x="annual_return",
        y="sharpe_ratio",
        size="drawdown_severity",
        color=color_by,
        hover_name="experiment_id",
        hover_data={
            "max_drawdown": ":.2%",
            "calmar_ratio": ":.2f",
            "trade_count": True,
            "drawdown_severity": False,
        },
        color_continuous_scale="Viridis" if is_numeric_color else None,
        title="Risk/Return Overview — Annual Return vs. Sharpe Ratio (bubble size = drawdown severity)",
        labels={"annual_return": "Annual Return (CAGR)", "sharpe_ratio": "Sharpe Ratio"},
    )
    fig.update_layout(template="plotly_white", xaxis_tickformat=".1%")  # type: ignore[unknownMemberType]
    return fig
