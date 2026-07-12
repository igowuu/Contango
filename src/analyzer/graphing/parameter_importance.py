"""
Chart 2a: Parameter Importance Ranking.

Answers: "Which knobs actually matter?"

For each swept parameter, computes an eta-squared style sensitivity score
against a target metric (how much of the metric's total variance is explained
by grouping on that parameter alone). Plotted as a sorted horizontal bar
chart. This tells you where to spend your visual attention in the following
two charts (2b, 2c) and which parameters can be safely averaged over.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]


def compute_parameter_importance(
    df: pd.DataFrame,
    target_metric: str,
    param_columns: list[str],
) -> pd.DataFrame:
    """
    Scores each parameter's importance to `target_metric` using an
    eta-squared style measure: the share of total variance in the metric
    explained by grouping on that parameter's values.

    Args:
        df: Experiment DataFrame.
        target_metric: The metric column to explain (e.g. "calmar_ratio").
        param_columns: Parameter columns to score, typically from
            `data_prep.get_param_columns`.

    Returns:
        DataFrame with columns ["parameter", "importance"], sorted descending.
    """
    plot_df = df.dropna(subset=[target_metric])
    grand_mean = plot_df[target_metric].mean()
    ss_total = ((plot_df[target_metric] - grand_mean) ** 2).sum()

    scores: list[dict[str, str | float]] = []
    for param in param_columns:
        group_stats = plot_df.groupby(param)[target_metric].agg(["mean", "count"])
        ss_between = (group_stats["count"] * (group_stats["mean"] - grand_mean) ** 2).sum()
        importance = float(ss_between / ss_total) if ss_total > 0 else 0.0
        scores.append({"parameter": param, "importance": importance})

    return pd.DataFrame(scores).sort_values("importance", ascending=False).reset_index(drop=True)


def build_parameter_importance(
    df: pd.DataFrame,
    param_columns: list[str],
    target_metric: str = "calmar_ratio",
) -> go.Figure:
    """
    Builds the parameter importance bar chart.

    Args:
        df: Tidy experiment DataFrame.
        param_columns: Parameter columns to score.
        target_metric: Metric to explain. Defaults to "calmar_ratio" (risk-adjusted).

    Returns:
        A plotly Figure.
    """
    importance_df = compute_parameter_importance(df, target_metric, param_columns)

    fig = px.bar(   # type: ignore[unknownMemberType]
        importance_df,
        x="importance",
        y="parameter",
        orientation="h",
        title=f"Parameter Importance — Sensitivity of {target_metric} to Each Parameter",
        labels={"importance": "Relative Importance (eta²)", "parameter": "Parameter"},
    )
    fig.update_layout(template="plotly_white", yaxis={"categoryorder": "total ascending"})  # type: ignore[unknownMemberType]
    return fig
