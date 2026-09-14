from __future__ import annotations

from typing import Any

import pandas as pd
from pandas.api.types import is_hashable

from contango.trading.analysis.data.graphing_experiment import GraphingExperiment


_METRIC_COLUMNS = {
    "total_return", "monthly_returns", "equity_curve",
    "annual_return", "monthly_volatility", "sharpe_ratio", "calmar_ratio",
    "max_drawdown", "average_drawdown",
    "trade_count", "win_rate", "profit_factor", "expectancy",
    "average_win", "average_loss", "average_holding_period",
    "name",
}


def results_to_dataframe(experiments: list[GraphingExperiment]) -> pd.DataFrame:
    """
    Flattens a list of GraphingExperiment instances into a DataFrame.

    Args:
        experiments: The list of GraphingExperiment instances.

    Returns:
        pd.DataFrame: A pandas DataFrame with one row per experiment.
    """
    rows: list[dict[str, Any]] = []

    for experiment in experiments:
        metrics = experiment.metrics
        name = experiment.name

        row: dict[str, Any] = {}
        for key, value in experiment.parameters.items():
            row[key] = value

        row["total_return"] = metrics.returns.total_return
        row["monthly_returns"] = metrics.returns.monthly_returns
        row["equity_curve"] = metrics.returns.equity_curve

        row["annual_return"] = metrics.risk.annual_return
        row["monthly_volatility"] = metrics.risk.monthly_volatility
        row["sharpe_ratio"] = metrics.risk.sharpe_ratio
        row["calmar_ratio"] = metrics.risk.calmar_ratio

        row["max_drawdown"] = metrics.drawdowns.max_drawdown
        row["average_drawdown"] = metrics.drawdowns.average_drawdown

        row["trade_count"] = metrics.trades.trade_count
        row["win_rate"] = metrics.trades.win_rate
        row["profit_factor"] = metrics.trades.profit_factor
        row["expectancy"] = metrics.trades.expectancy
        row["average_win"] = metrics.trades.average_win
        row["average_loss"] = metrics.trades.average_loss
        row["average_holding_period"] = metrics.trades.average_holding_period

        row["name"] = name

        rows.append(row)

    return pd.DataFrame(rows)


def get_param_columns(df: pd.DataFrame, exclude_constant: bool = True) -> list[str]:
    """
    Returns the columns in `df` that represent swept strategy parameters.

    Args:
        df: DataFrame produced by `results_to_dataframe`.
        exclude_constant: If True (default), drop parameters that only take a
                          single unique value across all rows.

    Returns:
        List of parameter column names.
    """
    param_columns = [c for c in df.columns if c not in _METRIC_COLUMNS]
    param_columns = [
        c for c in param_columns
        if df[c].map(is_hashable).all()
    ]

    if exclude_constant:
        param_columns = [c for c in param_columns if df[c].nunique(dropna=False) > 1]

    return param_columns
