from __future__ import annotations

from collections import deque


USD = float
days = int


class SMA:
    """
    Rolling Simple Moving Average.

    Maintains a fixed-size window of prices and tracks their sum incrementally.
    Returns None until the window is full.
    """
    def __init__(self, period: days) -> None:
        """
        Initializes `SMA`.

        Args:
            period: The number of days (period) for the rolling window.
        """
        self._period = period
        self._window: deque[float] = deque(maxlen=period)
        self._sum = 0.0

    def update(self, price: USD) -> float | None:
        """
        Ingests a new price and returns the current SMA, or None if the window is not yet full.

        Args:
            price: The price for the current bar.
        
        Returns:
            The SMA over the current window, or `None` if `period` amount of days have not passed.
        """
        if len(self._window) == self._period:
            self._sum -= self._window[0]

        self._window.append(price)
        self._sum += price

        if len(self._window) < self._period:
            return None

        return self._sum / self._period
