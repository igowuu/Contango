from __future__ import annotations


from execution.backtester.config import BacktesterConfig, FillBehavior
from execution.backtester.strategy_backtester import StrategyBacktester
from execution.engine.events.events import MarketDataEvent
from execution.engine.strategy.strategy import Strategy


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