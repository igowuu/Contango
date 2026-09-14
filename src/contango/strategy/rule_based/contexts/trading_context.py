from __future__ import annotations

from dataclasses import dataclass

from contango.strategy.rule_based.contexts.context import Context
from contango.trading.execution.engine.events.types import MarketDataEvent, PortfolioSnapshotEvent


@dataclass(frozen=True, slots=True)
class TradingContext(Context):
    """
    A specific context for trading strategies.
    
    Attributes:
        event: The underlying market data event for the current context snapshot.
        portfolio: The portfolio event for the current context snapshot.
    """
    event: MarketDataEvent
    portfolio: PortfolioSnapshotEvent
