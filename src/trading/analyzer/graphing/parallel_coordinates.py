# trading/analyzer/graphing/parallel_coordinates.py — part of Contango, a parameterized backtesting & execution framework
# Copyright (C) 2026  Jacob Taylor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

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
        df: Experiment DataFrame.
        param_columns: Parameter columns to include as axes.
        target_metric: Metric column used as the final axis and the color scale.
        sample_size: If the experiment count is large (hundreds to thousands of
                     combos), parallel coordinates gets visually dense fast.

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
