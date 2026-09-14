from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from contango.trading.analysis.graphing.downsample import downsample_curve
from contango.trading.analysis.graph_type import GraphType
from contango.trading.analysis.graph_config import GraphConfig
from contango.trading.analysis.graph_registry import register_graph


def _compute_underwater_series(
    equity_curve: tuple[tuple[int, float], ...],
    max_points: int = 1500,
) -> tuple[list[pd.Timestamp], list[float]]:
    """
    Converts a raw equity curve into a (timestamps, drawdown_pct) series,
    where drawdown_pct is the percent decline from the running peak at each point.
    """
    peak: float | None = None
    drawdown_curve: list[tuple[int, float]] = []

    for t, v in equity_curve:
        peak = v if peak is None else max(peak, v)
        drawdown = (v - peak) / peak if peak else 0.0
        drawdown_curve.append((t, drawdown))

    curve = downsample_curve(tuple(drawdown_curve), max_points)

    timestamps = [pd.to_datetime(t, unit="ms") for t, _ in curve]
    drawdowns = [d for _, d in curve]
    return timestamps, drawdowns


@dataclass(frozen=True, slots=True)
class UnderwaterDrawdownConfig(GraphConfig):
    """
    A graph configuration specific to the underwater drawdown graph.

    Attributes:
        experiment_ids: The list of experiment_id values to plot.
        top_n: The top amount of experiments to plot when auto-ranking.
        rank_by: The name for the targeted metric to rank by when auto-selecting
                 the shortlist.
        max_points_per_curve: The maximum amount of points kept per curve after
                              downsampling.
    """
    experiment_ids: list[str] | None = None
    top_n: int = 8
    rank_by: str = "calmar_ratio"
    max_points_per_curve: int = 1500


@register_graph("underwater_drawdown")
class UnderwaterDrawdown(GraphType[UnderwaterDrawdownConfig]):
    """
    A graph type that shows drawdown-from-peak over time for a shortlist of experiments.
    """
    def build(self, df: pd.DataFrame) -> go.Figure:
        """
        Builds an underwater plot (drawdown-from-peak over time) for a shortlist
        of experiments.

        Args:
            df: The experiment DataFrame.

        Returns:
            A plotly Figure.
        """
        plot_df = df.dropna(subset=["equity_curve"]).copy()

        if self.config.experiment_ids is not None:
            plot_df = plot_df[plot_df["experiment_id"].isin(self.config.experiment_ids)]
        else:
            plot_df = (
                plot_df.sort_values(self.config.rank_by, ascending=False)
                .head(self.config.top_n)
                .reset_index(drop=True)
            )

        fig = go.Figure()
        for _, row in plot_df.iterrows():
            timestamps, drawdowns = _compute_underwater_series(row["equity_curve"], self.config.max_points_per_curve)
            fig.add_trace(  # type: ignore[unknownMemberType]
                go.Scatter(
                    x=timestamps,
                    y=drawdowns,
                    mode="lines",
                    name=row["name"],
                    fill="tozeroy",
                )
            )

        fig.update_layout(  # type: ignore[unknownMemberType]
            title="Underwater plot: drawdown from peak over time",
            xaxis_title="Time",
            yaxis_title="Drawdown From Peak",
            yaxis_tickformat=".1%",
        )
        return fig
