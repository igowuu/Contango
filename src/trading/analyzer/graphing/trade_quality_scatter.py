# trading/analyzer/graphing/trade_quality_scatter.py — part of Contango, a parameterized backtesting & execution framework
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


def build_trade_quality_scatter(
    df: pd.DataFrame,
    y_metric: str = "profit_factor",
    color_by: str = "calmar_ratio",
) -> go.Figure:
    """
    Builds the trade-quality scatter plot.

    Args:
        df: Experiment DataFrame.
        y_metric: Metric for the y-axis. "profit_factor" (default) or "expectancy" are best.
        color_by: Column to color points by. Defaults to "calmar_ratio".

    Returns:
        A plotly Figure.
    """
    plot_df = df.dropna(subset=["win_rate", y_metric, "trade_count", color_by]).copy()

    fig = px.scatter(   # type: ignore[unknownMemberType]
        plot_df,
        x="win_rate",
        y=y_metric,
        size="trade_count",
        color=color_by,
        hover_name="experiment_id",
        title=f"Trade Quality — Win Rate vs. {y_metric} (bubble size = trade count)",
        labels={"win_rate": "Win Rate"},
    )
    fig.update_layout(template="plotly_white", xaxis_tickformat=".0%")  # type: ignore[unknownMemberType]
    return fig
