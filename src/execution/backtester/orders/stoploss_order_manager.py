from __future__ import annotations

from execution.engine.events.event_bus import EventBus
from execution.engine.events.events import MarketDataEvent, PortfolioSnapshotEvent, StoplossOrderEvent, OrderEvent


class StoplossOrderManager:
    """
    Holds pending stoploss order events & publishes order events if the stoploss is met.
    If the stoploss event is exited manually (all shares are sold), the stoploss has no effect.
    Assumes only one ticker to be traded & no pyramiding.
    """
    def __init__(self, event_bus: EventBus) -> None:
        """
        Initializes `StoplossOrderManager`.
        
        Args:
            event_bus: The event bus to publish order events to upon the stoploss price being met.
        """
        self._event_bus = event_bus

        self._pending_stoploss_order: StoplossOrderEvent | None = None
        self._current_portfolio_snapshot: PortfolioSnapshotEvent | None = None
        self._previous_portfolio_snapshot: PortfolioSnapshotEvent | None = None

    def collect_stoploss_order_event(self, stoploss_order: StoplossOrderEvent) -> None:
        """
        Stores the latest pending stoploss order.
        """
        self._pending_stoploss_order = stoploss_order

    def collect_portfolio_snapshot(self, snapshot: PortfolioSnapshotEvent) -> None:
        """
        Sets the latest & previous portfolio snapshots so the manager can tell whether the stop is still relevant.
        """
        self._previous_portfolio_snapshot = self._current_portfolio_snapshot
        self._current_portfolio_snapshot = snapshot

    def check_if_stoploss_met(self, market_data: MarketDataEvent) -> None:
        """
        Executes the pending stoploss order when the market bar breaches the stop price.
        Publishes an `OrderEvent` upon the stoploss being reached.

        Args:
            market_data: The current market data event (bar) for the OHLCV data.
        """
        stoploss_order = self._pending_stoploss_order
        previous_portfolio = self._previous_portfolio_snapshot
        current_portfolio = self._current_portfolio_snapshot

        if previous_portfolio is None or current_portfolio is None:
            return

        # If the position is sold off in the strategy elsewhere
        if previous_portfolio.position != 0 and current_portfolio.position == 0:
            self._pending_stoploss_order = None
            return

        if stoploss_order is None:
            return

        if market_data.close < stoploss_order.stop_price:
            quantity_to_sell = -stoploss_order.quantity
            order = OrderEvent(
                timestamp=market_data.timestamp,
                symbol=market_data.symbol,
                quantity=quantity_to_sell,
                reason="Stoploss was met."
            )

            self._event_bus.publish(order)
            self._pending_stoploss_order = None
