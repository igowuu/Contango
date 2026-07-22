# trading/execution/engine/results/execution_data.py — part of Contango, a parameterized backtesting & execution framework
# Copyright (C) 2026  Jacob Taylor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

from typing import NamedTuple

from trading.execution.engine.events.events import (
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
