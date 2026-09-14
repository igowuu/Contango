from __future__ import annotations

from typing import TypeVar, Generic

from abc import ABC, abstractmethod
from contango.stream.stream import Stream


R = TypeVar("R")
USD = float


class Indicator(Generic[R], Stream[R], ABC):
    """
    Base class for all per-bar indicators.

    Attributes:
        R: The return type for the indicator.
    """
    @abstractmethod
    def __repr__(self) -> str:
        """
        Returns a string representation of the indicator.
        """
        ...
