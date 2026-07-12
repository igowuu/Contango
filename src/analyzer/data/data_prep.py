"""
Shared data preparation utilities for backtest analysis & graphing.

Every chart module in this package consumes the tidy DataFrame produced by
`results_to_dataframe` — this is the single source of truth for turning raw
`BacktestExperimentResult` objects into something plottable. Chart files
should never reach back into `experiment` / `backtest_metrics` directly.
"""
from __future__ import annotations

from typing import Any

import pandas as pd

from optimizer.experiments.backtest_experiment_result import BacktestExperimentResult


# Columns produced by results_to_dataframe that are NOT swept strategy
# parameters. Used by get_param_columns() to infer which columns are params
# by exclusion, so new metrics added to Metrics don't need to be special-cased
# everywhere else.
_METRIC_COLUMNS = {
    "total_return", "monthly_returns", "equity_curve",
    "annual_return", "monthly_volatility", "sharpe_ratio", "calmar_ratio",
    "max_drawdown", "average_drawdown",
    "trade_count", "win_rate", "profit_factor", "expectancy",
    "average_win", "average_loss", "average_holding_period",
    "experiment_id",
}


def results_to_dataframe(results: list[BacktestExperimentResult]) -> pd.DataFrame:
    """
    Flattens a list of BacktestExperimentResult into a tidy DataFrame.

    Each row = one experiment. Columns:
        - one column per parameter key in experiment.parameters
        - flattened metric columns (total_return, sharpe_ratio, max_drawdown, ...)
        - "equity_curve" / "monthly_returns": kept as raw tuples (object dtype),
          consumed directly by the equity-curve / underwater-plot charts
        - "experiment_id": a human-readable label built from the parameter values,
          used for hover text, legends, and shortlist filtering

    Args:
        results: The list of BacktestExperimentResult from ResearchRunner.run(...).

    Returns:
        A pandas DataFrame with one row per experiment.
    """
    rows: list[dict[str, Any]] = []

    for result in results:
        params = dict(result.experiment.parameters)
        metrics = result.backtest_metrics

        row: dict[str, Any] = dict(params)

        # Returns
        row["total_return"] = metrics.returns.total_return
        row["monthly_returns"] = metrics.returns.monthly_returns
        row["equity_curve"] = metrics.returns.equity_curve

        # Risk
        row["annual_return"] = metrics.risk.annual_return
        row["monthly_volatility"] = metrics.risk.monthly_volatility
        row["sharpe_ratio"] = metrics.risk.sharpe_ratio
        row["calmar_ratio"] = metrics.risk.calmar_ratio

        # Drawdowns
        row["max_drawdown"] = metrics.drawdowns.max_drawdown
        row["average_drawdown"] = metrics.drawdowns.average_drawdown

        # Trades
        row["trade_count"] = metrics.trades.trade_count
        row["win_rate"] = metrics.trades.win_rate
        row["profit_factor"] = metrics.trades.profit_factor
        row["expectancy"] = metrics.trades.expectancy
        row["average_win"] = metrics.trades.average_win
        row["average_loss"] = metrics.trades.average_loss
        row["average_holding_period"] = metrics.trades.average_holding_period

        row["experiment_id"] = ", ".join(f"{k}={v}" for k, v in params.items())

        rows.append(row)

    return pd.DataFrame(rows)


def get_param_columns(df: pd.DataFrame, exclude_constant: bool = True) -> list[str]:
    """
    Returns the columns in `df` that represent swept strategy parameters, inferred
    by exclusion of known metric column names.

    Args:
        df: DataFrame produced by `results_to_dataframe`.
        exclude_constant: If True (default), drop parameters that only take a
            single unique value across all rows (e.g. a fixed `allocation`),
            since they carry zero information for comparison/graphing.

    Returns:
        List of parameter column names.
    """
    param_columns = [c for c in df.columns if c not in _METRIC_COLUMNS]

    if exclude_constant:
        param_columns = [c for c in param_columns if df[c].nunique(dropna=False) > 1]

    return param_columns
