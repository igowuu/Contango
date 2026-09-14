from __future__ import annotations

from contango.trading.execution.backtest.fill_behavior.rules.partial_position_rule import PartialPositionRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


def _context(desired_quantity: int, current_position: int) -> RuleContext:
    return RuleContext(
        desired_quantity=desired_quantity,
        current_position=current_position,
        total_cost=0.0,
        current_cash=0.0,
    )


def test_passes_for_any_buy() -> None:
    rule = PartialPositionRule()

    assert rule.validate(_context(desired_quantity=5, current_position=0)) is True


def test_passes_when_desired_quantity_is_zero() -> None:
    rule = PartialPositionRule()

    assert rule.validate(_context(desired_quantity=0, current_position=10)) is True


def test_passes_when_selling_the_entire_position() -> None:
    rule = PartialPositionRule()

    assert rule.validate(_context(desired_quantity=-10, current_position=10)) is True


def test_fails_when_selling_only_part_of_the_position() -> None:
    rule = PartialPositionRule()

    assert rule.validate(_context(desired_quantity=-4, current_position=10)) is False


def test_fails_when_selling_with_no_open_position() -> None:
    rule = PartialPositionRule()

    assert rule.validate(_context(desired_quantity=-4, current_position=0)) is False


def test_reason_is_a_non_empty_string() -> None:
    assert PartialPositionRule().reason
