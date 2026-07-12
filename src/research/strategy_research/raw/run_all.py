from __future__ import annotations

from pathlib import Path

from research.strategy_research.raw.bollinger_mean_reversion.runner import run_bollinger_mean_reversion
from research.strategy_research.raw.buy_and_hold.runner import run_buy_and_hold
from research.strategy_research.raw.ema_double_crossover.runner import run_ema_double_crossover
from research.strategy_research.raw.rsi_mean_reversion.runner import run_rsi_mean_reversion
from research.strategy_research.raw.sma_double_crossover.runner import run_sma_double_crossover
from research.strategy_research.raw.wilder_average_crossover.runner import run_wilder_average_crossover
from research.strategy_research.raw.vwap_mean_reversion.runner import run_vwap_mean_reversion


def run_all_raw() -> None:
    """
    Runs all `raw` strategies with the same unified data.
    """
    ticker = "AAPL"
    start = "2000-01-01"
    end = "2026-01-01"
    interval = "1d"
    save_folder = "graphs/1d_raw/"

    folder_as_path = Path(save_folder)
    folder_as_path.mkdir(parents=True, exist_ok=True)

    run_buy_and_hold(ticker, save_folder + "buy_and_hold_plot.html", start, end, interval)
    run_sma_double_crossover(ticker, save_folder + "sma_double_crossover_plot.html", start, end, interval)
    run_ema_double_crossover(ticker, save_folder + "ema_double_crossover_plot.html", start, end, interval)
    run_wilder_average_crossover(ticker, save_folder + "wilder_average_crossover_plot.html", start, end, interval)
    run_rsi_mean_reversion(ticker, save_folder + "rsi_mean_reversion_plot.html", start, end, interval)
    run_bollinger_mean_reversion(ticker, save_folder + "bollinger_mean_reversion_plot.html", start, end, interval)
    run_vwap_mean_reversion(ticker, save_folder + "vwap_mean_reversion_plot.html", start, end, interval)


if __name__ == '__main__':
    run_all_raw()
