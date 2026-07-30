# trading/indicators/calculations/bollinger_bands.py — part of Contango, a parameterized backtesting & execution framework
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

from typing import NamedTuple

from contango.trading.indicators.indicator import Indicator
from contango.trading.indicators.calculations.sma import SMA


USD = float
days = int


class BollingerBandSnapshot(NamedTuple):
    """
    A single snapshot of Bollinger Bands.

    Attributes:
        upper: The upper band for the current price.
        middle: The middle band (pure SMA) for the current price.
        lower: The lower band for the current price.
        stdev: The population standard deviation over the lookback window.
    """
    upper: float
    middle: float
    lower: float
    stdev: float


class BollingerBands(Indicator[BollingerBandSnapshot | None]):
    """
    Rolling Bollinger Bands with variance updates.

    Wraps an SMA and tracks a running sum-of-squares so that
    standard deviation is recomputed in constant time on every tick.
    Returns None until the lookback window is full.
    """
    def __init__(self, period: days = 20, k: float = 2.0) -> None:
        """
        Args:
            period: Lookback window in bars (default 20).
            k: Band-width multiplier in standard deviations (default 2.0).
        """
        self._period = period
        self._k = k
        self._sma = SMA(period)

        self._sum: float = 0.0
        self._sum_sq: float = 0.0
        self._count: int = 0

        self._window: list[float] = [0.0] * period
        self._head: int = 0

    def update(self, price: USD) -> BollingerBandSnapshot | None:
        """
        Takes in a new price and return the current bands, or None while the
        window is still filling.

        Args:
            price: The price for the current bar.

        Returns:
            A BollingerBandSnapshot(upper, middle, lower), or None until
            `period` prices have been seen.
        """
        middle = self._sma.update(price)

        if self._count == self._period:
            oldest = self._window[self._head]
            self._sum -= oldest
            self._sum_sq -= oldest * oldest

        self._window[self._head] = price
        self._head = (self._head + 1) % self._period
        self._count = min(self._count + 1, self._period)

        self._sum += price
        self._sum_sq += price * price

        if middle is None:
            return None

        n = self._period
        variance = (self._sum_sq - self._sum * self._sum / n) / n
        stdev = variance ** 0.5
        band = self._k * stdev

        return BollingerBandSnapshot(
            upper=middle + band,
            middle=middle,
            lower=middle - band,
            stdev=stdev,
        )
