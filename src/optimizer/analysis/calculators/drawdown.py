from __future__ import annotations

import logging

import numpy as np

from optimizer.analysis.metrics import DrawdownMetrics
from optimizer.analysis.context import AnalysisContext, DrawdownPoint


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
