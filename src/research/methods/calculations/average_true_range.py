from __future__ import annotations

from research.methods.calculations.true_range import TrueRange
from research.methods.calculations.wilder_average import WilderAverage


USD = float
days = int


class AverageTrueRange:
    """
    The average true range (volatility measure).
    """
    def __init__(self, period: days = 14) -> None:
        """
        Initializes `AverageTrueRange`.

        Args:
            period: Lookback period used to smooth the True Range.
        """
        self._true_range = TrueRange()
        self._average = WilderAverage(period)

    def update(self, high: USD, low: USD, close: USD) -> float | None:
        """
        Updates the ATR for each bar.

        Args:
            high: The highest price reached in USD for a bar.
            low: The lowest price reached in USD for a bar.
            close: The closing price in USD for a bar.

        Returns:
            The current ATR. Returns None until enough bars have been
            observed to initialize the Wilder average.
        """
        tr = self._true_range.update(high, low, close)
        return self._average.update(tr)
