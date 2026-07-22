# trading/indicators/calculations/average_true_range.py — part of Contango, a parameterized backtesting & execution framework
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
from trading.indicators.calculations.true_range import TrueRange
from trading.indicators.calculations.wilder_average import WilderAverage


USD = float
days = int


class AverageTrueRange(Indicator[float | None]):
    """
    The average true range (volatility measure).
    """
    def __init__(self, period: days = 14) -> None:
        """
        Initializes `AverageTrueRange`.

        Args:
            period: Lookback period used to smooth the True Range.
        """
        self._true_range = TrueRange()
        self._average = WilderAverage(period)

    def update(self, high: USD, low: USD, close: USD) -> float | None:
        """
        Updates the ATR for each bar.

        Args:
            high: The highest price reached in USD for a bar.
            low: The lowest price reached in USD for a bar.
            close: The closing price in USD for a bar.

        Returns:
            The current ATR. Returns None until enough bars have been
            observed to initialize the Wilder average.
        """
        tr = self._true_range.update(high, low, close)
        return self._average.update(tr)
