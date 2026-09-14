from __future__ import annotations

from contango.trading.execution.backtest.fill_behavior.rules.sufficient_cash_rule import SufficientCashRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


def _context(total_cost: float, current_cash: float) -> RuleContext:
    return RuleContext(
        desired_quantity=0,
        current_position=0,
        total_cost=total_cost,
        current_cash=current_cash,
    )


def test_passes_when_cost_is_less_than_available_cash() -> None:
    rule = SufficientCashRule()

    assert rule.validate(_context(total_cost=50.0, current_cash=100.0)) is True


def test_passes_when_cost_exactly_equals_available_cash() -> None:
    rule = SufficientCashRule()

    assert rule.validate(_context(total_cost=100.0, current_cash=100.0)) is True


def test_fails_when_cost_exceeds_available_cash() -> None:
    rule = SufficientCashRule()

    assert rule.validate(_context(total_cost=101.0, current_cash=100.0)) is False


def test_reason_is_a_non_empty_string() -> None:
    assert SufficientCashRule().reason
