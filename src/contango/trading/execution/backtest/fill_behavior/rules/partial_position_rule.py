from __future__ import annotations

from contango.trading.execution.engine.fills.fill_rule import FillRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


class PartialPositionRule(FillRule[RuleContext]):
    """
    Rule that only allows full trades (no partial trades).
    This means that you must sell all of the shares you bought in a previous order every time.
    """
    @property
    def reason(self) -> str:
        return "Only full trades (no partial trades) are allowed. All position must be sold; not part of it."

    def validate(self, context: RuleContext) -> bool:
        """
        Returns True if there is currently a position & the desired quantity is negative, and adding the 
        current posiiton and desired quantity correctly results in no position.
        """
        if context.desired_quantity >= 0:
            return True

        return (
            context.current_position > 0
            and context.current_position + context.desired_quantity == 0
        )
