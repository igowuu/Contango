# trading/analyzer/graphing/underwater_drawdown.py — part of Contango, a parameterized backtesting & execution framework
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
    max_traces: int = 40,
) -> go.Figure:
    """
    Builds an underwater plot (drawdown-from-peak over time) for a shortlist of experiments.

    Args:
        df: Experiment DataFrame.
        experiment_ids: List of experiment_id values to plot. If given, all of
                        them are plotted and no slider is added (the set is fixed).
        top_n: How many traces are visible when the chart first loads (auto-rank mode only).
        rank_by: Metric column to rank by when auto-selecting the shortlist.
        max_traces: How many experiments get a trace at all, i.e. the slider's max
                    (auto-rank mode only; ignored when experiment_ids is given).

    Returns:
        A plotly Figure.
    """
    plot_df = df.dropna(subset=["equity_curve"]).copy()
    use_slider = experiment_ids is None

    if not use_slider:
        plot_df = plot_df[plot_df["experiment_id"].isin(experiment_ids)]
    else:
        plot_df = (
            plot_df.sort_values(rank_by, ascending=False)
            .head(max_traces)
            .reset_index(drop=True)
        )

    n_traces = len(plot_df)
    default_top_n = min(top_n, n_traces)

    fig = go.Figure()
    for i, (_, row) in enumerate(plot_df.iterrows()):
        timestamps, drawdowns = _compute_underwater_series(row["equity_curve"])
        fig.add_trace(  # type: ignore[unknownMemberType]
            go.Scatter(
                x=timestamps,
                y=drawdowns,
                mode="lines",
                name=row["experiment_id"],
                fill="tozeroy",
                visible=(i < default_top_n) if use_slider else True,
            )
        )

    layout_kwargs: dict[str, object] = dict(
        title="Underwater Plot — Drawdown From Peak Over Time",
        xaxis_title="Time",
        yaxis_title="Drawdown From Peak",
        yaxis_tickformat=".1%"
    )

    if use_slider:
        steps: list[dict[str, str | list[dict[str, list[bool]]]]] = []
        for n in range(1, n_traces + 1):
            steps.append(
                dict(
                    method="restyle",
                    args=[{"visible": [i < n for i in range(n_traces)]}],
                    label=str(n),
                )
            )

        layout_kwargs["sliders"] = [
            dict(
                active=default_top_n - 1,
                currentvalue={"prefix": "Showing top "},
                pad={"t": 60},
                steps=steps,
            )
        ]

    fig.update_layout(**layout_kwargs)  # type: ignore[unknownMemberType]
    return fig
