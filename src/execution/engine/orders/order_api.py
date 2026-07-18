from __future__ import annotations

from execution.engine.events.events import OrderEvent, MarketDataEvent, StoplossOrderEvent
from execution.engine.events.event_bus import EventBus


units = int
USD = float


class OrderAPI:
    """
    API that allows `OrderEvent` instances to be published to the execution engine.
    """
    def __init__(self, event_bus: EventBus) -> None:
        """
        Initializes `OrderAPI`.

        Args:
            event_bus: The event bus to publish `OrderEvent` objects to.
        """
        self._event_bus = event_bus

    def submit_order(
        self, 
        market_data: MarketDataEvent, 
        symbol: str, 
        quantity: units,
        reason: str | None = None,
    ) -> None:
        """
        Submits a market order object to the engine.

        Attributes:
            market_data: The market data event for the order.
            symbol: The symbol to create the order for.
            quantity: The amount of units of the symbol to trade (positive or negative depending on buy or sell).
            reason: The optional reason for the trade.
        """
        order = OrderEvent(
            market_data.timestamp,
            symbol=symbol,
            quantity=quantity,
            reason=reason
        )
        self._event_bus.publish(order)

    def submit_stoploss_order(
        self, 
        market_data: MarketDataEvent, 
        symbol: str, 
        quantity: units,
        stoploss_price: USD,
        reason: str | None = None,
    ) -> None:
        """
        Submits a stoploss order object to the engine.

        Attributes:
            market_data: The market data event for the order.
            symbol: The symbol to create the order for.
            quantity: The amount of units of the symbol to trade (positive or negative depending on buy or sell).
            stoploss_price: The price in which the quantity amount of shares will be sold upon being met.
            reason: The optional reason for the trade.
        """
        order = StoplossOrderEvent(
            market_data.timestamp,
            symbol=symbol,
            quantity=quantity,
            stop_price=stoploss_price,
            reason=reason
        )
        self._event_bus.publish(order)
