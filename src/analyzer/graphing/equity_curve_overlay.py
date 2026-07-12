"""
Chart 4: Equity Curve Overlay.

Answers: "What does the ride actually look like?"

Operates on a shortlist only (top N by default, or an explicit list of
experiment_ids) — this chart gets unreadable past ~8 lines. Shows raw account
value over time so you can visually catch the difference between a steady
climb, one lucky spike, or a flat-then-pop pattern that summary stats alone
don't reveal.
"""
from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]


def build_equity_curve_overlay(
    df: pd.DataFrame,
    experiment_ids: list[str] | None = None,
    top_n: int = 8,
    rank_by: str = "calmar_ratio",
) -> go.Figure:
    """
    Builds an overlaid line chart of equity curves for a shortlist of experiments.

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
        curve = row["equity_curve"]
        timestamps = [pd.to_datetime(t, unit="ms") for t, _ in curve]   # type: ignore[unknownMemberType]
        values = [v for _, v in curve]
        fig.add_trace(go.Scatter(x=timestamps, y=values, mode="lines", name=row["experiment_id"]))  # type: ignore[unknownMemberType]

    fig.update_layout(  # type: ignore[unknownMemberType]
        title="Equity Curve Overlay — Shortlisted Candidates",
        xaxis_title="Time",
        yaxis_title="Account Value (USD)",
        template="plotly_white",
    )
    return fig
