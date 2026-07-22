# trading/indicators/calculations/wilder_average.py — part of Contango, a parameterized backtesting & execution framework
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


class WilderAverage(Indicator[float | None]):
    """
    Wilder's Moving Average (RMA).
    """
    def __init__(self, period: days) -> None:
        """
        Initializes `WilderAverage`.
        
        Args:
            period: Lookback period to derive the smoothing factor. Larger values -> slower to react to price changes.
        """
        self._period = period
        self._window: deque[float] = deque(maxlen=period)

        self._value: float | None = None

    def update(self, price: USD) -> float | None:
        """
        Takes in a new value and return smoothed result.

        Args:
            price: The price for the current bar.
        
        Returns:
            The current WilderAverage. Returns None if period amount of days have not been reached.
        """
        self._window.append(price)

        if len(self._window) < self._period:
            return None

        # First full initialization: simple average
        if self._value is None:
            self._value = sum(self._window) / self._period
            return self._value

        self._value = (
            (self._value * (self._period - 1)) + price
        ) / self._period

        return self._value
