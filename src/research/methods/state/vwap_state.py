from __future__ import annotations

from enum import Enum, auto

from research.methods.calculations.vwap import VWAPSnapshot


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
