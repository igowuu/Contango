from __future__ import annotations

from contango.trading.execution.backtest.fill_behavior.rules.pyramiding_rule import PyramidingRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


def _context(desired_quantity: int, current_position: int) -> RuleContext:
    return RuleContext(
        desired_quantity=desired_quantity,
        current_position=current_position,
        total_cost=0.0,
        current_cash=0.0,
    )


def test_fails_when_already_long_and_buying_more() -> None:
    rule = PyramidingRule()

    assert rule.validate(_context(desired_quantity=5, current_position=10)) is False


def test_passes_when_flat_and_making_the_initial_buy() -> None:
    rule = PyramidingRule()

    assert rule.validate(_context(desired_quantity=5, current_position=0)) is True


def test_passes_when_long_and_selling() -> None:
    rule = PyramidingRule()

    assert rule.validate(_context(desired_quantity=-5, current_position=10)) is True


def test_passes_when_long_and_desired_quantity_is_zero() -> None:
    rule = PyramidingRule()

    assert rule.validate(_context(desired_quantity=0, current_position=10)) is True


def test_reason_is_a_non_empty_string() -> None:
    assert PyramidingRule().reason
