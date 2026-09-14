from __future__ import annotations

from typing import Generic, TypeVar

from contango.strategy.rule_based.conditions.condition import Condition
from contango.strategy.rule_based.actions.action import Action
from contango.strategy.rule_based.contexts.context import Context


R = TypeVar("R", covariant=True)
C = TypeVar("C", bound=Context, contravariant=True)


class Rule(Generic[C, R]):
    """
    Executes an action upon a condition being True.

    Attributes:
        C: The context for the rule.
        R: The return type for the rule.
    """
    def __init__(self, when: Condition[C], then: Action[C, R]) -> None:
        """
        Initializes a `Rule` with a condition & action.
        """
        self._when = when
        self._then = then

    def evaluate(self, context: C) -> R | None:
        """
        Evaluates the status of the condition, executing & returning the output from the action if True.
        """
        if self._when.evaluate(context):
            return self._then.execute(context)
