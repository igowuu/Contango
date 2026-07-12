"""
Chart 2b: Parallel Coordinates Plot.

Answers: "What do the full parameter combinations that work actually look like?"

One axis per swept parameter plus a final axis for the target metric. Each
line is one experiment, colored by outcome. Look for lines that share color
converging through a consistent narrow band on 2-3 axes (a real interaction
effect) vs. good lines scattered randomly across every axis (no coherent
parameter story — likely noise/overfit). This is the only chart in the flow
that shows all swept dimensions simultaneously.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]


def build_parallel_coordinates(
    df: pd.DataFrame,
    param_columns: list[str],
    target_metric: str = "calmar_ratio",
    sample_size: int | None = None,
) -> go.Figure:
    """
    Builds the parallel coordinates plot across all swept parameters.

    Args:
        df: Tidy experiment DataFrame.
        param_columns: Parameter columns to include as axes.
        target_metric: Metric column used as the final axis and the color scale.
        sample_size: If the experiment count is large (hundreds to thousands of
            combos), parallel coordinates gets visually dense fast. Pass a
            sample_size to randomly subsample rows for a readable plot; leave
            as None to plot everything.

    Returns:
        A plotly Figure.
    """
    plot_df = df.dropna(subset=param_columns + [target_metric]).copy()

    if sample_size is not None and len(plot_df) > sample_size:
        plot_df = plot_df.sample(sample_size, random_state=42)

    dimensions = param_columns + [target_metric]

    fig = px.parallel_coordinates(  # type: ignore[unknownMemberType]
        plot_df,
        dimensions=dimensions,
        color=target_metric,
        color_continuous_scale=px.colors.diverging.RdYlGn,
        title=f"Parameter Combinations — Parallel Coordinates (colored by {target_metric})",
    )
    fig.update_layout(template="plotly_white")  # type: ignore[unknownMemberType]
    return fig
