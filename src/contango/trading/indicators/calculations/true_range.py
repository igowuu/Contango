# trading/indicators/calculations/true_range.py — part of Contango, a parameterized backtesting & execution framework
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


USD = float


class TrueRange(Indicator[float]):
    """
    The volatility during a single trading period.
    """
    def __init__(self) -> None:
        """
        Initializes `TrueRange`.
        """
        self._previous_close: USD | None = None

    def update(self, high: USD, low: USD, close: USD) -> float:
        """
        Updates the state of the true range for every bar.
        
        Args:
            high: The highest price reached in USD for a bar.
            low: The lowest price reached in USD for a bar.
            close: The closing price in USD for a bar.
        
        Returns:
            float: The true range for the bar.
        """
        if self._previous_close is None:
            tr = high - low
        else:
            tr = max(
                high - low,
                abs(high - self._previous_close),
                abs(low - self._previous_close),
            )

        self._previous_close = close
        return tr