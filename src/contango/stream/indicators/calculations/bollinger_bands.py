from __future__ import annotations

from typing import NamedTuple

from contango.stream.indicators.indicator import Indicator
from contango.trading.execution.engine.events.types import MarketDataEvent


USD = float
days = int


class BollingerBandSnapshot(NamedTuple):
    """
    A single snapshot of Bollinger Bands.

    Attributes:
        upper: The upper band for the current price.
        middle: The middle band (pure SMA) for the current price.
        lower: The lower band for the current price.
        stdev: The population standard deviation over the lookback window.
    """
    upper: float
    middle: float
    lower: float
    stdev: float


class BollingerBands(Indicator[BollingerBandSnapshot | None]):
    """
    Rolling Bollinger Bands with variance updates.

    Wraps an SMA and tracks a running sum-of-squares so that
    standard deviation is recomputed in constant time on every tick.
    Returns None until the lookback window is full.
    """
    def __init__(self, pd: days = 20, k: float = 2.0) -> None:
        """
        Args:
            pd: Lookback window in bars (default 20).
            k: Band-width multiplier in standard deviations (default 2.0).
        """
        self._period = pd
        self._k = k

        self._sum: float = 0.0
        self._sum_sq: float = 0.0
        self._count: int = 0

        self._window: list[float] = [0.0] * pd
        self._head: int = 0

        self._value: BollingerBandSnapshot | None = None

    def update(self, event: MarketDataEvent) -> BollingerBandSnapshot | None:
        """
        Takes in a new price and return the current bands, or None while the
        window is still filling.

        Args:
            event: The underlying event to update the bollinger bands indicator with.

        Returns:
            A BollingerBandSnapshot(upper, middle, lower), or None until
            `period` prices have been seen.
        """
        if self._count == self._period:
            oldest = self._window[self._head]
            self._sum -= oldest
            self._sum_sq -= oldest * oldest

        self._window[self._head] = event.close
        self._head = (self._head + 1) % self._period
        self._count = min(self._count + 1, self._period)

        self._sum += event.close
        self._sum_sq += event.close * event.close

        if self._count < self._period:
            return None

        n = self._period
        middle = self._sum / n
        variance = (self._sum_sq - self._sum * self._sum / n) / n
        stdev = variance ** 0.5
        band = self._k * stdev

        self._value = BollingerBandSnapshot(
            upper=middle + band,
            middle=middle,
            lower=middle - band,
            stdev=stdev,
        )
        return self._value

    @property
    def value(self) -> BollingerBandSnapshot | None:
        """
        Returns the latest value for the bollinger bands.
        """
        return self._value

    def __repr__(self) -> str:
        return f"BollingerBands(period={self._period}, k={self._k})"
