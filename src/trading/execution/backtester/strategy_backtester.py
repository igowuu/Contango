# trading/execution/backtester/strategy_backtester.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.execution.engine.strategy.strategy import Strategy
from trading.execution.engine.strategy.strategy_injector import StrategyInjector

from trading.execution.engine.events.events import (
    AcceptedFillEvent, 
    RejectedFillEvent, 
    OrderEvent, 
    StoplossOrderEvent,
    MarketDataEvent, 
    PortfolioSnapshotEvent
)
from trading.execution.engine.events.event_bus import EventBus

from trading.execution.engine.orders.order_api import OrderAPI
from trading.execution.backtester.orders.order_filler import OrderFiller
from trading.execution.backtester.orders.stoploss_order_manager import StoplossOrderManager

from trading.execution.backtester.portfolio.portfolio import Portfolio
from trading.execution.backtester.market.feed import MarketDataFeed
from trading.execution.backtester.config import BacktesterConfig

from trading.execution.engine.results.results_collector import ResultsCollector
from trading.execution.engine.results.execution_data import ExecutionData


class StrategyBacktester:
    """
    Backtester that coordinates a Strategy object over OHLCV data at a high level.  
    Allows for iteration of data with historical data rather than a live feed.  
    Subscribes all handlers to an `EventBus`, calls lifecycle methods for the provided `Strategy`,
    injects data into the `Strategy`, and returns a `ExecutionData` object for analysis.
    """
    def __init__(
        self, 
        feed: MarketDataFeed, 
        order_api: OrderAPI,
        order_filler: OrderFiller,
        stoploss_order_manager: StoplossOrderManager,
        portfolio: Portfolio,
        strategy: Strategy,
        strategy_injector: StrategyInjector,
        results_collector: ResultsCollector,
        event_bus: EventBus
    ) -> None:
        """
        Initializes `StrategyBacktester` & subscribes all event methods into the event bus.

        Args:
            feed: The feed to derive `MarketDataEvent` instances from for every bar.
            order_api: Allows the user can make `OrderEvent` instances in the event bus.
            order_filler: Fills any `OrderEvent` instances and publishes them as filled events.
            stoploss_order_manager: Publishes `OrderEvent` instances and handles checking stoplosses upon market events.
            portfolio: Takes filled events, tracks positions & money. Publishes `PortfolioSnapshotEvent` instances.
            strategy: The user's strategy with lifecycle hooks to test.
            strategy_injector: Injects snapshot events into the strategy upon them being published.
            results_collector: Collects all events & computes results at the end of the backtest.
            event_bus: The tool that allows events to be published & broadcasted to multiple modules at once.
        """
        self._feed = feed
        self._strategy = strategy
        self._results_collector = results_collector

        event_bus.subscribe(MarketDataEvent, order_filler.collect_market_data, priority=4)
        event_bus.subscribe(MarketDataEvent, stoploss_order_manager.check_if_stoploss_met, priority=3)
        event_bus.subscribe(MarketDataEvent, portfolio.update_equity, priority=2)
        event_bus.subscribe(MarketDataEvent, strategy.on_market_event, priority=1)
        event_bus.subscribe(MarketDataEvent, results_collector.collect_market_data_event, priority=0)

        event_bus.subscribe(OrderEvent, strategy.on_order_event, priority=2)
        event_bus.subscribe(OrderEvent, order_filler.fill_order_event, priority=1)
        event_bus.subscribe(OrderEvent, results_collector.collect_order_event, priority=0)

        event_bus.subscribe(StoplossOrderEvent, stoploss_order_manager.collect_stoploss_order_event, priority=0)

        event_bus.subscribe(AcceptedFillEvent, strategy.on_accepted_fill_event, priority=2)
        event_bus.subscribe(AcceptedFillEvent, portfolio.apply_accepted_fill, priority=1)
        event_bus.subscribe(AcceptedFillEvent, results_collector.collect_accepted_fill_event, priority=0)

        event_bus.subscribe(RejectedFillEvent, strategy.on_rejected_fill_event, priority=1)
        event_bus.subscribe(RejectedFillEvent, results_collector.collect_rejected_fill_event, priority=0)

        event_bus.subscribe(PortfolioSnapshotEvent, order_filler.collect_portfolio_snapshot, priority=3)
        event_bus.subscribe(PortfolioSnapshotEvent, stoploss_order_manager.collect_portfolio_snapshot, priority=2)
        event_bus.subscribe(PortfolioSnapshotEvent, strategy_injector.inject_portfolio_event, priority=1)
        event_bus.subscribe(PortfolioSnapshotEvent, results_collector.collect_portfolio_snapshot_event, priority=0)

        initial_market_event = feed.get_initial_event()
        self._initial_portfolio_snapshot_event = portfolio.get_initial_snapshot(initial_market_event)

        # Inject the initial state of the fields in slots.
        strategy.portfolio_snapshot = self._initial_portfolio_snapshot_event
        strategy.order_api = order_api

    def _run(self) -> ExecutionData:
        """
        Runs the Backtester, looping through each OHLCV data point and calling
        the lifecycle methods of the Strategy.

        Returns:
            ExecutionData: A data object that holds all events from the backtest.
        """
        self._strategy.on_start()
        self._feed.run()
        self._strategy.on_end()

        return ExecutionData(
            accepted_fill_events=tuple(self._results_collector.accepted_fill_events),
            rejected_fill_events=tuple(self._results_collector.rejected_fill_events),
            order_events=tuple(self._results_collector.order_events),
            market_data_events=tuple(self._results_collector.market_data_events),
            initial_portfolio_snapshot_event=self._initial_portfolio_snapshot_event,
            portfolio_snapshot_events=tuple(self._results_collector.portfolio_snapshot_events)
        )

    @classmethod
    def backtest(
        cls,
        ohlcv_data: list[MarketDataEvent],
        strategy: Strategy,
        config: BacktesterConfig
    ) -> ExecutionData:
        """
        Runs a full backtest for a single ticker & returns the data generated from the backtest.
        The provided data is validated for every backtest, & will raise if in the incorrect format.
        
        Args:
            ohlcv_data: The bar data for the backtest.
            strategy: The strategy subclass for the backtest (determining when to trade).
            config: The configuration for the backtest.
        
        Raises:
            ValueError: If schema is invalid or data types cannot be derived from the provided dataframe.
        """
        bus = EventBus()
        backtester = StrategyBacktester(
            feed=MarketDataFeed(ohlcv_data, bus),
            order_api=OrderAPI(bus),
            order_filler=OrderFiller(config, bus),
            stoploss_order_manager=StoplossOrderManager(bus),
            portfolio=Portfolio(bus, config, config.initial_cash, config.initial_position),
            strategy=strategy,
            strategy_injector=StrategyInjector(strategy),
            results_collector=ResultsCollector(),
            event_bus=bus
        )
        return backtester._run()
