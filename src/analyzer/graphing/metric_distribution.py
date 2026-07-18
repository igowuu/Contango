from __future__ import annotations

import pandas as pd
import plotly.express as px # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]


def build_metric_distribution(
    df: pd.DataFrame,
    group_by: str,
    target_metric: str = "total_return",
    plot_type: str = "box",
) -> go.Figure:
    """
    Builds a distribution plot of `target_metric` grouped by `group_by`.

    Args:
        df: Tidy experiment DataFrame.
        group_by: Column to group by — typically a parameter column, or a
            pre-binned version of one for continuous parameters with many
            distinct values.
        target_metric: Metric column to show the distribution of.
        plot_type: "box" (default) or "violin".

    Returns:
        A plotly Figure.
    """
    plot_df = df.dropna(subset=[group_by, target_metric]).copy()
    plot_df[group_by] = plot_df[group_by].astype(str)

    fig_fn = px.box if plot_type == "box" else px.violin    # type: ignore[unknownMemberType]
    fig = fig_fn(
        plot_df,
        x=group_by,
        y=target_metric,
        points="all",
        title=f"Distribution of {target_metric} by {group_by}",
        labels={group_by: group_by, target_metric: target_metric},
    )
    fig.update_layout(template="plotly_white")  # type: ignore[unknownMemberType]
    return fig
