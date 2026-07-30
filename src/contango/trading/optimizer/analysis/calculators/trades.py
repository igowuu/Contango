# trading/optimizer/analysis/calculators/trades.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.optimizer.analysis.metrics import TradeMetrics
from contango.trading.optimizer.analysis.context import TradePoint, AnalysisContext


logger = logging.getLogger(__name__)

percent = float
time_unix_ms = int


def _get_trade_returns(
    trades: tuple[TradePoint, ...],
) -> tuple[percent, ...] | None:
    """
    Returns the trade return percents for the trades.
    """
    if not trades:
        logger.debug("Trade returns: Trade list was empty!")
        return None

    return tuple(
        (t.exit_price - t.entry_price) / t.entry_price
        for t in trades
    )


def _get_trade_count(
    trades: tuple[TradePoint, ...]
) -> int:
    """
    Returns the amount of trades made for the strategy backtest.
    """
    return len(trades)


def _get_win_rate(
    trades: tuple[TradePoint, ...],
) -> percent | None:
    """
    Returns the percent that a trade will yield positive results.
    """
    if not trades:
        logger.debug("Win rate: Trades list was empty.")
        return None

    wins = [
        t for t in trades
        if t.exit_price > t.entry_price
    ]

    return len(wins) / len(trades)


def _get_profit_factor(
    trades: tuple[TradePoint, ...],
) -> float | None:
    """
    Returns the a ratio profits : losses for the strategy backtest.
    """
    if not trades:
        logger.debug("Profit factor: Trades list was empty.")
        return None

    profits = [
        (t.exit_price - t.entry_price) * t.quantity
        for t in trades
        if t.exit_price > t.entry_price
    ]
    losses = [
        (t.exit_price - t.entry_price) * t.quantity
        for t in trades
        if t.exit_price < t.entry_price
    ]

    gross_profit = sum(profits)
    gross_loss = abs(sum(losses))

    if gross_loss == 0:
        logger.debug("Profit factor: Gross loss was zero")
        return None

    return gross_profit / gross_loss


def _get_expectancy(
    trades: tuple[TradePoint, ...]
) -> percent | None:
    """
    Returns the expected profit per trade with the strategy.
    """
    if not trades:
        logger.debug("Expectancy: Trades list was empty.")
        return None

    return_percents = _get_trade_returns(trades)

    if not return_percents:
        logger.debug("Expectancy: return percents was None.")
        return None

    wins = [
        r for r in return_percents
        if r > 0
    ]
    losses = [
        r for r in return_percents
        if r < 0
    ]

    win_rate = len(wins) / len(return_percents)
    loss_rate = len(losses) / len(return_percents)

    average_win = float(np.mean(wins)) if wins else 0.0
    average_loss = abs(float(np.mean(losses))) if losses else 0.0

    return (
        win_rate * average_win
        -
        loss_rate * average_loss
    )


def _get_average_win(
    trades: tuple[TradePoint, ...]
) -> percent | None:
    """
    Returns the average percent profit per win.
    """
    returns = _get_trade_returns(trades)

    if not returns:
        logger.debug("Average win: Returns list was None")
        return None

    wins = [r for r in returns if r > 0]

    if not wins:
        logger.debug("Average win: Wins list was empty.")
        return None

    return float(np.mean(wins))


def _get_average_loss(
    trades: tuple[TradePoint, ...]
) -> percent | None:
    """
    Returns the average percent lost per loss.
    """
    returns = _get_trade_returns(trades)

    if not returns:
        logger.debug("Average loss: Returns list was None")
        return None

    losses = [r for r in returns if r < 0]

    if not losses:
        logger.debug("Average loss: Losses list was empty.")
        return None

    return float(np.mean(losses))


def _get_average_holding_period(
    trades: tuple[TradePoint, ...],
) -> time_unix_ms | None:
    """
    Returns the average holding period per trade across all `TradePoint` instances.
    """
    if not trades:
        logger.debug("Average holding period: Trades list was empty.")
        return None

    durations = [t.exit_time - t.entry_time for t in trades]
    return int(sum(durations) / len(durations))


def get_trade_metrics(context: AnalysisContext) -> TradeMetrics:
    """
    Returns the `TradeMetrics` for the given context.

    Args:
        context: The `AnalysisContext` object to derive data from.
    
    Returns:
        A `TradeMetrics` object with all the metrics relating to trades.
    """
    trade_count = _get_trade_count(context.trades)
    win_rate = _get_win_rate(context.trades)
    profit_factor = _get_profit_factor(context.trades)
    expectancy = _get_expectancy(context.trades)
    average_win = _get_average_win(context.trades)
    average_loss = _get_average_loss(context.trades)
    average_holding_period = _get_average_holding_period(context.trades)
    return TradeMetrics(
        trade_count=trade_count,
        win_rate=win_rate,
        profit_factor=profit_factor,
        expectancy=expectancy,
        average_win=average_win,
        average_loss=average_loss,
        average_holding_period=average_holding_period
    )
