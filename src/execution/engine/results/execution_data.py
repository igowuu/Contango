from __future__ import annotations

from typing import NamedTuple

from execution.engine.events.events import (
    AcceptedFillEvent, 
    RejectedFillEvent, 
    OrderEvent, 
    MarketDataEvent, 
    PortfolioSnapshotEvent
)


class ExecutionData(NamedTuple):
    """
    The accumulated execution data for analysis.

    Attributes:
        accepted_fill_events: All the accumulated accepted fill events (order from start -> finish) during execution.
        rejected_fill_events: All the accumulated rejected fill events (order from start -> finish) during execution.
        order_events: All the accumulated order events (order from start -> finish) during execution.
        market_data_events: All the accumulated market data (order from start -> finish) during execution.
        initial_portfolio_snapshot_event: The first portfolio snapshot event before any trading.
        portfolio_snapshot_events: All the accumulated portfolio snapshots (order from start -> finish) during execution.
    """
    accepted_fill_events: tuple[AcceptedFillEvent, ...]
    rejected_fill_events: tuple[RejectedFillEvent, ...]
    order_events: tuple[OrderEvent, ...]
    market_data_events: tuple[MarketDataEvent, ...]
    initial_portfolio_snapshot_event: PortfolioSnapshotEvent
    portfolio_snapshot_events: tuple[PortfolioSnapshotEvent, ...]
