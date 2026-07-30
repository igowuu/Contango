# research/research_strategies/bollinger_band_mean_reversion/runner.py — part of Contango, a parameterized backtesting & execution framework
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

from datetime import datetime

from contango.broker.calendar.nyse_calendar import NYSECalendar
from contango.broker.historical_brokers.config_type import Interval
from contango.broker.historical_brokers.yfinance import Yfinance, YfinanceConfig

from contango.trading.execution.backtester import FillBehavior

from contango.research.research_runner import ResearchRunner, RunConfig
from contango.research.research_strategies.bollinger_band_mean_reversion.strategy import BollingerBandMeanReversion

from contango.trading.analyzer.data import generate_report


def build_config() -> RunConfig[YfinanceConfig]:
    """
    Builds the backtest configuration for a Bollinger Band mean-reversion
    parameter sweep on AAPL daily bars, 2000-2026.
    """
    ticker = "AAPL"
    interval = Interval.DAY_1
    start = datetime(2000, 1, 1)
    end = datetime(2026, 1, 1)

    initial_cash = 1_000
    initial_position = 0
    fill_behavior = FillBehavior.INSTANT  # fills orders immediately at the bar's price, no partial fills
    slippage = 0.001                      # 0.1% price slippage applied per fill, to simulate imperfect execution
    commission_per_unit = 0.0             # fee per share bought

    start_unix_ms = int(start.timestamp() * 1000)
    end_unix_ms = int(end.timestamp() * 1000)

    # ResearchRunner will grid-search every combination of these values,
    # instantiating BollingerBandMeanReversion(**params) for each one and
    # running a full backtest per combination. Total runs = product of list
    # lengths below (11 * 5 * 4 * 1 = 220 backtests in this case).
    param_space: dict[str, list[int | float | str]] = {
        # Lookback window (in bars) used to compute the Bollinger Band's
        # moving average and standard deviation. Swept from 5 to 25 in
        # steps of 2 -> [5, 7, 9, ..., 25].
        "bollinger_bands_period": list(range(5, 26, 2)),

        # Band width, in standard deviations, above/below the moving
        # average. Smaller values -> tighter bands -> more frequent,
        # lower-conviction signals. Larger values -> wider bands -> rarer signals.
        "bollinger_bands_stdev": [0.5, 1.0, 1.5, 2.0, 2.5],

        # Fraction of available cash committed to each buy signal.
        # 1.0 means trade 100% of cash on every entry; lower values leave cash
        # in portfolio (less risky, as shown when graphing).
        "allocation": [0.25, 0.5, 0.75, 1.0],

        # Held fixed at a single value here since this run only trades
        # one ticker, but keeping it in param_space keeps the strategy
        # constructor signature uniform for the grid search.
        "symbol": [ticker],
    }

    return RunConfig[YfinanceConfig](
        broker=Yfinance(NYSECalendar()),
        broker_config=YfinanceConfig(ticker, interval, start_unix_ms, end_unix_ms),
        strategy_factory=BollingerBandMeanReversion,
        param_space=param_space,
        initial_cash=initial_cash,
        initial_position=initial_position,
        fill_behavior=fill_behavior,
        slippage=slippage,
        commission_per_unit=commission_per_unit,
    )


if __name__ == "__main__":
    config = build_config()
    results = ResearchRunner.run(config, verbose_iterating=True)

    graph_dir = "research/research_strategies/bollinger_band_mean_reversion/graphs/"
    generate_report(results, graph_dir, rank_metric="calmar_ratio")
