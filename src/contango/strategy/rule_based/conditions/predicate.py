from __future__ import annotations

from typing import Callable

from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.strategy.rule_based.conditions.condition import Condition


class Predicate(Condition[TradingContext]):
    """
    A lambda expression that evaluates to a boolean.
    """
    def __init__(self, fn: Callable[[TradingContext], bool]) -> None:
        """
        Initializes `Predicate`.
        
        Args:   
            fn: The callable that returns a boolean.
        """
        self._fn = fn

    def evaluate(self, context: TradingContext) -> bool:
        """
        Evaluates the state of the predicate.
        
        Args:
            context: The current context to feed into the lambda.
        
        Returns:
            bool: The boolean value of the lambda.
        """
        return self._fn(context)

    def __str__(self) -> str:
        return "Predicate"
