# trading/execution/backtester/market/feed.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.execution.engine.events.events import MarketDataEvent
from trading.execution.engine.events.event_bus import EventBus


class MarketDataFeed:
    """
    Allows an OHLCV dataframe to be sequentially iterated over and published.
    """
    def __init__(self, data: list[MarketDataEvent], event_bus: EventBus):
        """
        Initializes `MarketDataFeed`.
        
        Args:
            data: The OHLCV list of `MarketDataEvent` to iterate over.
            event_bus: The event bus to publish `MarketDataEvent` instances to.
        """
        self._data = data
        self._event_bus = event_bus

    def get_initial_event(self) -> MarketDataEvent:
        """
        Returns the first `MarketDataEvent` in the OHLCV data.
        """
        return self._data[0]

    def run(self) -> None:
        """
        Iterates through the provided data & publishes 'MarketDataEvent` instances for each bar.
        """
        for event in self._data:
            self._event_bus.publish(event)
