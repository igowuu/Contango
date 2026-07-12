from __future__ import annotations

from execution.engine.events.events import (
	AcceptedFillEvent,
	MarketDataEvent,
	OrderEvent,
	PortfolioSnapshotEvent,
	RejectedFillEvent,
)
from execution.engine.results.results_collector import ResultsCollector


def test_results_collector_stores_accepted_fill_events() -> None:
	collector = ResultsCollector()
	event = AcceptedFillEvent(
		timestamp=1,
		market_event=MarketDataEvent(1, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000),
		order_event=OrderEvent(1, "AAPL", 5, "buy"),
		fill_price=100.5,
		total_cost=502.5,
	)

	collector.collect_accepted_fill_event(event)

	assert collector.accepted_fill_events == [event]


def test_results_collector_stores_rejected_fill_events() -> None:
	collector = ResultsCollector()
	event = RejectedFillEvent(
		timestamp=1,
		market_event=MarketDataEvent(1, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000),
		order_event=OrderEvent(1, "AAPL", 5, "buy"),
		reason="insufficient cash",
	)

	collector.collect_rejected_fill_event(event)

	assert collector.rejected_fill_events == [event]


def test_results_collector_stores_order_events() -> None:
	collector = ResultsCollector()
	event = OrderEvent(1, "AAPL", 5, "buy")

	collector.collect_order_event(event)

	assert collector.order_events == [event]


def test_results_collector_stores_market_data_events() -> None:
	collector = ResultsCollector()
	event = MarketDataEvent(1, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000)

	collector.collect_market_data_event(event)

	assert collector.market_data_events == [event]


def test_results_collector_stores_portfolio_snapshot_events() -> None:
	collector = ResultsCollector()
	event = PortfolioSnapshotEvent(1, 1000.0, 10, 1500.0)

	collector.collect_portfolio_snapshot_event(event)

	assert collector.portfolio_snapshot_events == [event]
