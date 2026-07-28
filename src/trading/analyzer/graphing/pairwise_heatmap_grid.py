# trading/analyzer/graphing/pairwise_heatmap_grid.py — part of Contango, a parameterized backtesting & execution framework
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

import math

import pandas as pd
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]
from plotly.subplots import make_subplots   # type: ignore[unknownMemberType]


def build_pairwise_heatmap_grid(
    df: pd.DataFrame,
    param_x: str,
    param_y: str,
    facet_param: str,
    target_metric: str = "calmar_ratio",
    max_cols: int = 4,
) -> go.Figure:
    """
    Builds a grid of 2D heatmaps: param_x vs. param_y, one panel per unique
    value of facet_param.

    Args:
        df: Experiment DataFrame.
        param_x: Parameter column for the heatmap x-axis.
        param_y: Parameter column for the heatmap y-axis.
        facet_param: Parameter column to facet panels by.
        target_metric: Metric column used for cell color. Defaults to
                       "calmar_ratio" (risk-adjusted, better for spotting robust regions
                       than raw return).
        max_cols: Maximum number of panels per row before wrapping.

    Returns:
        A plotly Figure with one subplot per facet_param value.
    """
    plot_df = df.dropna(subset=[param_x, param_y, facet_param, target_metric])
    facet_values = sorted(plot_df[facet_param].unique())

    n = len(facet_values)
    cols = min(n, max_cols)

    if cols == 0:
        raise ValueError("No trades were made! Could not graph the pairwise heatmap grid.")

    rows = math.ceil(n / cols)

    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[f"{facet_param}={v}" for v in facet_values],
        shared_xaxes=True,
        shared_yaxes=True,
    )

    zmin, zmax = plot_df[target_metric].min(), plot_df[target_metric].max()

    for i, val in enumerate(facet_values):
        mask: pd.Series = plot_df[facet_param] == val
        subset: pd.DataFrame = plot_df[mask]
        pivot = subset.pivot_table(index=param_y, columns=param_x, values=target_metric, aggfunc="mean")

        fig.add_trace(  # type: ignore[unknownMemberType]
            go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=pivot.index,
                coloraxis="coloraxis",
            ),
            row=(i // cols) + 1,
            col=(i % cols) + 1,
        )

    fig.update_layout(  # type: ignore[unknownMemberType]
        title=f"Pairwise Heatmap Grid — {param_x} × {param_y}, faceted by {facet_param} (color = {target_metric})",
        coloraxis={"colorscale": "RdYlGn", "cmin": zmin, "cmax": zmax},
        height=320 * rows,
    )
    return fig
