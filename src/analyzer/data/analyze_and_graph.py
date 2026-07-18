from __future__ import annotations

import os

from analyzer.graphing.risk_return_overview import build_risk_return_overview
from analyzer.graphing.parameter_importance import build_parameter_importance, compute_parameter_importance
from analyzer.graphing.parallel_coordinates import build_parallel_coordinates
from analyzer.graphing.pairwise_heatmap_grid import build_pairwise_heatmap_grid
from analyzer.graphing.metric_distribution import build_metric_distribution
from analyzer.graphing.equity_curve_overlay import build_equity_curve_overlay
from analyzer.graphing.underwater_drawdown import build_underwater_plot
from analyzer.graphing.trade_quality_scatter import build_trade_quality_scatter
from analyzer.graphing.final_comparison_radar import build_final_comparison_radar
from analyzer.data.data_prep import get_param_columns, results_to_dataframe

from optimizer.experiments.backtest_experiment_result import BacktestExperimentResult


def generate_report(
    results: list[BacktestExperimentResult],
    output_dir: str,
    rank_metric: str = "calmar_ratio",
    shortlist_size: int = 8,
    final_comparison_size: int = 5,
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
        final_comparison_size: Number of experiments to show in the final
            radar comparison (chart 7) — keep this small (3-5) for readability.
    """
    os.makedirs(output_dir, exist_ok=True)

    df = results_to_dataframe(results)
    param_columns = get_param_columns(df)

    if not param_columns:
        raise ValueError("No swept parameters found — every parameter is constant across `results`.")

    build_risk_return_overview(df, color_by=rank_metric).write_html(    # type: ignore[unknownMemberType]
        os.path.join(output_dir, "01_risk_return_overview.html")
    )

    build_parameter_importance(df, param_columns, target_metric=rank_metric).write_html(    # type: ignore[unknownMemberType]
        os.path.join(output_dir, "02a_parameter_importance.html")
    )
    importance_df = compute_parameter_importance(df, rank_metric, param_columns)
    ranked_params = importance_df["parameter"].tolist()

    build_parallel_coordinates(df, param_columns, target_metric=rank_metric, sample_size=500).write_html(   # type: ignore[unknownMemberType]
        os.path.join(output_dir, "02b_parallel_coordinates.html")
    )

    if len(ranked_params) >= 3:
        param_x, param_y, facet_param = ranked_params[0], ranked_params[1], ranked_params[2]
        build_pairwise_heatmap_grid(df, param_x, param_y, facet_param, target_metric=rank_metric).write_html(   # type: ignore[unknownMemberType]
            os.path.join(output_dir, "02c_pairwise_heatmap_grid.html")
        )
    elif len(ranked_params) == 2:
        # No third parameter to facet by — fall back to a single 2D heatmap
        df["_single_facet"] = "all"
        build_pairwise_heatmap_grid(    # type: ignore[unknownMemberType]
            df, ranked_params[0], ranked_params[1], "_single_facet", target_metric=rank_metric
        ).write_html(os.path.join(output_dir, "02c_pairwise_heatmap_grid.html"))
        df.drop(columns=["_single_facet"], inplace=True)

    build_metric_distribution(df, group_by=ranked_params[0], target_metric="total_return").write_html(  # type: ignore[unknownMemberType]
        os.path.join(output_dir, "03_metric_distribution.html")
    )

    build_equity_curve_overlay(df, top_n=shortlist_size, rank_by=rank_metric).write_html(   # type: ignore[unknownMemberType]
        os.path.join(output_dir, "04_equity_curve_overlay.html")
    )

    build_underwater_plot(df, top_n=shortlist_size, rank_by=rank_metric).write_html(    # type: ignore[unknownMemberType]
        os.path.join(output_dir, "05_underwater_drawdown.html")
    )

    build_trade_quality_scatter(df, color_by=rank_metric).write_html(   # type: ignore[unknownMemberType]
        os.path.join(output_dir, "06_trade_quality_scatter.html")
    )

    final_shortlist = (
        df.sort_values(rank_metric, ascending=False).head(final_comparison_size)["experiment_id"].tolist()
    )
    build_final_comparison_radar(df, final_shortlist).write_html(   # type: ignore[unknownMemberType]
        os.path.join(output_dir, "07_final_comparison_radar.html")
    )
