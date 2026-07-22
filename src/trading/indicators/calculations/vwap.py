# trading/indicators/calculations/vwap.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.indicators.indicator import Indicator


USD = float


class VWAPSnapshot(NamedTuple):
    """
    A single snapshot of VWAP with bands.

    Attributes:
        vwap: The current volume-weighted average price.
        upper: VWAP + k standard deviations.
        lower: VWAP - k standard deviations.
    """
    vwap: float
    upper: float
    lower: float


class VWAP(Indicator[VWAPSnapshot | None]):
    """
    VWAP with standard deviation bands.

    Resets at the start of each new trading session.
    Returns None on the first bar of each session (no deviation yet).
    """
    def __init__(self, k: float = 1.25) -> None:
        """
        Args:
            k: Band-width multiplier in standard deviations.
        """
        self._k = k

        # Intraday accumulators — reset each session
        self._cumulative_tp_volume: float = 0.0
        self._cumulative_volume: float = 0.0
        self._cumulative_tp_sq_volume: float = 0.0
        self._bar_count: int = 0

    def update(
        self,
        high: USD,
        low: USD,
        close: USD,
        volume: float
    ) -> VWAPSnapshot | None:
        """
        Takes in a new bar and returns the current VWAP snapshot.
        Returns None on the first bar of the session (standard deviation undefined).

        Args:
            high: Bar high price.
            low: Bar low price.
            close: Bar close price.
            volume: Bar volume.
        """
        typical_price = (high + low + close) / 3

        self._cumulative_tp_volume += typical_price * volume
        self._cumulative_volume += volume
        self._cumulative_tp_sq_volume += (typical_price ** 2) * volume
        self._bar_count += 1

        if self._cumulative_volume == 0:
            return None

        vwap = self._cumulative_tp_volume / self._cumulative_volume

        # Volume-weighted variance
        variance = (
            self._cumulative_tp_sq_volume / self._cumulative_volume
        ) - vwap ** 2

        # Variance can be slightly negative due to floating point
        std = max(variance, 0.0) ** 0.5

        if self._bar_count < 2:
            return None

        band = self._k * std

        return VWAPSnapshot(
            vwap=vwap,
            upper=vwap + band,
            lower=vwap - band,
        )
