# tests/unit/trading/test_execution/test_engine/test_order_api.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.execution.engine.events.event_bus import EventBus
from contango.trading.execution.engine.events.events import MarketDataEvent, OrderEvent
from contango.trading.execution.engine.orders.order_api import OrderAPI


def test_submit_order_publishes_order_event_with_expected_fields() -> None:
	bus = EventBus()
	received: list[OrderEvent] = []
	bus.subscribe(OrderEvent, received.append, priority=0)

	api = OrderAPI(bus)
	market_data = MarketDataEvent(
		timestamp=1234567890,
		symbol="AAPL",
		open=100.0,
		high=101.0,
		low=99.0,
		close=100.5,
		volume=1000,
	)

	api.submit_order(
		market_data=market_data,
		symbol="AAPL",
		quantity=25,
		reason="test order",
	)

	assert len(received) == 1

	order = received[0]
	assert order.timestamp == market_data.timestamp
	assert order.quantity == 25
	assert order.reason == "test order"


def test_submit_order_allows_missing_reason() -> None:
	bus = EventBus()
	received: list[OrderEvent] = []
	bus.subscribe(OrderEvent, received.append, priority=0)

	api = OrderAPI(bus)
	market_data = MarketDataEvent(
		timestamp=1234567890,
		symbol="AAPL",
		open=100.0,
		high=101.0,
		low=99.0,
		close=100.5,
		volume=1000,
	)

	api.submit_order(
		market_data=market_data,
		symbol="AAPL",
		quantity=-10,
	)

	assert len(received) == 1
	assert received[0].reason is None
