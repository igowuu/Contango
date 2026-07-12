from __future__ import annotations

import logging

from analyzer import generate_report

from research.utils.research_runner import ResearchRunner, RunConfig
from research.strategy_research.raw.buy_and_hold.buy_and_hold import BuyAndHold


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_buy_and_hold(
    ticker: str, 
    save_file: str,
    start: str = "2000-01-01", 
    end: str = "2026-01-01", 
    interval: str = "1d"
) -> None:
    """
    Runs a full iteration of buy & hold, backtesting & graphing based on a parameter space.
    """
    config = RunConfig(
        ticker=ticker,
        start_date=start,
        end_date=end,
        interval=interval,
        strategy_factory=BuyAndHold,
        param_space={
            "allocation": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        }
    )
    results = ResearchRunner.run(config)
    generate_report(results, save_file)


if __name__ == "__main__":
    run_buy_and_hold("AAPL", "graphs/tests/buy_and_hold_plot.html")
