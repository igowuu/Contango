# trading/analyzer/graphing/final_comparison_radar.py — part of Contango, a parameterized backtesting & execution framework
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


_DEFAULT_METRICS = ["sharpe_ratio", "calmar_ratio", "win_rate", "profit_factor", "average_holding_period"]


def build_final_comparison_radar(
    df: pd.DataFrame,
    experiment_ids: list[str],
    metrics: list[str] | None = None,
) -> go.Figure:
    """
    Builds a chart comparing a final shortlist of experiments across
    several normalized metrics.

    Args:
        df: Experiment DataFrame.
        experiment_ids: The final shortlist of experiment_id values to compare.
        metrics: Metric columns to compare, excluding "max_drawdown".
                 Defaults to sharpe_ratio, calmar_ratio, win_rate,
                 profit_factor, average_holding_period.

    Returns:
        A plotly Figure.
    """
    metrics = list(metrics) if metrics is not None else list(_DEFAULT_METRICS)
    all_metrics = metrics + ["max_drawdown"]

    plot_df = df[df["experiment_id"].isin(experiment_ids)].dropna(subset=all_metrics).copy()
    normalized = plot_df.copy()

    for m in all_metrics:
        col = plot_df[m].copy()
        if m == "max_drawdown":
            col = -col.abs()  # smaller magnitude drawdown -> higher normalized score
        min_v, max_v = col.min(), col.max()
        normalized[m] = 0.5 if max_v == min_v else (col - min_v) / (max_v - min_v)

    categories = all_metrics
    fig = go.Figure()
    for _, row in normalized.iterrows():
        values = [row[m] for m in categories] + [row[categories[0]]]
        fig.add_trace(  # type: ignore[unknownMemberType]
            go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                fill="toself",
                name=row["experiment_id"]
            )
        )

    fig.update_layout(  # type: ignore[unknownMemberType]
        polar={"radialaxis": {"visible": True, "range": [0, 1]}},
        title="Final Comparison — Normalized Metrics Across Shortlisted Strategies",
        template="plotly_white",
    )
    return fig
