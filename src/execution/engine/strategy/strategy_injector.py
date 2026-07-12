from __future__ import annotations

from execution.engine.events.events import PortfolioSnapshotEvent
from execution.engine.strategy.strategy import Strategy


class StrategyInjector:
    """
    Injects snapshot events into the strategy upon them being updated.
    """
    def __init__(self, strategy: Strategy) -> None:
        """
        Initializes `StrategyInjector`.
        
        Args:
            strategy: The underlying `Strategy` instance to inject to.
        """
        self._strategy = strategy

    def inject_portfolio_event(self, event: PortfolioSnapshotEvent) -> None:
        """
        Injects a `PortfolioSnapshotEvent` into the strategy upon publication.
        """
        self._strategy.portfolio_snapshot = event
