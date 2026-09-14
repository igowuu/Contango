from __future__ import annotations

import math
from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]
from plotly.subplots import make_subplots   # type: ignore[unknownMemberType]

from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import register_graph


@dataclass(frozen=True, slots=True)
class PairwiseHeatmapGridConfig(GraphConfig):
    """
    A graph configuration specific to the pairwise heatmap grid graph.

    Attributes:
        param_x: The parameter column for the heatmap x-axis.
        param_y: The parameter column for the heatmap y-axis.
        facet_param: The parameter column to facet panels by.
        target_metric: The name for the targeted metric used for cell color.
        max_cols: The maximum amount of panels per row before wrapping.
    """
    param_x: str
    param_y: str
    facet_param: str
    target_metric: str = "calmar_ratio"
    max_cols: int = 4


@register_graph("pairwise_heatmap_grid")
class PairwiseHeatmapGrid(GraphType[PairwiseHeatmapGridConfig]):
    """
    A graph type that shows a grid of 2D heatmaps, one panel per facet value.
    """
    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds a grid of 2D heatmaps: param_x vs. param_y, one panel per unique
        value of facet_param.

        Args:
            df: The experiment DataFrame.

        Returns:
            A plotly Figure with one subplot per facet_param value.
        """
        plot_df = df.dropna(subset=[self.config.param_x, self.config.param_y, self.config.facet_param, self.config.target_metric])
        facet_values = sorted(plot_df[self.config.facet_param].unique())

        n = len(facet_values)
        cols = min(n, self.config.max_cols)

        if cols == 0:
            raise ValueError("No trades were made! Could not graph the pairwise heatmap grid.")

        rows = math.ceil(n / cols)

        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=[f"{self.config.facet_param}={v}" for v in facet_values],
            shared_xaxes=True,
            shared_yaxes=True,
        )

        zmin, zmax = plot_df[self.config.target_metric].min(), plot_df[self.config.target_metric].max()

        for i, val in enumerate(facet_values):
            mask: pd.Series = plot_df[self.config.facet_param] == val
            subset: pd.DataFrame = plot_df[mask]
            pivot = subset.pivot_table(
                index=self.config.param_y,
                columns=self.config.param_x,
                values=self.config.target_metric,
                aggfunc="mean",
            )

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
            title=f"Pairwise Heatmap Grid: {self.config.param_x} × {self.config.param_y}, faceted by {self.config.facet_param} (color = {self.config.target_metric})",
            coloraxis={"colorscale": "RdYlGn", "cmin": zmin, "cmax": zmax},
            height=320 * rows,
        )
        return fig
