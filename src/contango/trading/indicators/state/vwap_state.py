# trading/indicators/state/vwap_state.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.indicators.calculations.vwap import VWAPSnapshot


class VWAPState(Enum):
    """
    The current price location relative to VWAP.

    Attributes:
        BELOW_LOWER: The price is below the lower band.
        BETWEEN_LOWER_AND_MIDDLE: The price is between the lower & VWAP band.
        ABOVE_MIDDLE: The price is above the VWAP band.
    """
    BELOW_LOWER = auto()
    BETWEEN_LOWER_AND_VWAP = auto()
    ABOVE_VWAP = auto()


    @classmethod
    def get_state(cls, price: float, snapshot: VWAPSnapshot) -> VWAPState:
        """
        Returns the zone of the price relative to the VWAP bands.

        Args:
            price: The close price for the current bar.
            snapshot: The VWAP snapshot for the current bar.
        
        Returns:
            VWAPState: The price relative to the VWAP snapshot.
        """
        if price < snapshot.lower:
            return VWAPState.BELOW_LOWER
        if price < snapshot.vwap:
            return VWAPState.BETWEEN_LOWER_AND_VWAP
        return VWAPState.ABOVE_VWAP
