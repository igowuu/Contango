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
