from __future__ import annotations

from typing import TypeVar, Generic
from abc import ABC, abstractmethod

from contango.strategy.rule_based.contexts.context import Context


R = TypeVar("R")
C = TypeVar("C", bound=Context)


class Action(ABC, Generic[C, R]):
    """
    An object that executes a single action or behavior.

    Attributes:
        C: The context type for the action to be passed into the execute() method.
        R: The return type for the action when executed.
    """
    @abstractmethod
    def execute(self, context: C) -> R:
        """
        Executes the behavior of the action.
        """
        ...
