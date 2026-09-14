from __future__ import annotations

from contango.trading.execution.backtest.fill_behavior.fill_policy import BACKTESTER_FILL_POLICY
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


def _context(
    desired_quantity: int = 0,
    current_position: int = 0,
    total_cost: float = 0.0,
    current_cash: float = 1000.0,
) -> RuleContext:
    return RuleContext(
        desired_quantity=desired_quantity,
        current_position=current_position,
        total_cost=total_cost,
        current_cash=current_cash,
    )


def test_valid_buy_passes_all_rules() -> None:
    context = _context(desired_quantity=5, current_position=0, total_cost=500.0, current_cash=1000.0)

    assert BACKTESTER_FILL_POLICY.validate_rules(context) is None


def test_valid_full_sell_passes_all_rules() -> None:
    context = _context(desired_quantity=-5, current_position=5, total_cost=0.0, current_cash=1000.0)

    assert BACKTESTER_FILL_POLICY.validate_rules(context) is None


def test_insufficient_position_is_caught_before_other_rules() -> None:
    # Also violates pyramiding-adjacent shape, but insufficient position should surface first.
    context = _context(desired_quantity=-10, current_position=5, total_cost=0.0, current_cash=1000.0)

    assert BACKTESTER_FILL_POLICY.validate_rules(context) == (
        "Insufficient position - cannot sell more position than available."
    )


def test_pyramiding_is_caught_when_position_and_cash_are_otherwise_valid() -> None:
    context = _context(desired_quantity=5, current_position=10, total_cost=500.0, current_cash=1000.0)

    assert BACKTESTER_FILL_POLICY.validate_rules(context) == (
        "Pyramiding is not allowed. After buying units, all of the units must be sold; more cannot be bought."
    )


def test_partial_sell_is_caught_when_position_and_pyramiding_rules_pass() -> None:
    context = _context(desired_quantity=-4, current_position=10, total_cost=0.0, current_cash=1000.0)

    assert BACKTESTER_FILL_POLICY.validate_rules(context) == (
        "Only full trades (no partial trades) are allowed. All position must be sold; not part of it."
    )


def test_insufficient_cash_is_caught_last_when_earlier_rules_pass() -> None:
    context = _context(desired_quantity=5, current_position=0, total_cost=2000.0, current_cash=1000.0)

    assert BACKTESTER_FILL_POLICY.validate_rules(context) == "Not enough cash to make the trade."
