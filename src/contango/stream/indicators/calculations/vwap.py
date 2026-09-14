from __future__ import annotations

from typing import NamedTuple

from contango.stream.indicators.indicator import Indicator
from contango.trading.execution.engine.events.types import MarketDataEvent


USD = float


class VWAPSnapshot(NamedTuple):
    """
    A single snapshot of VWAP with bands.

    Attributes:
        vwap: The current volume-weighted average price.
        upper: VWAP + k standard deviations.
        lower: VWAP - k standard deviations.
    """
    vwap: float
    upper: float
    lower: float


class VWAP(Indicator[VWAPSnapshot | None]):
    """
    VWAP with standard deviation bands.

    Returns None on the first bar of each session (no deviation yet).
    """
    def __init__(self, k: float) -> None:
        """
        Args:
            k: Band-width multiplier in standard deviations.
        """
        self._k = k

        # Intraday accumulators — reset each session
        self._cumulative_tp_volume: float = 0.0
        self._cumulative_volume: float = 0.0
        self._cumulative_tp_sq_volume: float = 0.0
        self._bar_count: int = 0

        self._value: VWAPSnapshot | None = None

    def update(self, event: MarketDataEvent) -> VWAPSnapshot | None:
        """
        Takes in a new bar and returns the current VWAP snapshot.
        Returns None on the first bar of the session (standard deviation undefined).

        Args:
            event: The underlying event to update the VWAP with.
        
        Returns:
            VWAPSnapshot | None: If the VWAP is settled, returns a snapshot containing
                                 the VWAP alongside the upper and lower VWAP bounds.
        """
        typical_price = (event.high + event.low + event.close) / 3

        self._cumulative_tp_volume += typical_price * event.volume
        self._cumulative_volume += event.volume
        self._cumulative_tp_sq_volume += (typical_price ** 2) * event.volume
        self._bar_count += 1

        if self._cumulative_volume == 0:
            return None

        vwap = self._cumulative_tp_volume / self._cumulative_volume

        # Volume-weighted variance
        variance = (
            self._cumulative_tp_sq_volume / self._cumulative_volume
        ) - vwap ** 2

        # Variance can be slightly negative due to floating point
        std = max(variance, 0.0) ** 0.5

        if self._bar_count < 2:
            return None

        band = self._k * std

        self._value = VWAPSnapshot(
            vwap=vwap,
            upper=vwap + band,
            lower=vwap - band,
        )

        return self._value

    @property
    def value(self) -> VWAPSnapshot | None:
        """
        Returns the latest value for the VWAP.
        """
        return self._value

    def __repr__(self) -> str:
        return f"VWAP(k={self._k})"