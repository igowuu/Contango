from __future__ import annotations

from execution.engine.events.event_bus import EventBus
from execution.engine.events.events import MarketDataEvent, OrderEvent
from execution.engine.orders.order_api import OrderAPI


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
	assert order.symbol == "AAPL"
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
