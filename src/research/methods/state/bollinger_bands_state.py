from __future__ import annotations

from enum import Enum, auto

from research.methods.calculations.bollinger_bands import BollingerBandSnapshot


class BollingerState(Enum):
    """
    Current price location relative to Bollinger Bands.

    Attributes:
        BELOW_LOWER: The price is below the lower bollinger band.
        BETWEEN_LOWER_AND_MIDDLE: The price is between the lower & middle bollinger bands.
        BETWEEN_MIDDLE_AND_HIGHER: The price is above the middle bollinger band but below the higher one.
        ABOVE_HIGHER: The price is above the higher bollinger band.
    """
    BELOW_LOWER = auto()
    BETWEEN_LOWER_AND_MIDDLE = auto()
    BETWEEN_MIDDLE_AND_HIGHER = auto()
    ABOVE_HIGHER = auto()


    @classmethod
    def get_state(cls, current_price: float, bands: BollingerBandSnapshot) -> BollingerState:
        """
        Returns the band zone that the price is currently in.

        Args:
            current_price: The price for the current bar.
            bands: The snapshot of bollinger bands for the current bar.
        
        Returns:
            BollingerState: The state enum of the price relative to the bollinger bands.
        """
        if current_price < bands.lower:
            return BollingerState.BELOW_LOWER
        if current_price < bands.middle:
            return BollingerState.BETWEEN_LOWER_AND_MIDDLE
        if current_price > bands.middle:
            return BollingerState.BETWEEN_MIDDLE_AND_HIGHER
        return BollingerState.ABOVE_HIGHER
