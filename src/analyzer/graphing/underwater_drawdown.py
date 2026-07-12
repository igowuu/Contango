"""
Chart 5: Underwater Plot (drawdown over time).

Answers: "How much pain, and for how long?"

Deliberately separate from chart 4: an equity curve can look fine while
visually compressing a long, brutal underwater period. This plots
drawdown-from-running-peak over time instead of raw account value, answering
"could I have actually stomached holding this?" for the same shortlist used
in chart 4.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]


def _compute_underwater_series(
    equity_curve: tuple[tuple[int, float], ...],
) -> tuple[list[pd.Timestamp], list[float]]:
    """
    Converts a raw equity curve into a (timestamps, drawdown_pct) series,
    where drawdown_pct is the percent decline from the running peak at each point.
    """
    timestamps: list[pd.Timestamp] = []
    drawdowns: list[float] = []
    peak: float | None = None

    for t, v in equity_curve:
        peak = v if peak is None else max(peak, v)
        drawdown = (v - peak) / peak if peak else 0.0
        timestamps.append(pd.to_datetime(t, unit="ms"))
        drawdowns.append(drawdown)

    return timestamps, drawdowns


def build_underwater_plot(
    df: pd.DataFrame,
    experiment_ids: list[str] | None = None,
    top_n: int = 8,
    rank_by: str = "calmar_ratio",
) -> go.Figure:
    """
    Builds an underwater plot (drawdown-from-peak over time) for a shortlist of experiments.

    Args:
        df: Tidy experiment DataFrame.
        experiment_ids: Explicit list of experiment_id values to plot. If None,
            the top `top_n` experiments ranked by `rank_by` (descending) are used.
        top_n: Number of experiments to include when experiment_ids is None.
        rank_by: Metric column to rank by when auto-selecting the shortlist.

    Returns:
        A plotly Figure.
    """
    plot_df = df.dropna(subset=["equity_curve"]).copy()

    if experiment_ids is not None:
        plot_df = plot_df[plot_df["experiment_id"].isin(experiment_ids)]
    else:
        plot_df = plot_df.sort_values(rank_by, ascending=False).head(top_n)

    fig = go.Figure()
    for _, row in plot_df.iterrows():
        timestamps, drawdowns = _compute_underwater_series(row["equity_curve"])
        fig.add_trace(  # type: ignore[unknownMemberType]
            go.Scatter(x=timestamps, y=drawdowns, mode="lines", name=row["experiment_id"], fill="tozeroy")
        )

    fig.update_layout(  # type: ignore[unknownMemberType]
        title="Underwater Plot — Drawdown From Peak Over Time",
        xaxis_title="Time",
        yaxis_title="Drawdown From Peak",
        yaxis_tickformat=".1%",
        template="plotly_white",
    )
    return fig
