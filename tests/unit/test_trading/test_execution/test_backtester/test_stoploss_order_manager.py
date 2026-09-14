from __future__ import annotations

from contango.trading.execution.backtest.orders.stoploss_order_manager import StoplossOrderManager
from contango.trading.execution.engine.events.event_bus import EventBus
from contango.trading.execution.engine.events.types import (
    MarketDataEvent,
    OrderEvent,
    PortfolioSnapshotEvent,
    StoplossOrderEvent,
)


def _bar(timestamp: int = 1000, close: float = 100.0) -> MarketDataEvent:
    return MarketDataEvent(timestamp, "AAPL", close, close, close, close, 1000)


def _snapshot(timestamp: int, position: int, cash: float = 1000.0) -> PortfolioSnapshotEvent:
    return PortfolioSnapshotEvent(timestamp, cash, position, cash)


def _manager_with_bus() -> tuple[StoplossOrderManager, EventBus, list[OrderEvent]]:
    bus = EventBus()
    orders: list[OrderEvent] = []
    bus.subscribe(OrderEvent, orders.append, priority=0)
    return StoplossOrderManager(bus), bus, orders


def test_no_publish_when_no_portfolio_snapshots_have_been_collected() -> None:
    manager, _, orders = _manager_with_bus()
    manager.collect_stoploss_order_event(StoplossOrderEvent(1000, 5, stop_price=90.0))

    manager.check_if_stoploss_met(_bar(close=80.0))

    assert orders == []


def test_no_publish_when_only_one_portfolio_snapshot_has_been_collected() -> None:
    manager, _, orders = _manager_with_bus()
    manager.collect_stoploss_order_event(StoplossOrderEvent(1000, 5, stop_price=90.0))
    manager.collect_portfolio_snapshot(_snapshot(1000, position=5))

    manager.check_if_stoploss_met(_bar(close=80.0))

    assert orders == []


def test_no_publish_when_there_is_no_pending_stoploss_order() -> None:
    manager, _, orders = _manager_with_bus()
    manager.collect_portfolio_snapshot(_snapshot(1000, position=5))
    manager.collect_portfolio_snapshot(_snapshot(2000, position=5))

    manager.check_if_stoploss_met(_bar(close=1.0))

    assert orders == []


def test_no_publish_when_close_is_above_the_stop_price() -> None:
    manager, _, orders = _manager_with_bus()
    manager.collect_stoploss_order_event(StoplossOrderEvent(1000, 5, stop_price=90.0))
    manager.collect_portfolio_snapshot(_snapshot(1000, position=5))
    manager.collect_portfolio_snapshot(_snapshot(2000, position=5))

    manager.check_if_stoploss_met(_bar(timestamp=3000, close=95.0))

    assert orders == []


def test_publishes_sell_order_when_close_breaches_the_stop_price() -> None:
    manager, _, orders = _manager_with_bus()
    manager.collect_stoploss_order_event(StoplossOrderEvent(1000, 5, stop_price=90.0))
    manager.collect_portfolio_snapshot(_snapshot(1000, position=5))
    manager.collect_portfolio_snapshot(_snapshot(2000, position=5))

    manager.check_if_stoploss_met(_bar(timestamp=3000, close=85.0))

    assert len(orders) == 1
    assert orders[0].timestamp == 3000
    assert orders[0].quantity == -5
    assert orders[0].reason == "Stoploss was met."


def test_pending_stoploss_is_cleared_after_being_triggered() -> None:
    manager, _, orders = _manager_with_bus()
    manager.collect_stoploss_order_event(StoplossOrderEvent(1000, 5, stop_price=90.0))
    manager.collect_portfolio_snapshot(_snapshot(1000, position=5))
    manager.collect_portfolio_snapshot(_snapshot(2000, position=5))
    manager.check_if_stoploss_met(_bar(timestamp=3000, close=85.0))

    # A second breach-worthy bar should not re-trigger since the stoploss already fired.
    manager.collect_portfolio_snapshot(_snapshot(4000, position=0))
    manager.collect_portfolio_snapshot(_snapshot(5000, position=0))
    manager.check_if_stoploss_met(_bar(timestamp=6000, close=80.0))

    assert len(orders) == 1


def test_pending_stoploss_is_cleared_when_position_is_closed_manually() -> None:
    manager, _, orders = _manager_with_bus()
    manager.collect_stoploss_order_event(StoplossOrderEvent(1000, 5, stop_price=90.0))
    manager.collect_portfolio_snapshot(_snapshot(1000, position=5))

    manager.collect_portfolio_snapshot(_snapshot(2000, position=0))
    manager.check_if_stoploss_met(_bar(timestamp=3000, close=1.0))

    assert orders == []
