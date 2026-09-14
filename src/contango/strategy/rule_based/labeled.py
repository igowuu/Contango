from __future__ import annotations

from abc import ABC, abstractmethod


class Labeled(ABC):
    """
    Marks a class as an implementer of __str__.
    """
    @abstractmethod
    def __str__(self) -> str:
        """
        Returns a string representation of the class.
        """
        ...
