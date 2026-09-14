from __future__ import annotations

from contango.trading.execution.engine.fills.fill_rule import FillRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


class SufficientPositionRule(FillRule[RuleContext]):
    """
    Rule that only allows a sufficient position, disallowing selling more position than available.
    """
    @property
    def reason(self) -> str:
        return "Insufficient position - cannot sell more position than available."

    def validate(self, context: RuleContext) -> bool:
        """
        Returns True if the desired quantity does not result in the position becoming negative.
        """
        return (context.desired_quantity + context.current_position) >= 0
