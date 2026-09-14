from __future__ import annotations

from contango.trading.execution.engine.fills.fill_rule import FillRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


class PyramidingRule(FillRule[RuleContext]):
    """
    Rule that does not allow two subsequent positive orders.
    """
    @property
    def reason(self) -> str:
        return "Pyramiding is not allowed. After buying units, all of the units must be sold; more cannot be bought."

    def validate(self, context: RuleContext) -> bool:
        """
        Returns True upon correctly selling shares when the last order was a buy.
        """
        return not (
            context.current_position > 0
            and context.desired_quantity > 0
        )
