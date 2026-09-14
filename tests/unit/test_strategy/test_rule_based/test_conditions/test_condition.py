from __future__ import annotations

from contango.trading.execution.engine.events.types import MarketDataEvent, PortfolioSnapshotEvent
from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.strategy.rule_based.conditions.condition import Condition
from contango.strategy.rule_based.conditions.predicate import Predicate


def _fake_context(close: float) -> TradingContext:
    return TradingContext(
        MarketDataEvent(0, "", 0, 0, 0, close, 0),
        PortfolioSnapshotEvent(0, 0, 0, 0)
    )


def test_predicate_evaluates_wrapped_callable() -> None:
    predicate = Predicate(lambda ctx: ctx.event.close > 5)

    assert predicate.evaluate(_fake_context(10)) is True
    assert predicate.evaluate(_fake_context(1)) is False


def test_and_returns_true_only_when_both_true() -> None:
    always_true = Predicate(lambda ctx: True)
    always_false = Predicate(lambda ctx: False)

    assert (always_true & always_true).evaluate(_fake_context(0)) is True
    assert (always_true & always_false).evaluate(_fake_context(0)) is False
    assert (always_false & always_false).evaluate(_fake_context(0)) is False


def test_or_returns_true_when_either_true() -> None:
    always_true = Predicate(lambda ctx: True)
    always_false = Predicate(lambda ctx: False)

    assert (always_true | always_false).evaluate(_fake_context(0)) is True
    assert (always_false | always_true).evaluate(_fake_context(0)) is True
    assert (always_false | always_false).evaluate(_fake_context(0)) is False


def test_not_inverts_evaluation() -> None:
    always_true = Predicate(lambda ctx: True)
    always_false = Predicate(lambda ctx: False)

    assert (~always_true).evaluate(_fake_context(0)) is False
    assert (~always_false).evaluate(_fake_context(0)) is True


def test_composed_conditions_evaluate_correctly() -> None:
    greater_than_five = Predicate(lambda ctx: ctx.event.close > 5)
    less_than_ten = Predicate(lambda ctx: ctx.event.close < 10)

    composed: Condition[TradingContext] = greater_than_five & ~less_than_ten

    assert composed.evaluate(_fake_context(15)) is True
    assert composed.evaluate(_fake_context(7)) is False
