from __future__ import annotations

from dataclasses import dataclass

from contango.strategy.rule_based.intents.intent import Intent


@dataclass(frozen=True, slots=True)
class EnterLongIntent(Intent):
    """
    Enters a long trade with a provided symbol.
    """
    symbol: str
