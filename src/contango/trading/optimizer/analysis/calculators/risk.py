# trading/optimizer/analysis/calculators/risk.py — part of Contango, a parameterized backtesting & execution framework
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
from math import sqrt

import numpy as np

from contango.trading.optimizer.analysis.context import EquityPoint, AnalysisContext
from contango.trading.optimizer.analysis.metrics import RiskMetrics


logger = logging.getLogger(__name__)

percent = float
time_unix_ms = int


def _get_monthly_volatility(
    monthly_returns: tuple[tuple[time_unix_ms, percent], ...] | None,
) -> percent | None:
    """
    Returns the monthly monthly standard deviation (volatility).
    """
    if monthly_returns is None:
        logger.debug("Monthly volatility: monthly returns list was None")
        return None

    if len(monthly_returns) < 2:
        logger.debug("Monthly volatility: monthly returns list length was lower than 2.")
        return None

    returns = [r[1] for r in monthly_returns]
    return float(np.std(returns, ddof=1))


def _get_sharpe_ratio(
    monthly_returns: tuple[tuple[time_unix_ms, percent], ...] | None,
    monthly_volatility: percent | None
) -> float | None:
    """
    Returns the annual sharp ratio (risk-adjusted return of the strategy).
    """
    if monthly_returns is None:
        logger.debug("Sharpe ratio: monthly returns list was None")
        return None

    if len(monthly_returns) < 2:
        logger.debug("Sharpe ratio: Monthly returns list length was below 2.")
        return None

    if monthly_volatility is None:
        logger.debug("Monthly volatility: monthly volatility was None")
        return None

    if monthly_volatility == 0:
        logger.debug("Sharpe ratio: Monthly volatility was equivelant to zero.")
        return None

    returns = [r[1] for r in monthly_returns]
    return (
        float(np.mean(returns))
    ) / monthly_volatility * sqrt(12)


def _get_calmar_ratio(
    annual_return: percent | None,
    max_drawdown: percent | None,
) -> float | None:
    """
    Returns the calmar ratio for the strategy.
    """
    if annual_return is None:
        logger.debug("Calmar ratio: Annual return was None.")
        return None

    if max_drawdown is None:
        logger.debug("Calmar ratio: Max drawdown was None")
        return None

    if max_drawdown == 0:
        logger.debug("Calmar ratio: Max drawdown was equivelant to zero.")
        return None

    return annual_return / abs(max_drawdown)


def _get_annual_return(
    equity_curve: tuple[EquityPoint, ...],
) -> percent | None:
    """
    Returns the annualized compound return (CAGR).
    """
    if len(equity_curve) < 2:
        logger.debug("Annual return: Equity curve length was lower than 2.")
        return None

    initial = equity_curve[0].equity
    final = equity_curve[-1].equity

    if initial <= 0:
        logger.debug("Annual return: Initial equity was zero or negative.")
        return None

    duration_ms = equity_curve[-1].timestamp - equity_curve[0].timestamp
    years = duration_ms / (365.25 * 24 * 60 * 60 * 1000)

    if years < (1 / 365.25):
        logger.debug("Annual return: Duration was less than one day.")
        return None

    return (final / initial) ** (1 / years) - 1


def get_risk_metrics(
    context: AnalysisContext,
    monthly_returns: tuple[tuple[time_unix_ms, percent], ...] | None,
    max_drawdown: percent | None
) -> RiskMetrics:
    """
    Returns the `RiskMetrics` for a strategy backtest.
    
    Args:
        context: The `AnalysisContext` object to derive data from.
        monthly_returns: The returns (in percent) per month from latest to most recent.
        max_drawdown: The worst single historical loss of the strategy.
    """
    annual_return = _get_annual_return(context.equity_curve)
    monthly_volatility = _get_monthly_volatility(monthly_returns)
    sharpe_ratio = _get_sharpe_ratio(monthly_returns, monthly_volatility)
    calmar_ratio = _get_calmar_ratio(annual_return, max_drawdown)
    return RiskMetrics(
        annual_return=annual_return,
        monthly_volatility=monthly_volatility,
        sharpe_ratio=sharpe_ratio,
        calmar_ratio=calmar_ratio
    )
