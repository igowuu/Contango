# tests/unit/trading/test_execution/test_backtester/test_portfolio.py — part of Contango, a parameterized backtesting & execution framework
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

import pytest

from contango.trading.execution.backtester.config import BacktesterConfig, FillBehavior
from contango.trading.execution.backtester.portfolio.portfolio import Portfolio
from contango.trading.execution.engine.events.event_bus import EventBus
from contango.trading.execution.engine.events.events import AcceptedFillEvent, MarketDataEvent, OrderEvent, PortfolioSnapshotEvent


def _create_config() -> BacktesterConfig:
    return BacktesterConfig(
        initial_cash=1000.0,
        initial_position=0,
        fill=FillBehavior.INSTANT,
        slippage=0.0,
        commission_per_unit=0.0,
    )


def _create_market_event(timestamp: int = 1000, close: float = 100.0) -> MarketDataEvent:
    return MarketDataEvent(timestamp, "AAPL", 99.0, 101.0, 98.0, close, 1000)


def test_get_initial_snapshot_uses_timestamp_for_first_bar() -> None:
    portfolio = Portfolio(EventBus(), _create_config(), initial_cash=1000.0, initial_position=10)

    snapshot = portfolio.get_initial_snapshot(_create_market_event())

    assert snapshot == PortfolioSnapshotEvent(1000, 1000.0, 10, 2000.0)


def test_update_equity_publishes_snapshot_with_current_values() -> None:
    bus = EventBus()
    snapshots: list[PortfolioSnapshotEvent] = []
    bus.subscribe(PortfolioSnapshotEvent, snapshots.append, priority=0)

    portfolio = Portfolio(bus, _create_config(), initial_cash=1000.0, initial_position=10)
    portfolio.update_equity(_create_market_event(close=120.0))

    assert snapshots == [PortfolioSnapshotEvent(1000, 1000.0, 10, 2200.0)]


def test_apply_accepted_fill_updates_cash_position_and_snapshot() -> None:
    bus = EventBus()
    snapshots: list[PortfolioSnapshotEvent] = []
    bus.subscribe(PortfolioSnapshotEvent, snapshots.append, priority=0)

    portfolio = Portfolio(bus, _create_config(), initial_cash=1000.0, initial_position=0)
    trade = AcceptedFillEvent(
        timestamp=1000,
        market_event=_create_market_event(close=100.0),
        order_event=OrderEvent(1000, 5, "buy"),
        fill_price=100.0,
        total_cost=500.0,
    )

    portfolio.apply_accepted_fill(trade)

    assert snapshots == [PortfolioSnapshotEvent(1000, 500.0, 5, 1000.0)]


def test_apply_accepted_fill_raises_when_cash_would_go_negative() -> None:
    portfolio = Portfolio(EventBus(), _create_config(), initial_cash=100.0, initial_position=0)
    trade = AcceptedFillEvent(
        timestamp=1000,
        market_event=_create_market_event(close=100.0),
        order_event=OrderEvent(1000, 5, "buy"),
        fill_price=100.0,
        total_cost=500.0,
    )

    with pytest.raises(ValueError):
        portfolio.apply_accepted_fill(trade)