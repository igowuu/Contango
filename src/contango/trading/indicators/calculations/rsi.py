# trading/indicators/calculations/rsi.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.indicators.indicator import Indicator
from contango.trading.indicators.calculations.wilder_average import WilderAverage


USD = float
days = int


class RSI(Indicator[float | None]):
    """
    Relative Strength Index (RSI).

    Uses Wilder's Moving Average to smooth average gains and losses
    over the given period. Returns None until both averages are seeded.
    """
    def __init__(self, period: days = 14) -> None:
        """
        Initializes `RSI`.

        Args:
            period: Lookback period for the Wilder averages.
        """
        self._period = period
        self._avg_gain = WilderAverage(period)
        self._avg_loss = WilderAverage(period)
        self._prev_price: float | None = None

    def update(self, price: USD) -> float | None:
        """
        Takes in a new price and returns the current RSI.

        Args:
            price: The price for the current bar.

        Returns:
            RSI in the range [0, 100], or None if the period has not been reached.
        """
        if self._prev_price is None:
            self._prev_price = price
            return None

        delta = price - self._prev_price
        self._prev_price = price

        gain = max(delta, 0.0)
        loss = max(-delta, 0.0)

        avg_gain = self._avg_gain.update(gain)
        avg_loss = self._avg_loss.update(loss)

        if avg_gain is None or avg_loss is None:
            return None

        if avg_loss == 0.0:
            return 100.0

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
