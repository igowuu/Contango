from __future__ import annotations

from typing import TypeVar, Generic
from abc import ABC, abstractmethod


T = TypeVar("T")


class FillRule(ABC, Generic[T]):
    """
    A single rule for validation when attempting to fill an order.
    """
    @property
    @abstractmethod
    def reason(self) -> str:
        """
        Returns the reason displayed upon the rule failing.
        """
        ...

    @abstractmethod
    def validate(self, context: T) -> bool:
        """
        Validates the state of the given rule for a policy.

        Returns:
            Whether or not the rule passed validation.
        """
        ...
