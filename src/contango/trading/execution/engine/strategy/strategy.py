# trading/execution/engine/strategy/strategy.py — part of Contango, a parameterized backtesting & execution framework
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

from abc import ABC, abstractmethod

from contango.trading.execution.engine.events.events import MarketDataEvent, AcceptedFillEvent, RejectedFillEvent, OrderEvent, PortfolioSnapshotEvent
from contango.trading.execution.engine.orders.order_api import OrderAPI


class Strategy(ABC):
    """
    Abstract base class for implementing trading strategies.

    A Strategy defines user logic by responding to lifecycle and market events
    emitted by the engine. Subclasses should implement the required
    event handlers to initialize state, process market data, and react
    to order/trade events.

    Lifecycle:
        - `on_start()`: called once before any data is processed.
        - `on_end()`: called once after all data has been processed.

    Event hooks:
        - `on_market_event()`: triggered upon a market event (bar).
        - `on_order_event()`: triggered when an order is submitted.
        - `on_fill_event()`: triggered when an order is filled.
    
    Fields (injected):
        - `order_api`: allows for communication with the engine to make orders.
        - `portfolio_snapshot`: the current snapshot of the account that holds all positions & cash.
    """
    order_api: OrderAPI
    portfolio_snapshot: PortfolioSnapshotEvent

    def on_start(self) -> None:
        """
        Called exactly once at the beginning of strategy execution.
        """
        ...

    @abstractmethod
    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Called once for market event (bar) in the given OHLCV data.
        """
        ...

    def on_order_event(self, order: OrderEvent) -> None:
        """
        Called once when an order has been submitted.
        """
        ...

    def on_accepted_fill_event(self, trade: AcceptedFillEvent) -> None:
        """
        Called once when an order has been successfully filled.
        """
        ...

    def on_rejected_fill_event(self, trade: RejectedFillEvent) -> None:
        """
        Called once when an order was rejected instead of filled.
        """
        ...

    def on_end(self) -> None:
        """
        Called exactly once at the end of strategy execution.
        """
        ...
