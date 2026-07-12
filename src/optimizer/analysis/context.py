from __future__ import annotations

from typing import NamedTuple


USD = float
percent = float
units = int
time_unix_ms = int


class EquityPoint(NamedTuple):
    """
    A single equity point in an equity curve.
    
    Attributes:
        timestamp: The time for the equity point (unix ms).
        equity: The price for the equity point at its timestamp.
    """
    timestamp: time_unix_ms
    equity: USD


class ReturnPoint(NamedTuple):
    """
    A single return point in time.
    
    Attributes:
        timestamp: The time for the return point (unix ms).
        return_percent: The percent increase / decrease from the previous point.
    """
    timestamp: time_unix_ms
    return_percent: percent


class DrawdownPoint(NamedTuple):
    """
    A single drawdown point in time.
    
    Attributes:
        timestamp: The time for the drawdown point (unix ms).
        peak: The highest equity up to and including this point.
        drawdown_percent: The current percentage decline of the equity from its peak value to its lowest point.
    """
    timestamp: time_unix_ms
    peak_equity: USD
    drawdown_percent: percent


class TradePoint(NamedTuple):
    """
    A single completed trade (long-only).
    
    Attributes:
        entry_time: When the position was opened (unix ms).
        exit_time: When the position was closed (unix ms).
        entry_price: Price at entry.
        exit_price: Price at exit.
        quantity: Units held.
    """
    entry_time: time_unix_ms
    exit_time: time_unix_ms
    entry_price: USD
    exit_price: USD
    quantity: units


class AnalysisContext(NamedTuple):
    """
    The analysis data necessary to compute the metrics for a backtest.

    Attributes:
        equity_curve: The equity (value of units + cash) in USD for every portfolio event.
        returns: The total returns (in percent) for every equity point.
        drawdowns: The peak (USD) & drawdown (in percent) for every equity point.
        trades: The trades made during the execution of the backtester.
    """
    equity_curve: tuple[EquityPoint, ...]
    returns: tuple[ReturnPoint, ...]
    drawdowns: tuple[DrawdownPoint, ...]
    trades: tuple[TradePoint, ...]
