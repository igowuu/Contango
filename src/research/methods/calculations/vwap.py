from __future__ import annotations

from typing import NamedTuple


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


class VWAP:
    """
    Intraday VWAP with standard deviation bands.

    Resets at the start of each new trading session.
    Returns None on the first bar of each session (no deviation yet).
    """
    def __init__(self, k: float = 1.25) -> None:
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

    def reset(self) -> None:
        """
        Resets all accumulators for a new session.
        """
        self._cumulative_tp_volume = 0.0
        self._cumulative_volume = 0.0
        self._cumulative_tp_sq_volume = 0.0
        self._bar_count = 0

    def update(
        self,
        high: USD,
        low: USD,
        close: USD,
        volume: float
    ) -> VWAPSnapshot | None:
        """
        Ingests a new bar and returns the current VWAP snapshot.
        Returns None on the first bar of the session (standard deviation undefined).

        Args:
            high: Bar high price.
            low: Bar low price.
            close: Bar close price.
            volume: Bar volume.
        """
        typical_price = (high + low + close) / 3

        self._cumulative_tp_volume += typical_price * volume
        self._cumulative_volume += volume
        self._cumulative_tp_sq_volume += (typical_price ** 2) * volume
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

        return VWAPSnapshot(
            vwap=vwap,
            upper=vwap + band,
            lower=vwap - band,
        )
