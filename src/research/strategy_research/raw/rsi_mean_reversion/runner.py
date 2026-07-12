from __future__ import annotations

import logging

from analyzer import generate_report

from research.utils.research_runner import ResearchRunner, RunConfig
from research.strategy_research.raw.rsi_mean_reversion.rsi_mean_reversion import RSIMeanReversion


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_rsi_mean_reversion(
    ticker: str, 
    save_file: str,
    start: str = "2000-01-01", 
    end: str = "2026-01-01", 
    interval: str = "1d"
):
    """
    Runs a full iteration of rsi mean reversion, backtesting & graphing based on a parameter space.
    """
    config = RunConfig(
        ticker=ticker,
        start_date=start,
        end_date=end,
        interval=interval,
        strategy_factory=RSIMeanReversion,
        param_space={
            "period":  [14],
            "upper_threshold": list(range(60, 81)),
            "lower_threshold": list(range(20, 41)),
            "allocation": [0.1],
        }
    )
    results = ResearchRunner.run(config)
    generate_report(results, save_file)


if __name__ == "__main__":
    run_rsi_mean_reversion("AAPL", "graphs/tests/rsi_mean_reversion_plot.html")
