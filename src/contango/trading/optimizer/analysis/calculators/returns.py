# trading/optimizer/analysis/calculators/returns.py — part of Contango, a parameterized backtesting & execution framework
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

import logging
from datetime import datetime, timezone

from contango.trading.optimizer.analysis.metrics import ReturnMetrics
from contango.trading.optimizer.analysis.context import AnalysisContext, EquityPoint


logger = logging.getLogger(__name__)

USD = float
percent = float
time_unix_ms = int


def _get_total_return(
    equity_curve: tuple[EquityPoint, ...],
) -> percent | None:
    """
    Returns the total profit as a percent.
    """
    if len(equity_curve) < 2:
        logger.debug("Total return: Length of equity curve was below 2.")
        return None

    initial = equity_curve[0].equity
    final = equity_curve[-1].equity

    if initial == 0:
        logger.debug("Cannot calculate return from zero starting equity.")
        return None

    return (final - initial) / initial


def _get_monthly_returns(
    equity_curve: tuple[EquityPoint, ...],
) -> tuple[tuple[time_unix_ms, percent], ...] | None:
    """
    Returns a list of how much the equity changes each month as a percentage (the monthly returns).
    """
    if not equity_curve:
        return None

    initial_equity = equity_curve[0].equity
    
    month_ends: dict[datetime, USD] = {}

    for point in equity_curve:
        time_as_dt = datetime.fromtimestamp(point.timestamp / 1000, timezone.utc)
        normalized_month = datetime(time_as_dt.year, time_as_dt.month, 1, tzinfo=timezone.utc)
        month_ends[normalized_month] = point.equity

    prev_equity = initial_equity
    results: list[tuple[time_unix_ms, percent]] = []

    for month_key in month_ends.keys():
        unix_ms_month_key = int(month_key.timestamp() * 1000)
        current_equity = month_ends[month_key]
        
        if prev_equity != 0:
            month_return = (current_equity - prev_equity) / prev_equity
            results.append((unix_ms_month_key, month_return))

        prev_equity = current_equity

    return tuple(results)


def get_return_metrics(context: AnalysisContext) -> ReturnMetrics:
    """
    Returns the `ReturnMetrics` for the given context.

    Args:
        context: The `AnalysisContext` object to derive data from.
    
    Returns:
        A `ReturnMetrics` object with all the metrics relating to returns.
    """
    total_return = _get_total_return(context.equity_curve)
    monthly_returns = _get_monthly_returns(context.equity_curve)
    equity_curve = context.equity_curve
    return ReturnMetrics(
        total_return=total_return,
        monthly_returns=monthly_returns,
        equity_curve=equity_curve
    )
