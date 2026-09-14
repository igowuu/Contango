from __future__ import annotations

from typing import Generic, TypeVar

from contango.trading.execution.engine.fills.fill_rule import FillRule


T = TypeVar("T")


class FillPolicy(Generic[T]):
    """
    The policy for a certain mode of trading to pre-validate that all trading rules are met.
    """
    def __init__(self, rules: tuple[FillRule[T], ...]) -> None:
        """
        Initializes `FillPolicy`.
        
        Args:
            rules: An iterable of fill rules for the policy.
        """
        self._rules = rules

    def validate_rules(self, context: T) -> str | None:
        """
        Validates all rules for the policy.

        Returns:
            str | None: The violation reason for the first violated rule, or `None` if none were violated.
        """
        for rule in self._rules:
            passing = rule.validate(context)

            if not passing:
                return rule.reason

        return None
