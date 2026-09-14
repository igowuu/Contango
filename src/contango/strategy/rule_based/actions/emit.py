from __future__ import annotations

from typing import Generic, TypeVar

from contango.strategy.rule_based.actions.action import Action
from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.strategy.rule_based.intents.intent import Intent


INTENT_T = TypeVar("INTENT_T", bound=Intent)


class Emit(Action[TradingContext, INTENT_T], Generic[INTENT_T]):
    """
    A simple action that emits an intent.

    Attributes:
        INTENT_T: The intent type that the execute() method will always return.
    """
    def __init__(self, intent: INTENT_T) -> None:
        """
        Initializes `Emit`.
        
        Args:
            intent: The intent to release what the action is executed.
        """
        self._intent = intent

    def execute(self, context: TradingContext) -> INTENT_T:
        """
        Executes the `Emit` action.
        
        Args:
            context: The context (unused) for the current market data event.
        
        Returns:
            INTENT_T: The unchanging intent to emit.
        """
        return self._intent
