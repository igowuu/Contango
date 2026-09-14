from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Intent:
    """
    Any intent for a rule, whether it be an intent to create a trade, exit a trade, etc.
    """
    ...
