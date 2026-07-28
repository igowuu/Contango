# trading/execution/engine/orders/order_api.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.execution.engine.events.events import OrderEvent, MarketDataEvent, StoplossOrderEvent
from trading.execution.engine.events.event_bus import EventBus


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
            quantity=quantity,
            stop_price=stoploss_price,
            reason=reason
        )
        self._event_bus.publish(order)
