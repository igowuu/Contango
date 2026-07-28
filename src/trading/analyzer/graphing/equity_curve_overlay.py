# trading/analyzer/graphing/equity_curve_overlay.py — part of Contango, a parameterized backtesting & execution framework
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


def build_equity_curve_overlay(
    df: pd.DataFrame,
    rank_by: str = "calmar_ratio",
    default_top_n: int = 8,
    max_traces: int = 40,
) -> go.Figure:
    """
    Builds an equity curve with the top amount of points, adjustable with a slider.

    Args:
        df: The experiment DataFrame.
        rank_by: Metric column to rank by (descending = best first).
        default_top_n: How many traces are visible when the chart first loads.
        max_traces: How many experiments get a trace at all (available in the slider).

    Returns:
        A plotly Figure with an embedded slider.
    """
    plot_df = (
        df.dropna(subset=["equity_curve"])
        .sort_values(rank_by, ascending=False)
        .head(max_traces)
        .reset_index(drop=True)
    )
    n_traces = len(plot_df)
    default_top_n = min(default_top_n, n_traces)

    fig = go.Figure()
    for i, (_, row) in enumerate(plot_df.iterrows()):
        curve = row["equity_curve"]
        timestamps: list[pd.Timestamp] = [pd.to_datetime(t, unit="ms") for t, _ in curve]
        values = [v for _, v in curve]
        fig.add_trace(  # type: ignore[unknownMemberType]
            go.Scatter(
                x=timestamps,
                y=values,
                mode="lines",
                name=f"{row['experiment_id']} ({rank_by}={row[rank_by]:.2f})",
                visible=(i < default_top_n),
            )
        )

    # One slider step per N, from 1 up to n_traces.
    steps: list[dict[str, str | list[dict[str, list[bool]]]]] = []
    for n in range(1, n_traces + 1):
        steps.append(
            dict(
                method="restyle",
                args=[{"visible": [i < n for i in range(n_traces)]}],
                label=str(n),
            )
        )

    sliders = [
        dict(
            active=default_top_n - 1,
            currentvalue={"prefix": "Showing top "},
            pad={"t": 60},
            steps=steps,
        )
    ]

    fig.update_layout(  # type: ignore[unknownMemberType]
        title=f"Equity Curve Overlay — ranked by {rank_by}",
        xaxis_title="Time",
        yaxis_title="Account Value (USD)",
        sliders=sliders,
    )
    return fig