from __future__ import annotations

from contango.trading.execution.engine.fills.fill_rule import FillRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


class SufficientCashRule(FillRule[RuleContext]):
    """
    Rule that only allows trades with sufficient cash.
    """
    @property
    def reason(self) -> str:
        return "Not enough cash to make the trade."

    def validate(self, context: RuleContext) -> bool:
        """
        Returns True if the desired quantity does not result in the position becoming negative.
        """
        return context.total_cost <= context.current_cash
