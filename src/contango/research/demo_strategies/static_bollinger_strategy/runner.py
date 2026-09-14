from __future__ import annotations

from datetime import datetime

from contango.market.calendar import NYSECalendar
from contango.market.data_providers import Interval
from contango.market.data_providers.yfinance import Yfinance, YfinanceConfig

from contango.trading.execution.backtest import FillBehavior, BacktesterConfig

from contango.research.demo_strategies.static_bollinger_strategy.strategy import BollingerBandMeanReversion
from contango.runners.static import StaticRunner


def run() -> None:
    # Fetch OHCLV data & store it into the database.
    data = StaticRunner[YfinanceConfig].fetch_data(
        provider=Yfinance(NYSECalendar()), 
        config=YfinanceConfig(
            ticker="AAPL", 
            interval=Interval.DAY_1,
            start_timestamp=int(datetime(2000, 1, 1).timestamp() * 1000),
            end_timestamp=int(datetime(2026, 1, 1).timestamp() * 1000)
        )
    )
    # Compute the metrics from the OHCLV data
    metrics = StaticRunner.run(
        ohlcv_data=data,
        strategy=BollingerBandMeanReversion(
            bollinger_bands_period=20,
            bollinger_bands_stdev=2.0,
            allocation=0.5,
            symbol="AAPL"
        ),
        backtester_config=BacktesterConfig(
            initial_cash=1000,
            initial_position=0,
            fill=FillBehavior.INSTANT,
            slippage=0.0,
            commission_per_unit=0.0
        )
    )
    # The reason this was not graphed instead was because one static strategy point is not
    # statistically meaningful to compare amongst only itself.
    # This just prints the metrics to the terminal.
    print(metrics)


if __name__ == '__main__':
    run()
