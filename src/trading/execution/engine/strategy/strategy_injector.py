# trading/execution/engine/strategy/strategy_injector.py — part of Contango, a parameterized backtesting & execution framework
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

# SPDX-FileCopyrightText: 2026 Jacob Taylor
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

from trading.execution.engine.events.events import PortfolioSnapshotEvent
from trading.execution.engine.strategy.strategy import Strategy


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
