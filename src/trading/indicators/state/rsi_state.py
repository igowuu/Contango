# trading/indicators/state/rsi_state.py — part of Contango, a parameterized backtesting & execution framework
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


class RSIState(Enum):
    """
    The position of the RSI relative to its thresholds.

    Attributes:
        OVERSOLD: RSI is below lower threshold.
        NEUTRAL: RSI is between thresholds.
        OVERBOUGHT: RSI is above upper threshold.
    """
    OVERSOLD = auto()
    NEUTRAL = auto()
    OVERBOUGHT = auto()


    @classmethod
    def get_state(
        cls,
        rsi: float, 
        lower_threshold: float, 
        upper_threshold: float
    ) -> RSIState:
        """
        Returns the state of the RSI relative to its thresholds.

        Args:
            rsi: The RSI value for the current bar.
            lower_threshold: The lower threshold for the RSI (determines if oversold).
            upper_threshold: The upper threshold for the RSI (determines if overbought).
        
        Returns:
            RSIState: Whether the RSI is above or below their respective thresholds (oversold or overbought).
        """
        if rsi < lower_threshold:
            return RSIState.OVERSOLD
        elif rsi > upper_threshold:
            return RSIState.OVERBOUGHT
        else:
            return RSIState.NEUTRAL
