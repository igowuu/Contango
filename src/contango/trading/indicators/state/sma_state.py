# trading/indicators/state/sma_state.py — part of Contango, a parameterized backtesting & execution framework
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


class SMAState(Enum):
    """
    The position of the fast SMA relative to a slow SMA.

    Attributes:
        BELOW: The fast SMA below the slow SMA.
        ABOVE: The fast SMA is above the slow SMA.
    """
    BELOW = auto()
    ABOVE = auto()


    @classmethod
    def get_state(cls, fast_sma: float, slow_sma: float) -> SMAState:
        """
        Returns the SMA state of the fast SMA relative to the slow SMA.

        Args:
            fast_sma: The value of the fast SMA for the current bar.
            slow_sma: The value of the slow SMA for the current bar.
        
        Returns:
            SMAState: Whether the fast SMA is above or below the slow SMA.
        """
        if fast_sma > slow_sma:
            return SMAState.ABOVE
        else:
            return SMAState.BELOW
