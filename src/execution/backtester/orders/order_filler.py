from __future__ import annotations

from execution.engine.events.events import (
    AcceptedFillEvent, 
    RejectedFillEvent, 
    MarketDataEvent, 
    OrderEvent, 
    PortfolioSnapshotEvent
)
from execution.engine.events.event_bus import EventBus

from execution.backtester.config import BacktesterConfig, FillBehavior


USD = float


class OrderFiller:
    """
    Fills all orders made by accepting `OrderEvent` instances and publishing filled events.
    """
    def __init__(
        self,
        config: BacktesterConfig,
        event_bus: EventBus
    ) -> None:
        """
        Initializes `ExecutionEngine`.
        
        Args:
            config: The `BacktesterConfig` to determine fill behavior from.
            event_bus: The event bus to publish filled events to.
        """
        self._config = config
        self._event_bus = event_bus

        self._last_market_event: MarketDataEvent | None = None
        self._last_portfolio_snapshot: PortfolioSnapshotEvent | None = None

    def _resolve_fill_price(self, market_event: MarketDataEvent) -> USD:
        """
        Returns the fill price for the current market data event based on the provded config.

        Raises:
            RuntimeError: Upon an unknown `FillBehavior` being detected.
        """
        fill_behavior = self._config.fill
        if fill_behavior == FillBehavior.INSTANT:
            return market_event.close

        raise RuntimeError(f"Unknown FillBehavior: {fill_behavior}")

    def collect_market_data(self, market_data: MarketDataEvent) -> None:
        """
        Collects & stores the current market event upon the event being published.
        """
        self._last_market_event = market_data
    
    def collect_portfolio_snapshot(self, event: PortfolioSnapshotEvent) -> None:
        """
        Collects & stores the current portfolio snapshot upon the event being published.
        """
        self._last_portfolio_snapshot = event

    def _apply_slippage(self, order: OrderEvent, fill_price: USD) -> USD:
        """
        Adjusts fill price against the trader based on configured slippage.
        Buys fill higher, sells fill lower.
        """
        multiplier = 1 + self._config.slippage
        if order.quantity > 0:
            return fill_price * multiplier
        else:
            return fill_price / multiplier

    def _calculate_commission(self, order: OrderEvent) -> USD:
        """
        Calculates commission as per-unit.
        """
        per_share = abs(order.quantity) * self._config.commission_per_unit
        return per_share

    def fill_order(self, order_event: OrderEvent) -> None:
        """
        Publishes an accepted or rejected filled event order whenever an `OrderEvent` is created.

        Args:
            order_event: The order event to process & create a `FillOrder` for.
        
        Raises:
            RuntimeError: Upon an order being made before required events being injected into the `OrderFiller`.
        """
        market_event = self._last_market_event
        portfolio_snapshot = self._last_portfolio_snapshot

        if market_event is None:
            raise RuntimeError("Tried to execute orders before market event was registered in the order filler.")
        if portfolio_snapshot is None:
            raise RuntimeError("Tried to execute orders before a portfolio snapshot was registered in the order filler.")

        fill_price = self._resolve_fill_price(market_event)
        price_with_slippage = self._apply_slippage(order_event, fill_price)
        commission = self._calculate_commission(order_event)

        order_cost = price_with_slippage * order_event.quantity
        total_cost = order_cost + commission

        if total_cost > portfolio_snapshot.cash:
            self._event_bus.publish(RejectedFillEvent(
                timestamp=market_event.timestamp, 
                market_event=market_event,
                order_event=order_event,
                reason="Insufficient available cash (slippage & commission applied)"
            ))
            return
        
        if order_event.quantity + portfolio_snapshot.position < 0:
            self._event_bus.publish(RejectedFillEvent(
                timestamp=market_event.timestamp, 
                market_event=market_event,
                order_event=order_event,
                reason="Insufficient position"
            ))
            return

        fill_event = AcceptedFillEvent(
            timestamp=market_event.timestamp,
            market_event=market_event,
            order_event=order_event,
            fill_price=fill_price,
            total_cost=total_cost
        )

        self._event_bus.publish(fill_event)
