from __future__ import annotations

from typing import NamedTuple

from research.methods.calculations.sma import SMA


USD = float
days = int


class BollingerBandSnapshot(NamedTuple):
    """
    A single snapshot of Bollinger Bands.

    Attributes:
        upper: The upper band for the current price.
        middle: The middle band (pure SMA) for the current price.
        lower: The lower band for the current price.
    """
    upper: float
    middle: float
    lower: float


class BollingerBands:
    """
    Rolling Bollinger Bands with variance updates.

    Wraps an SMA and tracks a running sum-of-squares so that population
    standard deviation is recomputed in constant time on every tick.
    Returns None until the lookback window is full.
    """
    def __init__(self, period: days = 20, k: float = 2.0) -> None:
        """
        Args:
            period: Lookback window in bars (default 20).
            k: Band-width multiplier in standard deviations (default 2.0).
        """
        self._period = period
        self._k = k
        self._sma = SMA(period)

        # Running accumulators for O(1) variance — no need to store raw prices.
        self._sum: float = 0.0
        self._sum_sq: float = 0.0
        self._count: int = 0

        # Circular buffer to track the value that ages out of the window.
        self._window: list[float] = [0.0] * period
        self._head: int = 0  # points to the oldest slot

    def update(self, price: USD) -> BollingerBandSnapshot | None:
        """
        Ingests a new price and return the current bands, or None while the
        window is still filling.

        Args:
            price: The price for the current bar.

        Returns:
            A BollingerBandSnapshot(upper, middle, lower), or None until
            `period` prices have been seen.
        """
        middle = self._sma.update(price)

        # Evict the oldest value once the window is full.
        if self._count == self._period:
            oldest = self._window[self._head]
            self._sum -= oldest
            self._sum_sq -= oldest * oldest

        # Insert the new price into the circular buffer.
        self._window[self._head] = price
        self._head = (self._head + 1) % self._period
        self._count = min(self._count + 1, self._period)

        self._sum += price
        self._sum_sq += price * price

        if middle is None:
            return None

        n = self._period
        variance = (self._sum_sq - self._sum * self._sum / n) / n
        band = self._k * (variance ** 0.5)

        return BollingerBandSnapshot(
            upper=middle + band,
            middle=middle,
            lower=middle - band,
        )
