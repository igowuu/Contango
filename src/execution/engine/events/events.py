from __future__ import annotations

from typing import NamedTuple


USD = float
time_unix_ms = int
units = int


class MarketDataEvent(NamedTuple):
    """
    Immutable event snapshot of OHLCV data for a single bar.

    Attributes:
        timestamp: Time unix (ms) of the bar.
        symbol: Ticker symbol.
        open: Opening price in USD.
        high: Highest price in USD.
        low: Lowest price in USD.
        close: Closing price in USD.
        volume: Number of units traded.
    """
    timestamp: time_unix_ms
    symbol: str
    open: USD
    high: USD
    low: USD
    close: USD
    volume: units


class OrderEvent(NamedTuple):
    """
    A single trade event emitted by a strategy.

    Attributes:
        timestamp: The time (unix ms) which the order event was created.
        symbol: The ticker to trade.
        quantity: Number of units (i.e. shares) to trade (signed for buys versus sells).
        reason: Optional description on why the trade was made.
    """
    timestamp: time_unix_ms
    symbol: str
    quantity: units
    reason: str | None = None


class AcceptedFillEvent(NamedTuple):
    """
    A single filled trade event (an order that has been processed) that has been accepted.
    
    Attributes:
        timestamp: When the trade was filled (unix ms).
        market_event: The market event in which the trade was filled at.
        order_event: The underlying order that was filled.
        fill_price: The price that the order was filled at (per unit).
        total_cost: The total cost (including slippage & commission) for the entire trade.
    """
    timestamp: time_unix_ms
    market_event: MarketDataEvent
    order_event: OrderEvent
    fill_price: USD
    total_cost: USD


class RejectedFillEvent(NamedTuple):
    """
    A single filled trade event (an order that has been processed) that has been rejected.
    
    Attributes:
        timestamp: When the rejected trade was attempted to be filled (unix ms).
        market_event: The market event in which the rejected trade was made at.
        order_event: The underlying order that was rejected.
        reason: The reasoning for the rejection.
    """
    timestamp: time_unix_ms
    market_event: MarketDataEvent
    order_event: OrderEvent
    reason: str | None = None


class PortfolioSnapshotEvent(NamedTuple):
    """
    A single event snapshot of an account portfolio.

    Attributes:
        timestamp: The timestamp in which the portfolio snapshot was made (unix ms).
        cash: The cash available for trading in the account.
        position: The current amount of units held in the account.
        equity: The total equity (cash + units) in the account, or None if it cannot be derived (e.g. initial snapshot).
    """
    timestamp: time_unix_ms
    cash: USD
    position: units
    equity: USD | None
