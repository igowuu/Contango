from __future__ import annotations

from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Context(ABC):
    """
    The necessary context that anything related to strategy creation may need.
    """
    ...
