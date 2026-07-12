from __future__ import annotations

import logging

from analyzer import generate_report

from research.utils.research_runner import ResearchRunner, RunConfig
from research.strategy_research.raw.sma_double_crossover.sma_double_crossover import SMADoubleCrossover


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_sma_double_crossover(
    ticker: str, 
    save_file: str,
    start: str = "2000-01-01", 
    end: str = "2026-01-01", 
    interval: str = "1d"
):
    """
    Runs a full iteration of sma double crossover, backtesting & graphing based on a parameter space.
    """
    config = RunConfig(
        ticker=ticker,
        start_date=start,
        end_date=end,
        interval=interval,
        strategy_factory=SMADoubleCrossover,
        param_space={
            "fast_sma_days": list(range(5, 51, 5)),
            "slow_sma_days": list(range(20, 251, 10)),
            "allocation": [0.1],
        }
    )
    results = ResearchRunner.run(config)
    generate_report(results, save_file)


if __name__ == "__main__":
    run_sma_double_crossover("AAPL", "graphs/tests/sma_double_crossover_plot.html")
