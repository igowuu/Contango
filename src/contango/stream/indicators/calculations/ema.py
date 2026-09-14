from __future__ import annotations

from contango.stream.indicators.indicator import Indicator
from contango.trading.execution.engine.events.types import MarketDataEvent


USD = float
days = int


class EMA(Indicator[float | None]):
    """
    Exponential Moving Average.

    Uses alpha = 2 / (period + 1) and seeds the first value
    directly from the first price to avoid bias (towards 0).
    """
    def __init__(self, pd: days) -> None:
        """
        Initializes `Ema`.

        Args:
            pd: Lookback period to derive the smoothing factor. Larger values -> slower to react to price changes.
        """
        self._alpha = 2 / (pd + 1)
        self._value: float | None = None
        self._period = pd

    def update(self, event: MarketDataEvent) -> float:
        """
        Takes in a new price and returns the current EMA.

        Args:
            event: The current market data event.
        
        Returns:
            The current EMA. The first call returns `price` unsmoothed.
        """
        if self._value is None:
            self._value = event.close
        else:
            self._value = event.close * self._alpha + self._value * (1 - self._alpha)
        return self._value

    @property
    def value(self) -> float | None:
        """
        Returns the latest value for the EMA.
        """
        return self._value

    def __repr__(self) -> str:
        return f"EMA(period={self._period})"
