from __future__ import annotations

from contango.trading.execution.engine.fills.fill_policy import FillPolicy
from contango.trading.execution.backtest.fill_behavior.rules.pyramiding_rule import PyramidingRule
from contango.trading.execution.backtest.fill_behavior.rules.partial_position_rule import PartialPositionRule
from contango.trading.execution.backtest.fill_behavior.rules.sufficient_position_rule import SufficientPositionRule
from contango.trading.execution.backtest.fill_behavior.rules.sufficient_cash_rule import SufficientCashRule
from contango.trading.execution.backtest.fill_behavior.rules.rule_context import RuleContext


BACKTESTER_FILL_POLICY = FillPolicy[RuleContext]((
    SufficientPositionRule(),
    PyramidingRule(),
    PartialPositionRule(),
    SufficientCashRule(),
))
