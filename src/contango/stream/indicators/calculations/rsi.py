from __future__ import annotations

from contango.stream.indicators.indicator import Indicator
from contango.stream.indicators.helpers.wilder_helper import WilderHelper
from contango.trading.execution.engine.events.types import MarketDataEvent


USD = float
days = int


class RSI(Indicator[float | None]):
    """
    Relative Strength Index (RSI).

    Uses Wilder's Moving Average to smooth average gains and losses
    over the given period. Returns None until both averages are seeded.
    """
    def __init__(self, pd: days = 14) -> None:
        """
        Initializes `RSI`.

        Args:
            pd: Lookback period for the Wilder averages.
        """
        self._period = pd
        self._avg_gain = WilderHelper(pd)
        self._avg_loss = WilderHelper(pd)
        self._prev_price: float | None = None
        self._value: float | None = None

    def update(self, event: MarketDataEvent) -> float | None:
        """
        Takes in a new price and returns the current RSI.

        Args:
            event: The underlying event to update the RSI with.

        Returns:
            RSI in the range [0, 100], or None if the period has not been reached.
        """
        if self._prev_price is None:
            self._prev_price = event.close
            return None

        delta = event.close - self._prev_price
        self._prev_price = event.close

        gain = max(delta, 0.0)
        loss = max(-delta, 0.0)

        avg_gain = self._avg_gain.update(gain)
        avg_loss = self._avg_loss.update(loss)

        if avg_gain is None or avg_loss is None:
            return None

        if avg_loss == 0.0:
            return 100.0

        rs = avg_gain / avg_loss

        self._value = 100 - (100 / (1 + rs))

        return self._value

    @property
    def value(self) -> float | None:
        """
        Returns the latest value for the RSI.
        """
        return self._value

    def __repr__(self) -> str:
        return f"RSI(period={self._period})"
