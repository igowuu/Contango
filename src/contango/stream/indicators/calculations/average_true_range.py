from __future__ import annotations

from contango.stream.indicators.indicator import Indicator
from contango.stream.indicators.calculations.true_range import TrueRange
from contango.stream.indicators.helpers.wilder_helper import WilderHelper

from contango.trading.execution.engine.events.types import MarketDataEvent


USD = float
days = int


class AverageTrueRange(Indicator[float | None]):
    """
    The average true range (volatility measure).
    """
    def __init__(self, pd: days = 14) -> None:
        """
        Initializes `AverageTrueRange`.

        Args:
            pd: Lookback period used to smooth the True Range.
        """
        self._true_range = TrueRange()
        self._average = WilderHelper(pd)
        self._period = pd
        self._value: float | None = None

    def update(self, event: MarketDataEvent) -> float | None:
        """
        Updates the ATR for each bar.

        Args:
            event: The underlying event to update the ATR with.

        Returns:
            The current ATR. Returns None until enough bars have been
            observed to initialize the Wilder average.
        """
        tr = self._true_range.update(event)
        if tr is None:
            return None

        self._value = self._average.update(tr)
        return self._value

    @property
    def value(self) -> float | None:
        """
        Returns the latest value for the ATR.
        """
        return self._value

    def __repr__(self) -> str:
        return f"ATR(period={self._period})"
