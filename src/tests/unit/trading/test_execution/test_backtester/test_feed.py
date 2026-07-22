# tests/unit/trading/test_execution/test_backtester/test_feed.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.execution.backtester.market.feed import MarketDataFeed
from trading.execution.engine.events.event_bus import EventBus
from trading.execution.engine.events.events import MarketDataEvent


def _create_valid_data() -> list[MarketDataEvent]:
    data = [
        MarketDataEvent(1000, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000),
        MarketDataEvent(2000, "AAPL", 101.0, 102.0, 100.0, 101.5, 1100),
    ]
    return data


def test_get_initial_event_returns_first_row() -> None:
    feed = MarketDataFeed(_create_valid_data(), EventBus())

    event = feed.get_initial_event()

    assert event == MarketDataEvent(1000, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000)


def test_run_publishes_all_rows_in_order() -> None:
    bus = EventBus()
    received: list[MarketDataEvent] = []
    bus.subscribe(MarketDataEvent, received.append, priority=0)

    feed = MarketDataFeed(_create_valid_data(), bus)
    feed.run()

    assert received == [
        MarketDataEvent(1000, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000),
        MarketDataEvent(2000, "AAPL", 101.0, 102.0, 100.0, 101.5, 1100),
    ]
