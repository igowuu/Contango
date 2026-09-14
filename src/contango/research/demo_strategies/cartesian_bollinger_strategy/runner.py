from __future__ import annotations

import logging
from datetime import datetime

from contango.market.calendar import NYSECalendar
from contango.market.data_providers import Interval
from contango.market.data_providers.yfinance import Yfinance, YfinanceConfig

from contango.trading.execution.backtest import FillBehavior, BacktesterConfig

from contango.research.demo_strategies.cartesian_bollinger_strategy.strategy import BollingerBandMeanReversion
from contango.runners.grid.grid_search_runner import GridSearchRunner

from contango.trading.analysis.data.graphing_experiment import GraphingExperiment
from contango.trading.analysis.data.graph_runner import GraphRunner


def run() -> None:
    tickers = ["AAPL", "SPY", "NVDA", "QQQ", "MSFT", "TSLA"]
    # Fetch OHCLV data & store it into the database.
    data = GridSearchRunner[YfinanceConfig].fetch_data_multi(
        provider=Yfinance(NYSECalendar()), 
        configs={
            ticker: YfinanceConfig(
                ticker=ticker,
                interval=Interval.DAY_1,
                start_timestamp=int(datetime(2000, 1, 1).timestamp() * 1000),
                end_timestamp=int(datetime(2026, 1, 1).timestamp() * 1000),
            )
            for ticker in tickers
        }
    )
    # Compute the results from the OHCLV data.
    results = GridSearchRunner.run(
        ohlcv_data=data,
        strategy_cls=BollingerBandMeanReversion,
        param_grid={
            "bollinger_bands_period": [15, 20, 25],
            "bollinger_bands_stdev": [1.0, 1.5, 2.0, 2.5],
            "allocation": [0.25, 0.5, 0.75],
            "symbol": tickers
        },
        backtester_config=BacktesterConfig(
            initial_cash=1000,
            initial_position=0,
            fill=FillBehavior.INSTANT,
            slippage=0.0,
            commission_per_unit=0.0
        )
    )
    # Graph the results.
    graphing_experiments = GraphingExperiment.from_experiment_results(results)
    graph_runner = GraphRunner()
    figures = graph_runner.build_all(graphing_experiments)
    graph_runner.write_to_html(figures, "graphs/")
    

if __name__ == '__main__':
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    run()
