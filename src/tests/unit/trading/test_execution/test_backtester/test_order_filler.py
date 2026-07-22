# tests/unit/trading/test_execution/test_backtester/test_order_filler.py — part of Contango, a parameterized backtesting & execution framework
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

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pytest

from trading.execution.backtester.config import BacktesterConfig, FillBehavior
from trading.execution.backtester.orders.order_filler import OrderFiller
from trading.execution.engine.events.event_bus import EventBus
from trading.execution.engine.events.events import (
    AcceptedFillEvent,
    MarketDataEvent,
    OrderEvent,
    PortfolioSnapshotEvent,
    RejectedFillEvent,
)


def _create_config(slippage: float = 0.0, commission_per_unit: float = 0.0) -> BacktesterConfig:
    return BacktesterConfig(
        initial_cash=1000.0,
        initial_position=0,
        fill=FillBehavior.INSTANT,
        slippage=slippage,
        commission_per_unit=commission_per_unit,
    )


def _create_market_event() -> MarketDataEvent:
    return MarketDataEvent(1000, "AAPL", 100.0, 101.0, 99.0, 100.0, 1000)


def _create_snapshot(cash: float = 1000.0, position: int = 0) -> PortfolioSnapshotEvent:
    return PortfolioSnapshotEvent(999, cash, position, cash)


def test_resolve_fill_price_returns_close_for_instant_fill() -> None:
    filler = OrderFiller(_create_config(), EventBus())

    assert filler._resolve_fill_price(_create_market_event()) == 100.0


def test_apply_slippage_adjusts_buys_and_sells() -> None:
    filler = OrderFiller(_create_config(slippage=0.1), EventBus())

    buy = OrderEvent(1000, "AAPL", 1, None)
    sell = OrderEvent(1000, "AAPL", -1, None)

    assert filler._apply_slippage(buy, 100.0) == pytest.approx(110.0)
    assert filler._apply_slippage(sell, 100.0) == pytest.approx(90.9090909091)


def test_calculate_commission_uses_absolute_quantity() -> None:
    filler = OrderFiller(_create_config(commission_per_unit=2.5), EventBus())

    assert filler._calculate_commission(OrderEvent(1000, "AAPL", -4, None)) == pytest.approx(10.0)


def test_fill_order_publishes_accepted_fill_with_total_cost() -> None:
    bus = EventBus()
    accepted: list[AcceptedFillEvent] = []
    bus.subscribe(AcceptedFillEvent, accepted.append, priority=0)

    filler = OrderFiller(_create_config(slippage=0.1, commission_per_unit=1.0), bus)
    market_event = _create_market_event()
    filler.collect_market_data(market_event)
    filler.collect_portfolio_snapshot(_create_snapshot(cash=500.0, position=0))

    filler.fill_order_event(OrderEvent(1000, "AAPL", 2, "buy"))

    assert len(accepted) == 1
    assert accepted[0].fill_price == 100.0
    assert accepted[0].total_cost == pytest.approx(222.0)


def test_fill_order_rejects_when_cash_is_insufficient() -> None:
    bus = EventBus()
    rejected: list[RejectedFillEvent] = []
    bus.subscribe(RejectedFillEvent, rejected.append, priority=0)

    filler = OrderFiller(_create_config(), bus)
    filler.collect_market_data(_create_market_event())
    filler.collect_portfolio_snapshot(_create_snapshot(cash=50.0, position=0))

    filler.fill_order_event(OrderEvent(1000, "AAPL", 1, "buy"))

    assert len(rejected) == 1
    assert rejected[0].reason == "Insufficient available cash (slippage & commission applied)"


def test_fill_order_rejects_when_position_is_insufficient() -> None:
    bus = EventBus()
    rejected: list[RejectedFillEvent] = []
    bus.subscribe(RejectedFillEvent, rejected.append, priority=0)

    filler = OrderFiller(_create_config(), bus)
    filler.collect_market_data(_create_market_event())
    filler.collect_portfolio_snapshot(_create_snapshot(cash=1000.0, position=1))

    filler.fill_order_event(OrderEvent(1000, "AAPL", -2, "sell"))

    assert len(rejected) == 1
    assert rejected[0].reason == "Insufficient position"


def test_fill_order_requires_market_event_before_order() -> None:
    filler = OrderFiller(_create_config(), EventBus())
    filler.collect_portfolio_snapshot(_create_snapshot())

    with pytest.raises(RuntimeError):
        filler.fill_order_event(OrderEvent(1000, "AAPL", 1, None))


def test_fill_order_requires_portfolio_snapshot_before_order() -> None:
    filler = OrderFiller(_create_config(), EventBus())
    filler.collect_market_data(_create_market_event())

    with pytest.raises(RuntimeError):
        filler.fill_order_event(OrderEvent(1000, "AAPL", 1, None))