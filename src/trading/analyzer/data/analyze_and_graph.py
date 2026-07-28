# trading/analyzer/data/analyze_and_graph.py — part of Contango, a parameterized backtesting & execution framework
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

import os
import plotly.io as pio # type: ignore[missingTypeStubs]
import plotly.graph_objects as go   # type: ignore[missingTypeStubs]

from trading.analyzer.graphing.risk_return_overview import build_risk_return_overview
from trading.analyzer.graphing.parameter_importance import build_parameter_importance, compute_parameter_importance
from trading.analyzer.graphing.parallel_coordinates import build_parallel_coordinates
from trading.analyzer.graphing.pairwise_heatmap_grid import build_pairwise_heatmap_grid
from trading.analyzer.graphing.metric_distribution import build_metric_distribution
from trading.analyzer.graphing.equity_curve_overlay import build_equity_curve_overlay
from trading.analyzer.graphing.underwater_drawdown import build_underwater_plot
from trading.analyzer.graphing.trade_quality_scatter import build_trade_quality_scatter
from trading.analyzer.data.data_prep import get_param_columns, results_to_dataframe

from trading.optimizer.experiments.backtest_experiment_result import BacktestExperimentResult


def generate_report(
    results: list[BacktestExperimentResult],
    output_dir: str,
    rank_metric: str = "calmar_ratio",
    shortlist_size: int = 8,
    max_traces: int = 40
) -> None:
    """
    Runs the full analysis flow and writes one HTML file per chart into `output_dir`.

    Args:
        results: The list of BacktestExperimentResult from ResearchRunner.run(config).
        output_dir: Directory to write the HTML files into (created if missing).
        rank_metric: Metric used to rank/shortlist experiments throughout
                     (charts 1 color, 4/5 selection, 7 selection). Defaults to
                     "calmar_ratio" since it's risk-adjusted.
        shortlist_size: Number of experiments to show in the equity curve
                        overlay (chart 4) and underwater plot (chart 5).
        max_traces: Number of traces (maximum amount of graphs) for all sliders.
    """
    dark_gray = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor="#1e1e1e",
            plot_bgcolor="#252526",
            font=dict(color="#d4d4d4"),
            xaxis=dict(
                gridcolor="#444444",
                zerolinecolor="#666666"
            ),
            yaxis=dict(
                gridcolor="#444444",
                zerolinecolor="#666666"
            )
        )
    )

    pio.templates["dark_gray"] = dark_gray
    pio.templates.default = "dark_gray"

    os.makedirs(output_dir, exist_ok=True)

    df = results_to_dataframe(results)
    param_columns = get_param_columns(df)

    if not param_columns:
        raise ValueError("No swept parameters found — every parameter is constant across `results`.")

    build_risk_return_overview(df, color_by=rank_metric).write_html(    # type: ignore[unknownMemberType]
        os.path.join(output_dir, "risk_return_overview.html")
    )

    build_parameter_importance(df, param_columns, target_metric=rank_metric).write_html(    # type: ignore[unknownMemberType]
        os.path.join(output_dir, "parameter_importance.html")
    )
    importance_df = compute_parameter_importance(df, rank_metric, param_columns)
    ranked_params = importance_df["parameter"].tolist()

    build_parallel_coordinates(df, param_columns, target_metric=rank_metric, sample_size=500).write_html(   # type: ignore[unknownMemberType]
        os.path.join(output_dir, "parallel_coordinates.html")
    )

    if len(ranked_params) >= 3:
        param_x, param_y, facet_param = ranked_params[0], ranked_params[1], ranked_params[2]
        build_pairwise_heatmap_grid(df, param_x, param_y, facet_param, target_metric=rank_metric).write_html(   # type: ignore[unknownMemberType]
            os.path.join(output_dir, "pairwise_heatmap_grid.html")
        )
    elif len(ranked_params) == 2:
        # No third parameter to facet by (make 2d grid)
        df["_single_facet"] = "all"
        build_pairwise_heatmap_grid(    # type: ignore[unknownMemberType]
            df, ranked_params[0], ranked_params[1], "_single_facet", target_metric=rank_metric
        ).write_html(os.path.join(output_dir, "02c_pairwise_heatmap_grid.html"))
        df.drop(columns=["_single_facet"], inplace=True)

    build_metric_distribution(df, group_by=ranked_params[0], target_metric="total_return").write_html(  # type: ignore[unknownMemberType]
        os.path.join(output_dir, "metric_distribution.html")
    )

    build_equity_curve_overlay(df, default_top_n=shortlist_size, rank_by=rank_metric, max_traces=max_traces).write_html(   # type: ignore[unknownMemberType]
        os.path.join(output_dir, "equity_curve_overlay.html")
    )

    build_underwater_plot(df, top_n=shortlist_size, rank_by=rank_metric, max_traces=max_traces).write_html(    # type: ignore[unknownMemberType]
        os.path.join(output_dir, "underwater_drawdown.html")
    )

    build_trade_quality_scatter(df, color_by=rank_metric).write_html(   # type: ignore[unknownMemberType]
        os.path.join(output_dir, "trade_quality_scatter.html")
    )
