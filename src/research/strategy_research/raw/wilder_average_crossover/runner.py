from __future__ import annotations

import logging

from analyzer import generate_report

from research.utils.research_runner import ResearchRunner, RunConfig
from research.strategy_research.raw.wilder_average_crossover.wilder_average_crossover import WilderAverageCrossover


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_wilder_average_crossover(
    ticker: str, 
    save_file: str,
    start: str = "2000-01-01", 
    end: str = "2026-01-01", 
    interval: str = "1d"
):
    """
    Runs a full iteration of wilder average crossover, backtesting & graphing based on a parameter space.
    """
    config = RunConfig(
        ticker=ticker,
        start_date=start,
        end_date=end,
        interval=interval,
        strategy_factory=WilderAverageCrossover,
        param_space={
            "fast_wilder_days": list(range(5, 51, 5)),
            "slow_wilder_days": list(range(20, 251, 10)),
            "allocation": [0.1],
        }
    )
    results = ResearchRunner.run(config)
    generate_report(results, save_file)


if __name__ == "__main__":
    run_wilder_average_crossover("AAPL", "graphs/tests/wilder_average_crossover.html")
