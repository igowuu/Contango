# trading/optimizer/analysis/builder.py — part of Contango, a parameterized backtesting & execution framework
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
from collections import deque
from datetime import datetime
from dataclasses import dataclass

from trading.execution.engine import ExecutionData
from trading.optimizer.analysis.context import AnalysisContext, EquityPoint, ReturnPoint, DrawdownPoint, TradePoint


logger = logging.getLogger(__name__)

USD = float
percent = float
units = int
time_unix_ms = int


def _build_equity_curve(
    data: ExecutionData,
) -> tuple[EquityPoint, ...]:
    """
    Builds the account equity curve from portfolio snapshots.
    Snapshots with unknown equity are skipped (the initial snapshot).

    Args:
        data: The `ExecutionData` to derive events from.

    Returns:
        A chronological sequence of `EquityPoint` instances.
    """
    return tuple(
        EquityPoint(snapshot.timestamp, snapshot.equity)
        for snapshot in data.portfolio_snapshot_events
        if snapshot.equity is not None
    )


def _build_returns(
    equity_curve: tuple[EquityPoint, ...],
) -> tuple[ReturnPoint, ...]:
    """
    Builds period returns from an equity curve.

    Each return represents the percentage change from the previous
    equity point.

    Args:
        equity_curve: The derived equity curve for the backtest.
    
    Returns:
        A chronological sequence of `ReturnPoint` instances.
    """
    if len(equity_curve) < 2:
        return ()

    returns: list[ReturnPoint] = []

    previous_equity = equity_curve[0][1]

    for timestamp, equity in equity_curve[1:]:
        if previous_equity == 0:
            raise ValueError("Cannot calculate return from zero equity")

        returns.append(ReturnPoint(
            timestamp,
            (equity - previous_equity) / previous_equity
        ))

        previous_equity = equity

    return tuple(returns)


def _build_drawdowns(
    equity_curve: tuple[EquityPoint, ...],
) -> tuple[DrawdownPoint, ...]:
    """
    Builds the historical drawdown series from an equity curve.

    Args:
        equity_curve: The derived equity curve for the backtest.
    
    Returns:
        A chronological sequence of `DrawdownPoint` instances.
    """
    if not equity_curve:
        return ()

    points: list[DrawdownPoint] = []
    peak_equity = equity_curve[0][1]

    for timestamp, equity in equity_curve:
        peak_equity = max(peak_equity, equity)

        drawdown = (
            (equity - peak_equity) / peak_equity
            if peak_equity != 0
            else 0.0
        )

        points.append(
            DrawdownPoint(
                timestamp=timestamp,
                peak_equity=peak_equity,
                drawdown_percent=drawdown,
            )
        )

    return tuple(points)


@dataclass(slots=True)
class OpenPosition:
    """
    A single open position when building trade points.
    
    Attributes:
        quantity: The units for the position.
        entry_time: The time in which the trade was entered.
        entry_price: The price in which the trade was entered at.
    """
    quantity: units = 0
    entry_time: datetime | None = None
    entry_price: USD | None = None


def _build_trades(data: ExecutionData) -> tuple[TradePoint, ...]:
    """
    Builds a tuple of `TradePoint` instances for backtest data.
    
    Args:
        data: The underlying `ExecutionData` to generate trades upon for calculating metrics.
    
    Returns:
        A tuple of `TradePoint` instances.
    """
    trades: list[TradePoint] = []

    position = OpenPosition()

    # FIFO for partial fills.
    entry_lots: deque[tuple[int, float, time_unix_ms]] = deque()

    for fill in data.accepted_fill_events:
        qty = fill.order_event.quantity
        price = fill.fill_price
        time = fill.timestamp

        # Entry (a buy)
        if qty > 0:
            entry_lots.append((qty, price, time))
            position.quantity += qty

        # Exit (a sell)
        elif qty < 0:
            sell_qty = -qty
            position.quantity -= sell_qty

            # Match FIFO against entry lots
            while sell_qty > 0 and entry_lots:
                lot_qty, lot_price, lot_time = entry_lots[0]

                matched_qty = min(lot_qty, sell_qty)

                trades.append(
                    TradePoint(
                        entry_time=lot_time,
                        exit_time=time,
                        entry_price=lot_price,
                        exit_price=price,
                        quantity=matched_qty,
                    )
                )

                lot_qty -= matched_qty
                sell_qty -= matched_qty

                if lot_qty == 0:
                    entry_lots.popleft()
                else:
                    entry_lots[0] = (lot_qty, lot_price, lot_time)

            if sell_qty > 0:
                raise ValueError("Selling more than position held (data inconsistency)")

    return tuple(trades)


def build_context(data: ExecutionData) -> AnalysisContext:
    """
    Builds an `AnalysisContext` for a single backtest.
    
    Args:
        data: The `ExecutionData` results from a strategy.

    Returns:
        AnalysisContext: The context to compute metrics for the backtest.
    """
    equity_curve = _build_equity_curve(data)
    returns = _build_returns(equity_curve)
    drawdowns = _build_drawdowns(equity_curve)
    trades = _build_trades(data)

    return AnalysisContext(
        equity_curve=equity_curve,
        returns=returns,
        drawdowns=drawdowns,
        trades=trades
    )
