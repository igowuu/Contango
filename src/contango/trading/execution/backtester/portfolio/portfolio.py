# trading/execution/backtester/portfolio/portfolio.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.execution.engine.events.events import PortfolioSnapshotEvent, AcceptedFillEvent, MarketDataEvent
from contango.trading.execution.engine.events.event_bus import EventBus
from contango.trading.execution.backtester.config import BacktesterConfig


USD = float
units = int


class Portfolio:
    """
    Tracks cash, position, and equity during backtesting for one symbol. 
    """
    def __init__(
        self, 
        event_bus: EventBus, 
        config: BacktesterConfig,
        initial_cash: USD = 0.0, 
        initial_position: units = 0
    ) -> None:
        """
        Initializes `Portfolio`.
        
        Args:
            event_bus: The event bus to publish `PortfolioSnapshotEvent` instances to.
            config: The backtester config to derive slippage & commission from.
            initial_cash: The initial cash (USD) to be stored into the portfolio.
            initial_position: The initial position (units) to be stored into the portfolio.
        """
        self._cash = initial_cash
        self._config = config
        self._position = initial_position

        self._event_bus = event_bus

    def _get_equity(self, price: float) -> USD:
        """
        Returns the current equity (cash + position) for the portfolio.
        """
        return (
            self._cash +
            self._position * price
        )

    def update_equity(self, market_data: MarketDataEvent) -> None:
        """
        Updates the equity for the portfolio with a `MarketDataEvent` & publishes a new `PortfolioSnapshotEvent`.

        Args:
            market_data: The `MarketDataEvent` to be processed into the equity.
        
        Raises:
            ValueError: Upon the portfolio cash going below 0 USD.
        """
        snapshot = PortfolioSnapshotEvent(
            timestamp=market_data.timestamp,
            cash=self._cash,
            position=self._position,
            equity=self._get_equity(market_data.close)
        )
        self._event_bus.publish(snapshot)


    def apply_accepted_fill(self, trade: AcceptedFillEvent) -> None:
        """
        Applies an `AcceptedFillEvent` to the internal portfolio & publishes a `PortfolioSnapshotEvent` for external access.

        Args:
            trade: The `AcceptedFillEvent` to be processed into the portfolio.
        
        Raises:
            ValueError: Upon the portfolio cash going below 0 USD (should never happen).
        """
        self._cash -= trade.total_cost

        if self._cash < 0:
            raise ValueError("Portfolio cash incorrectly reached below 0 USD.")

        self._position += trade.order_event.quantity

        snapshot = PortfolioSnapshotEvent(
            timestamp=trade.timestamp,
            cash=self._cash,
            position=self._position,
            equity=self._get_equity(trade.market_event.close)
        )
        self._event_bus.publish(snapshot)

    def get_initial_snapshot(self, initial_market_event: MarketDataEvent) -> PortfolioSnapshotEvent:
        """
        Creates an initial portfolio snapshot based on the current cash, units, & equity.
        The initial snapshot will derive the timestamp from the first market event.
        """
        return PortfolioSnapshotEvent(
            timestamp=initial_market_event.timestamp,
            cash=self._cash,
            position=self._position,
            equity=self._get_equity(initial_market_event.close)
        )
