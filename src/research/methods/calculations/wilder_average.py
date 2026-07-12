from __future__ import annotations

from collections import deque


USD = float
days = int


class WilderAverage:
    """
    Wilder's Moving Average (RMA).

    Equivalent to an EMA with alpha = 1/period, but seeded
    using a simple average of the first `period` values.
    """
    def __init__(self, period: days) -> None:
        """
        Initializes `WilderAverage`.
        
        Args:
            period: Lookback period to derive the smoothing factor. Larger values -> slower to react to price changes.
        """
        self._period = period
        self._window: deque[float] = deque(maxlen=period)

        self._value: float | None = None

    def update(self, price: USD) -> float | None:
        """
        Ingests a new value and return smoothed result.

        Args:
            price: The price for the current bar.
        
        Returns:
            The current WilderAverage. Returns None if period amount of days have not been reached.
        """
        self._window.append(price)

        if len(self._window) < self._period:
            return None

        # First full initialization: simple average
        if self._value is None:
            self._value = sum(self._window) / self._period
            return self._value

        self._value = (
            (self._value * (self._period - 1)) + price
        ) / self._period

        return self._value
