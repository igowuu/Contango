# trading/indicators/state/ema_state.py — part of Contango, a parameterized backtesting & execution framework
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


class EMAState(Enum):
    """
    Current location of the fast EMA relative to the slow EMA for a bar.

    Attributes:
        BELOW: The fast EMA is below the slow EMA.
        ABOVE: The fast EMA is above the slow EMA.
    """
    BELOW = auto()
    ABOVE = auto()


    @classmethod
    def get_state(cls, fast_ema: float, slow_ema: float) -> EMAState:
        """
        Returns the state of the fast EMA relative to the slow EMA (above or below).

        Args:
            fast_ema: The fast EMA value for the current bar.
            slow_ema: The slow EMA value for the current bar.

        Returns:
            EMAState: Whether the fast EMA is below or above the slow EMA.
        """
        if fast_ema > slow_ema:
            return EMAState.ABOVE
        else:
            return EMAState.BELOW
