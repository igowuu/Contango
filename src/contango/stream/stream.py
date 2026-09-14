from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from contango.trading.execution.engine.events.types import MarketDataEvent


R = TypeVar("R")


class Stream(ABC, Generic[R]):
    """
    Base class for anything that produces a value per market event.

    Attributes:
        R: The return type for the stream.
    """
    @abstractmethod
    def update(self, event: MarketDataEvent) -> R:
        """
        Updates the state of the stream given a market data event.

        Returns:    
            The updated value.
        """
        ...
    
    @property
    @abstractmethod
    def value(self) -> R:
        """
        Returns the most recent value of the stream.
        """
        ...
