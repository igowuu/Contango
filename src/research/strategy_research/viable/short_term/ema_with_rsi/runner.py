from __future__ import annotations

import logging

from analyzer.data.analyze_and_graph import generate_report

from research.utils.research_runner import ResearchRunner, RunConfig
from research.strategy_research.viable.short_term.ema_with_rsi.ema_with_rsi import EMAWithRSI


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_ema_with_rsi(
    ticker: str, 
    save_file: str,
    start: str = "2026-05-13", 
    end: str = "2026-07-11", 
    interval: str = "5m"
) -> None:
    """
    Runs a full iteration of the EMA with RSI strategy.
    """
    config = RunConfig(
        ticker=ticker,
        start_date=start,
        end_date=end,
        interval=interval,
        strategy_factory=EMAWithRSI,
        param_space={
            "fast_ema_period": list(range(20, 61, 20)),
            "slow_ema_period": list(range(100, 260, 20)),
            "rsi_period": list(range(2, 9, 2)),
            "lower_rsi_threshold": list(range(10, 41, 10)),
            "upper_rsi_threshold": list(range(65, 96, 10)),
            "allocation": [0.75],
        }
    )
    results = ResearchRunner.run(config)
    generate_report(results, save_file)


if __name__ == '__main__':
    run_ema_with_rsi("AAPL", "graphs/tests/ema_with_rsi_plot.html")
