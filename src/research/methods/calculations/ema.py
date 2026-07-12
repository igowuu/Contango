from __future__ import annotations


USD = float
days = int


class EMA:
    """
    Exponential Moving Average.

    Uses the alpha = 2 / (period + 1) and seeds the first value
    directly from the first observed price to avoid bias towards zero.
    """
    def __init__(self, period: days) -> None:
        """
        Initializes `Ema`.

        Args:
            period: Lookback period to derive the smoothing factor. Larger values -> slower to react to price changes.
        """
        self._alpha = 2 / (period + 1)
        self._value: float | None = None
        self._period = period

    def update(self, price: USD) -> float:
        """
        Ingests a new price and returns the current EMA.

        Args:
            price: The price for the current bar.
        
        Returns:
            The current EMA. The first call returns `price` unsmoothed.
        """
        if self._value is None:
            self._value = price
        else:
            self._value = price * self._alpha + self._value * (1 - self._alpha)
        return self._value
