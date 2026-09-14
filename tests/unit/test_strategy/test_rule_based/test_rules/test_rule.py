from __future__ import annotations

from contango.trading.execution.engine.events.types import MarketDataEvent, PortfolioSnapshotEvent
from contango.strategy.rule_based.rules.rule import Rule
from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.strategy.rule_based.conditions.predicate import Predicate
from contango.strategy.rule_based.actions.emit import Emit
from contango.strategy.rule_based.intents.enter_long_intent import EnterLongIntent


def _fake_context() -> TradingContext:
    return TradingContext(
        MarketDataEvent(0, "", 0, 0, 0, 0, 0),
        PortfolioSnapshotEvent(0, 0, 0, 0)
    )


def test_rule_executes_action_when_condition_is_true() -> None:
    intent = EnterLongIntent(symbol="AAPL")
    rule = Rule(Predicate(lambda ctx: True), Emit(intent))

    assert rule.evaluate(_fake_context()) is intent


def test_rule_returns_none_when_condition_is_false() -> None:
    intent = EnterLongIntent(symbol="AAPL")
    rule = Rule(Predicate(lambda ctx: False), Emit(intent))

    assert rule.evaluate(_fake_context()) is None


def test_rule_condition_receives_the_context_passed_to_evaluate() -> None:
    received: list[TradingContext] = []
    rule = Rule(
        Predicate(lambda ctx: received.append(ctx) or True),
        Emit(EnterLongIntent(symbol="AAPL")),
    )
    context = _fake_context()

    rule.evaluate(context)

    assert received == [context]