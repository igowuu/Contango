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
