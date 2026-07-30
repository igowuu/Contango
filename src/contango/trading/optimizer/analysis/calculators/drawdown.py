# trading/optimizer/analysis/calculators/drawdown.py — part of Contango, a parameterized backtesting & execution framework
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

import numpy as np

from contango.trading.optimizer.analysis.metrics import DrawdownMetrics
from contango.trading.optimizer.analysis.context import AnalysisContext, DrawdownPoint


logger = logging.getLogger(__name__)

percent = float


def _get_max_drawdown(
    drawdowns: tuple[DrawdownPoint, ...],
) -> percent | None:
    """
    Returns the largest drawdown (lowest deceimal percent), given a list of drawdowns that are below zero.
    """
    values = [
        x.drawdown_percent
        for x in drawdowns
        if x.drawdown_percent < 0
    ]

    if not values:
        logger.debug("Max Drawdown: negative drawdowns list was empty.")
        return None

    return min(values)


def _get_average_drawdown(
    drawdowns: tuple[DrawdownPoint, ...],
) -> percent | None:
    """
    Returns the mean of all drawdown percents that are below zero.
    """
    values = [
        x.drawdown_percent
        for x in drawdowns
        if x.drawdown_percent < 0
    ]

    if not values:
        logger.debug("Average drawdown: negative drawdowns list was empty.")
        return None

    return float(np.mean(values))


def get_drawdown_metrics(context: AnalysisContext) -> DrawdownMetrics:
    """
    Calculates the drawdown metrics for a strategy backtest.
    
    Args:
        context: The `AnalysisContext` object to derive data from.
    
    Returns:
        A `DrawdownMetrics` object with all the metrics relating to returns.
    """
    max_drawdown = _get_max_drawdown(context.drawdowns)
    average_drawdown = _get_average_drawdown(context.drawdowns)
    return DrawdownMetrics(
        max_drawdown=max_drawdown,
        average_drawdown=average_drawdown
    )
