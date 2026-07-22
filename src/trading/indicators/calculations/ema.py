# trading/indicators/calculations/ema.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.indicators.indicator import Indicator


USD = float
days = int


class EMA(Indicator[float]):
    """
    Exponential Moving Average.

    Uses alpha = 2 / (period + 1) and seeds the first value
    directly from the first price to avoid bias (towards 0).
    """
    def __init__(self, period: days) -> None:
        """
        Initializes `Ema`.

        Args:
            period: Lookback period to derive the smoothing factor. Larger values -> slower to react to price changes.
        """
        self._alpha = 2 / (period + 1)
        self._value: float | None = None
        self._period = period

    def update(self, price: USD) -> float:
        """
        Takes in a new price and returns the current EMA.

        Args:
            price: The price for the current bar.
        
        Returns:
            The current EMA. The first call returns `price` unsmoothed.
        """
        if self._value is None:
            self._value = price
        else:
            self._value = price * self._alpha + self._value * (1 - self._alpha)
        return self._value
