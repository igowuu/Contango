# trading/indicators/state/wilder_average_state.py — part of Contango, a parameterized backtesting & execution framework
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


class WilderState(Enum):
    """
    Current location of the fast wilder average relative to the slow wilder average for a bar.

    Attributes:
        BELOW: The fast wilder average is below the slow wilder average.
        ABOVE: The fast wilder average is above the slow wilder average.
    """
    BELOW = auto()
    ABOVE = auto()


    @classmethod
    def get_state(cls, fast_wilder_average: float, slow_wilder_average: float) -> WilderState:
        """
        Returns the state of the fast wilder average relative to the slow wilder average (above or below).

        Args:
            fast_wilder_average: The fast wilder average value for the current bar.
            slow_wilder_average: The slow wilder average value for the current bar.

        Returns:
            WilderState: Whether the fast wilder average is below or above the slow wilder average.
        """
        if fast_wilder_average > slow_wilder_average:
            return WilderState.ABOVE
        else:
            return WilderState.BELOW
