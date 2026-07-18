from __future__ import annotations

from execution.backtester.market.feed import MarketDataFeed
from execution.engine.events.event_bus import EventBus
from execution.engine.events.events import MarketDataEvent


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
