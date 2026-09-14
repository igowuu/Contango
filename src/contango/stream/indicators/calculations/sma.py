from __future__ import annotations

from collections import deque

from contango.stream.indicators.indicator import Indicator
from contango.trading.execution.engine.events.types import MarketDataEvent


USD = float
days = int


class SMA(Indicator[float | None]):
    """
    Simple Moving Average.

    Maintains a window of prices and tracks their sum incrementally.
    Returns None until the window is full.
    """
    def __init__(self, pd: days) -> None:
        """
        Initializes `SMA`.

        Args:
            pd: The number of days (period) for the rolling window.
        """
        self._period = pd
        self._window: deque[float] = deque(maxlen=pd)
        self._sum = 0.0
        self._value: float | None = None

    def update(self, event: MarketDataEvent) -> float | None:
        """
        Takes in a new price and returns the current SMA, or None if the window is not yet full.

        Args:
            event: The underlying event to update teh SMA with.
        
        Returns:
            The SMA over the current window, or `None` if `period` amount of days have not passed.
        """
        if len(self._window) == self._period:
            self._sum -= self._window[0]

        self._window.append(event.close)
        self._sum += event.close

        if len(self._window) < self._period:
            return None

        self._value = self._sum / self._period

        return self._value

    @property
    def value(self) -> float | None:
        """
        Returns the latest value for the SMA.
        """
        return self._value

    def __repr__(self) -> str:
        return f"SMA(period={self._period})"
