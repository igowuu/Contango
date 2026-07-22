# trading/indicators/calculations/sma.py — part of Contango, a parameterized backtesting & execution framework
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

from collections import deque

from trading.indicators.indicator import Indicator


USD = float
days = int


class SMA(Indicator[float | None]):
    """
    Simple Moving Average.

    Maintains a window of prices and tracks their sum incrementally.
    Returns None until the window is full.
    """
    def __init__(self, period: days) -> None:
        """
        Initializes `SMA`.

        Args:
            period: The number of days (period) for the rolling window.
        """
        self._period = period
        self._window: deque[float] = deque(maxlen=period)
        self._sum = 0.0

    def update(self, price: USD) -> float | None:
        """
        Takes in a new price and returns the current SMA, or None if the window is not yet full.

        Args:
            price: The price for the current bar.
        
        Returns:
            The SMA over the current window, or `None` if `period` amount of days have not passed.
        """
        if len(self._window) == self._period:
            self._sum -= self._window[0]

        self._window.append(price)
        self._sum += price

        if len(self._window) < self._period:
            return None

        return self._sum / self._period
