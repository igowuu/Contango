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
