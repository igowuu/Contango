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
