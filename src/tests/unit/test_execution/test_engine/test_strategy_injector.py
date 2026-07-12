from __future__ import annotations

from execution.engine.events.events import MarketDataEvent, PortfolioSnapshotEvent
from execution.engine.strategy.strategy import Strategy
from execution.engine.strategy.strategy_injector import StrategyInjector


class DummyStrategy(Strategy):
	def on_market_event(self, event: MarketDataEvent) -> None:
		pass


def test_strategy_injector_sets_portfolio_snapshot_on_strategy() -> None:
	strategy = DummyStrategy()
	injector = StrategyInjector(strategy)
	event = PortfolioSnapshotEvent(1, 1000.0, 10, 1500.0)

	injector.inject_portfolio_event(event)

	assert strategy.portfolio_snapshot == event
