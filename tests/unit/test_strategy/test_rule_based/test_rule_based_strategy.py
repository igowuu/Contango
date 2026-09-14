from __future__ import annotations

from dataclasses import dataclass

import pytest
from typing import Any

from contango.strategy.rule_based.rule_based_strategy import RuleBasedStrategy
from contango.strategy.rule_based.rules.rule import Rule
from contango.strategy.rule_based.conditions.predicate import Predicate
from contango.strategy.rule_based.actions.emit import Emit
from contango.strategy.rule_based.intents.intent import Intent
from contango.strategy.rule_based.intents.enter_long_intent import EnterLongIntent
from contango.strategy.rule_based.intents.exit_long_intent import ExitLongIntent
from contango.strategy.rule_based.position_sizers.fixed_position_sizer import FixedPositionSizer
from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.strategy.rule_based.position_sizers.position_sizer import PositionSizer
from contango.stream.indicators.indicator import Indicator

from contango.trading.execution.engine.events.event_bus import EventBus
from contango.trading.execution.engine.events.types import MarketDataEvent, OrderEvent, PortfolioSnapshotEvent
from contango.trading.execution.engine.orders.order_api import OrderAPI


class _CountingIndicator(Indicator[int]):
    def __init__(self) -> None:
        self.updates = 0
        self.last_event: MarketDataEvent | None = None

    def update(self, event: MarketDataEvent) -> int:
        self.updates += 1
        self.last_event = event
        return self.updates

    @property
    def value(self) -> int:
        return self.updates

    def __repr__(self) -> str:
        return ""


@dataclass(frozen=True, slots=True)
class _UnknownIntent(Intent):
    ...


def _create_market_event(timestamp: int = 1000, symbol: str = "AAPL", close: float = 100.0) -> MarketDataEvent:
    return MarketDataEvent(timestamp, symbol, close, close, close, close, 1000)


def _create_strategy(
    rules: list[Rule[TradingContext, Intent]],
    position_sizer: None | PositionSizer[Any] = None,
    indicators: None | list[Indicator[int]] = None,
    cash: float = 1000.0,
    position: int = 0,
) -> tuple[RuleBasedStrategy, EventBus, list[OrderEvent]]:
    strategy = RuleBasedStrategy(
        streams=indicators or [],
        rules=rules,
        position_sizer=position_sizer or FixedPositionSizer(fixed_units=1),
    )

    bus = EventBus()
    orders: list[OrderEvent] = []
    bus.subscribe(OrderEvent, orders.append, priority=0)

    strategy.order_api = OrderAPI(bus)
    strategy.portfolio_snapshot = PortfolioSnapshotEvent(1000, cash, position, cash)

    return strategy, bus, orders


def test_on_market_event_updates_every_registered_indicator() -> None:
    indicator_a = _CountingIndicator()
    indicator_b = _CountingIndicator()
    strategy, _, _ = _create_strategy(
        rules=[], indicators=[indicator_a, indicator_b]
    )
    event = _create_market_event()

    strategy.on_market_event(event)

    assert indicator_a.updates == 1
    assert indicator_a.last_event is event
    assert indicator_b.updates == 1
    assert indicator_b.last_event is event


def test_on_market_event_skips_rules_that_return_none() -> None:
    rule = Rule(Predicate(lambda ctx: False), Emit(EnterLongIntent(symbol="AAPL")))
    strategy, _, orders = _create_strategy(rules=[rule])

    strategy.on_market_event(_create_market_event())

    assert orders == []


def test_on_market_event_submits_buy_order_sized_by_position_sizer_for_enter_long() -> None:
    rule = Rule(Predicate(lambda ctx: True), Emit(EnterLongIntent(symbol="AAPL")))
    strategy, _, orders = _create_strategy(
        rules=[rule], position_sizer=FixedPositionSizer(fixed_units=7)
    )

    strategy.on_market_event(_create_market_event(timestamp=2000))

    assert len(orders) == 1
    assert orders[0].timestamp == 2000
    assert orders[0].quantity == 7


def test_on_market_event_submits_sell_order_for_full_position_on_exit_intent() -> None:
    rule = Rule(Predicate(lambda ctx: True), Emit(ExitLongIntent(symbol="AAPL")))
    strategy, _, orders = _create_strategy(rules=[rule], position=5)

    strategy.on_market_event(_create_market_event())

    assert len(orders) == 1
    assert orders[0].quantity == -5


def test_on_market_event_exit_intent_is_noop_when_no_open_position() -> None:
    rule = Rule(Predicate(lambda ctx: True), Emit(ExitLongIntent(symbol="AAPL")))
    strategy, _, orders = _create_strategy(rules=[rule], position=0)

    strategy.on_market_event(_create_market_event())

    assert orders == []


def test_on_market_event_raises_for_unhandled_intent_type() -> None:
    rule = Rule(Predicate(lambda ctx: True), Emit(_UnknownIntent()))
    strategy, _, _ = _create_strategy(rules=[rule])

    with pytest.raises(RuntimeError):
        strategy.on_market_event(_create_market_event())


def test_on_end_closes_open_position_using_final_market_event() -> None:
    strategy, _, orders = _create_strategy(rules=[], position=5)
    final_event = _create_market_event(timestamp=3000, symbol="AAPL")
    strategy.on_market_event(final_event)

    strategy.on_end()

    assert len(orders) == 1
    assert orders[0].timestamp == 3000
    assert orders[0].quantity == -5


def test_on_end_is_noop_when_no_open_position() -> None:
    strategy, _, orders = _create_strategy(rules=[], position=0)
    strategy.on_market_event(_create_market_event())

    strategy.on_end()

    assert orders == []


def test_on_end_raises_when_no_market_event_was_ever_received() -> None:
    strategy, _, _ = _create_strategy(rules=[], position=5)

    with pytest.raises(ValueError):
        strategy.on_end()
