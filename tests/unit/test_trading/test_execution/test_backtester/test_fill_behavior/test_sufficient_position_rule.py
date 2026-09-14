from __future__ import annotations

from contango.trading.execution.backtest.fill_behavior.rules.sufficient_position_rule import SufficientPositionRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


def _context(desired_quantity: int, current_position: int) -> RuleContext:
    return RuleContext(
        desired_quantity=desired_quantity,
        current_position=current_position,
        total_cost=0.0,
        current_cash=0.0,
    )


def test_passes_when_selling_less_than_current_position() -> None:
    rule = SufficientPositionRule()

    assert rule.validate(_context(desired_quantity=-3, current_position=5)) is True


def test_passes_when_selling_exactly_the_full_position() -> None:
    rule = SufficientPositionRule()

    assert rule.validate(_context(desired_quantity=-5, current_position=5)) is True


def test_fails_when_selling_more_than_the_current_position() -> None:
    rule = SufficientPositionRule()

    assert rule.validate(_context(desired_quantity=-6, current_position=5)) is False


def test_passes_for_any_buy_regardless_of_position() -> None:
    rule = SufficientPositionRule()

    assert rule.validate(_context(desired_quantity=10, current_position=0)) is True


def test_reason_is_a_non_empty_string() -> None:
    assert SufficientPositionRule().reason
