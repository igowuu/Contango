# trading/indicators/state/bollinger_bands_state.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.indicators.calculations.bollinger_bands import BollingerBandSnapshot


class BollingerState(Enum):
    """
    Current price location relative to Bollinger Bands.

    Attributes:
        BELOW_LOWER: The price is below the lower bollinger band.
        BETWEEN_LOWER_AND_MIDDLE: The price is between the lower & middle bollinger bands.
        BETWEEN_MIDDLE_AND_HIGHER: The price is above the middle bollinger band but below the higher one.
        ABOVE_HIGHER: The price is above the higher bollinger band.
    """
    BELOW_LOWER = auto()
    BETWEEN_LOWER_AND_MIDDLE = auto()
    BETWEEN_MIDDLE_AND_HIGHER = auto()
    ABOVE_HIGHER = auto()


    @classmethod
    def get_state(cls, current_price: float, bands: BollingerBandSnapshot) -> BollingerState:
        """
        Returns the band zone that the price is currently in.

        Args:
            current_price: The price for the current bar.
            bands: The snapshot of bollinger bands for the current bar.
        
        Returns:
            BollingerState: The state enum of the price relative to the bollinger bands.
        """
        if current_price < bands.lower:
            return BollingerState.BELOW_LOWER
        if current_price < bands.middle:
            return BollingerState.BETWEEN_LOWER_AND_MIDDLE
        if current_price > bands.middle:
            return BollingerState.BETWEEN_MIDDLE_AND_HIGHER
        return BollingerState.ABOVE_HIGHER
