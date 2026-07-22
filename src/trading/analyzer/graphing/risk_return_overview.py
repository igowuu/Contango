# trading/analyzer/graphing/risk_return_overview.py — part of Contango, a parameterized backtesting & execution framework
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


def build_risk_return_overview(
    df: pd.DataFrame,
    color_by: str = "calmar_ratio",
) -> go.Figure:
    """
    Builds the risk/return overview scatter plot.

    Args:
        df: Experiment DataFrame from `data_prep.results_to_dataframe`.
        color_by: Column to color points by. Defaults to "calmar_ratio" so
                  warmer colors highlight the best risk-adjusted performers. Pass a
                  parameter column name instead to color by a swept parameter.

    Returns:
        A plotly Figure.
    """
    plot_df = df.dropna(subset=["annual_return", "sharpe_ratio", "max_drawdown", color_by]).copy()
    plot_df["drawdown_severity"] = plot_df["max_drawdown"].abs()

    is_numeric_color = pd.api.types.is_numeric_dtype(plot_df[color_by])

    fig = px.scatter(   # type: ignore[unknownMemberType]
        plot_df,
        x="annual_return",
        y="sharpe_ratio",
        size="drawdown_severity",
        color=color_by,
        hover_name="experiment_id",
        hover_data={
            "max_drawdown": ":.2%",
            "calmar_ratio": ":.2f",
            "trade_count": True,
            "drawdown_severity": False,
        },
        color_continuous_scale="Viridis" if is_numeric_color else None,
        title="Risk/Return Overview — Annual Return vs. Sharpe Ratio (bubble size = drawdown severity)",
        labels={"annual_return": "Annual Return (CAGR)", "sharpe_ratio": "Sharpe Ratio"},
    )
    fig.update_layout(template="plotly_white", xaxis_tickformat=".1%")  # type: ignore[unknownMemberType]
    return fig
