
from __future__ import annotations

from collections import deque

from contango.stream.indicators.indicator import Indicator
from contango.trading.execution.engine.events.types import MarketDataEvent


USD = float
days = int


class WilderAverage(Indicator[float | None]):
    """
    Wilder's Moving Average (RMA).
    """
    def __init__(self, pd: days) -> None:
        """
        Initializes `WilderAverage`.
        
        Args:
            pd: Lookback period to derive the smoothing factor. Larger values -> slower to react to price changes.
        """
        self._period = pd
        self._window: deque[float] = deque(maxlen=pd)

        self._value: float | None = None

    def update(self, event: MarketDataEvent) -> float | None:
        """
        Takes in a new value and return smoothed result.

        Args:
            event: The underlying event to update the wilder average with.
        
        Returns:
            The current WilderAverage. Returns None if period amount of days have not been reached.
        """
        self._window.append(event.close)

        if len(self._window) < self._period:
            return None

        # First full initialization: simple average
        if self._value is None:
            self._value = sum(self._window) / self._period
            return self._value

        self._value = (
            (self._value * (self._period - 1)) + event.close
        ) / self._period

        return self._value

    @property
    def value(self) -> float | None:
        """
        Returns the latest value for the wilder average.
        """
        return self._value

    def __repr__(self) -> str:
        return f"WilderAverage(period={self._period})"
