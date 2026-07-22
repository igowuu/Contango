# trading/optimizer/experiments/backtest_experiment.py — part of Contango, a parameterized backtesting & execution framework
# Copyright (C) 2026  Jacob Taylor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

from typing import NamedTuple, Callable, Any

from trading.execution.engine.strategy import Strategy
from trading.execution.engine.events import MarketDataEvent
from trading.execution.backtester.config import BacktesterConfig


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