# trading/execution/backtester/config.py — part of Contango, a parameterized backtesting & execution framework
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

from enum import Enum, auto
from typing import NamedTuple


USD = float
percent = float
units = int


class FillBehavior(Enum):
    """
    Defines when simulated orders are considered filled.

    Attributes:
        INSTANT: Orders will be filled instantly when made for the current bars close.
    """
    INSTANT = auto()


class BacktesterConfig(NamedTuple):
    """
    Holds the simulation settings for the backtester.

    Attributes:
        initial_cash: Starting account equity in USD.
        initial_position: Starting position (amount of units).
        fill: Execution timing behavior for simulated fills.
        slippage: The percent difference beteween the expected price & filled price.
        commission_per_unit: The price taxed per unit bought.
    """
    initial_cash: USD
    initial_position: units
    fill: FillBehavior
    slippage: percent = 0.0
    commission_per_unit: USD = 0.0
