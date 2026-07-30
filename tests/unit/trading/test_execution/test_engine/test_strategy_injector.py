# tests/unit/trading/test_execution/test_engine/test_strategy_injector.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.execution.engine.events.events import MarketDataEvent, PortfolioSnapshotEvent
from contango.trading.execution.engine.strategy.strategy import Strategy
from contango.trading.execution.engine.strategy.strategy_injector import StrategyInjector


class DummyStrategy(Strategy):
	def on_market_event(self, event: MarketDataEvent) -> None:
		pass


def test_strategy_injector_sets_portfolio_snapshot_on_strategy() -> None:
	strategy = DummyStrategy()
	injector = StrategyInjector(strategy)
	event = PortfolioSnapshotEvent(1, 1000.0, 10, 1500.0)

	injector.inject_portfolio_event(event)

	assert strategy.portfolio_snapshot == event
