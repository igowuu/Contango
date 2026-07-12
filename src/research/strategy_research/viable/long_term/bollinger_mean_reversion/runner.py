from __future__ import annotations

import logging

from analyzer import generate_report

from research.utils.research_runner import ResearchRunner, RunConfig
from research.strategy_research.raw.bollinger_mean_reversion.bollinger_mean_reversion import BollingerMeanReversion


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_bollinger_mean_reversion(
    ticker: str, 
    save_file: str,
    start: str = "2000-01-01", 
    end: str = "2026-01-01", 
    interval: str = "1d"
) -> None:
    """
    Runs a full iteration of bollinger mean reversion, backtesting & graphing based on a parameter space.
    """
    config = RunConfig(
        ticker=ticker,
        start_date=start,
        end_date=end,
        interval=interval,
        strategy_factory=BollingerMeanReversion,
        param_space={
            "period": list(range(1, 25)),
            "num_stdevs": [1.0, 1.25, 1.5, 1.75, 2.0],
            "allocation": [0.5, 0.75],
        }
    )
    results = ResearchRunner.run(config)
    generate_report(results, save_file)


if __name__ == "__main__":
    run_bollinger_mean_reversion("SPY", "graphs/tests/bollinger_mean_reversion_plot.html")
