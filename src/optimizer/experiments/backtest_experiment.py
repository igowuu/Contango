from __future__ import annotations

from typing import NamedTuple, Callable, Any

from execution.engine.strategy import Strategy
from execution.engine.events import MarketDataEvent
from execution.backtester.config import BacktesterConfig


class BacktestExperiment(NamedTuple):
    """
    A reusable strategy that allows it to be used with configurable parameters.
    
    Attributes:
        strategy_factory: A callable that returns a `Strategy` instance.
        parameters: The parameters for the method, mapping the parameter name to the desired value.
        dataset: The OHLCV data to use for the experiment.
        config: The backtest configuration to use for the experiment.
    """
    strategy_factory: Callable[..., Strategy]
    parameters: dict[str, Any]
    dataset: list[MarketDataEvent]
    config: BacktesterConfig