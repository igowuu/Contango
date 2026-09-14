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
