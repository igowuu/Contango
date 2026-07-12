from __future__ import annotations

import logging

from analyzer import generate_report

from research.utils.research_runner import ResearchRunner, RunConfig
from research.strategy_research.raw.vwap_mean_reversion.vwap_mean_reversion import VWAPMeanReversion


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_vwap_mean_reversion(
    ticker: str, 
    save_file: str,
    start: str = "2000-01-01", 
    end: str = "2026-01-01", 
    interval: str = "1d"
):
    """
    Runs a full iteration of VWAP mean reversion, backtesting & graphing based on a parameter space.
    """
    config = RunConfig(
        ticker=ticker,
        start_date=start,
        end_date=end,
        interval=interval,
        strategy_factory=VWAPMeanReversion,
        param_space={
            "k": [round(x * 0.01, 1) for x in range(1, 500)],
            "allocation": [0.75],
        }
    )
    results = ResearchRunner.run(config)
    generate_report(results, save_file)


if __name__ == "__main__":
    run_vwap_mean_reversion("AAPL", "graphs/tests/vwap_mean_reversion_plot.html")
