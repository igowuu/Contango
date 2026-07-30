# tests/unit/trading/test_execution/test_backtester/test_strategy_backtester.py — part of Contango, a parameterized backtesting & execution framework
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


from contango.trading.execution.backtester.config import BacktesterConfig, FillBehavior
from contango.trading.execution.backtester.strategy_backtester import StrategyBacktester
from contango.trading.execution.engine.events.events import MarketDataEvent
from contango.trading.execution.engine.strategy.strategy import Strategy


def _create_dataframe() -> list[MarketDataEvent]:
    data = [
        MarketDataEvent(1000, "AAPL", 100.0, 101.0, 99.0, 100.0, 1000),
        MarketDataEvent(2000, "AAPL", 101.0, 102.0, 100.0, 101.0, 1000)
    ]

    return data


class BuyOnceStrategy(Strategy):
    def __init__(self) -> None:
        self.started = False
        self.ended = False
        self.market_events: list[MarketDataEvent] = []

    def on_start(self) -> None:
        self.started = True

    def on_market_event(self, event: MarketDataEvent) -> None:
        self.market_events.append(event)

        if len(self.market_events) == 1:
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=1,
                reason="buy once",
            )

    def on_end(self) -> None:
        self.ended = True


def test_backtest_runs_and_collects_expected_events() -> None:
    strategy = BuyOnceStrategy()
    data = StrategyBacktester.backtest(
        ohlcv_data=_create_dataframe(),
        strategy=strategy,
        config=BacktesterConfig(
            initial_cash=1000.0,
            initial_position=0,
            fill=FillBehavior.INSTANT,
            slippage=0.0,
            commission_per_unit=0.0,
        ),
    )

    assert strategy.started is True
    assert strategy.ended is True
    assert len(data.market_data_events) == 2
    assert len(data.order_events) == 1
    assert len(data.accepted_fill_events) == 1
    assert len(data.portfolio_snapshot_events) == 3
    assert strategy.portfolio_snapshot.timestamp == 2000
    assert strategy.portfolio_snapshot.position == 1