# trading/execution/engine/results/results_collector.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.execution.engine.events.events import (
    AcceptedFillEvent, 
    RejectedFillEvent, 
    OrderEvent, 
    MarketDataEvent, 
    PortfolioSnapshotEvent
)


class ResultsCollector:
    """
    Collects all results from events & stores them for later analysis.
    """
    def __init__(self) -> None:
        """
        Initializes `ResultsCollector` with empty lists for all events.
        """
        self.accepted_fill_events: list[AcceptedFillEvent] = []
        self.rejected_fill_events: list[RejectedFillEvent] = []
        self.order_events: list[OrderEvent] = []
        self.market_data_events: list[MarketDataEvent] = []
        self.portfolio_snapshot_events: list[PortfolioSnapshotEvent] = []
    
    def collect_accepted_fill_event(self, event: AcceptedFillEvent) -> None:
        """
        Stores an `AcceptedFillEvent` in an internal list.
        """
        self.accepted_fill_events.append(event)
    
    def collect_rejected_fill_event(self, event: RejectedFillEvent) -> None:
        """
        Stores an `RejectedFillEvent` in an internal list.
        """
        self.rejected_fill_events.append(event)
    
    def collect_order_event(self, event: OrderEvent) -> None:
        """
        Stores an `OrderEvent` in an internal list.
        """
        self.order_events.append(event)

    def collect_market_data_event(self, event: MarketDataEvent) -> None:
        """
        Stores a `MarketDataEvent` in an internal list.
        """
        self.market_data_events.append(event)

    def collect_portfolio_snapshot_event(self, event: PortfolioSnapshotEvent) -> None:
        """
        Stores a `PortfolioSnapshotEvent` in an internal list.
        """
        self.portfolio_snapshot_events.append(event)
