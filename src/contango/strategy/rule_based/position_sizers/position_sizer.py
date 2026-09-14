from __future__ import annotations

from typing import TypeVar, Generic
from abc import ABC, abstractmethod

from contango.strategy.rule_based.contexts.context import Context
from contango.strategy.rule_based.labeled import Labeled

from contango.trading.execution.engine.events.types import MarketDataEvent


C = TypeVar("C", bound=Context)


class PositionSizer(Labeled, ABC, Generic[C]):
    """
    Decides how many units to trade when an intent is published.

    Attributes:
        C: The context for the `PositionSizer`.
    """
    def update(self, event: MarketDataEvent) -> None:
        """
        Updates the state of the position sizer with the latest market data event.
        """
        pass

    @abstractmethod
    def size(self, context: C) -> int:
        """
        Returns the size in units for the given context.
        """
        ...
