from __future__ import annotations

import logging

from analyzer import generate_report

from research.utils.research_runner import ResearchRunner, RunConfig
from research.strategy_research.raw.ema_double_crossover.ema_double_crossover import EMADoubleCrossover


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_ema_double_crossover(
    ticker: str, 
    save_file: str,
    start: str = "2000-01-01", 
    end: str = "2026-01-01", 
    interval: str = "1d"
):
    """
    Runs a full iteration of ema double crossover, backtesting & graphing based on a parameter space.
    """
    config = RunConfig(
        ticker=ticker,
        start_date=start,
        end_date=end,
        interval=interval,
        strategy_factory=EMADoubleCrossover,
        param_space={
            "fast_ema_days": [3, 5, 7, 10],
            "slow_ema_days": [15, 20, 25, 30],
            "allocation": [0.25, 0.5, 0.75],
        }
    )
    results = ResearchRunner.run(config)
    generate_report(results, save_file)


if __name__ == "__main__":
    run_ema_double_crossover("AAPL", "graphs/tests/ema_double_crossover_plot.py")
