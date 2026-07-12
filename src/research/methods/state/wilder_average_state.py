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
