# tests/unit/trading/test_execution/test_engine/test_results_collector.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.execution.engine.events.events import (
	AcceptedFillEvent,
	MarketDataEvent,
	OrderEvent,
	PortfolioSnapshotEvent,
	RejectedFillEvent,
)
from trading.execution.engine.results.results_collector import ResultsCollector


def test_results_collector_stores_accepted_fill_events() -> None:
	collector = ResultsCollector()
	event = AcceptedFillEvent(
		timestamp=1,
		market_event=MarketDataEvent(1, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000),
		order_event=OrderEvent(1, 5, "buy"),
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
		order_event=OrderEvent(1, 5, "buy"),
		reason="insufficient cash",
	)

	collector.collect_rejected_fill_event(event)

	assert collector.rejected_fill_events == [event]


def test_results_collector_stores_order_events() -> None:
	collector = ResultsCollector()
	event = OrderEvent(1, 5, "buy")

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
