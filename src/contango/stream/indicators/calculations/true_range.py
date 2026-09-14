from __future__ import annotations

from contango.stream.indicators.indicator import Indicator
from contango.trading.execution.engine.events.types import MarketDataEvent


USD = float


class TrueRange(Indicator[float | None]):
    """
    The volatility during a single trading period.
    """
    def __init__(self) -> None:
        """
        Initializes `TrueRange`.
        """
        self._previous_close: USD | None = None
        self._value: float | None = None

    def update(self, event: MarketDataEvent) -> float | None:
        """
        Updates the state of the true range for every bar.
        
        Args:
            event: The underlying event to update the true range with.
        
        Returns:
            float: The true range for the bar.
        """
        if self._previous_close is None:
            tr = event.high - event.low
        else:
            tr = max(
                event.high - event.low,
                abs(event.high - self._previous_close),
                abs(event.low - self._previous_close),
            )

        self._previous_close = event.close
        self._value = tr

        return tr

    @property
    def value(self) -> float | None:
        """
        Returns the latest value for the true range.
        """
        return self._value

    def __repr__(self) -> str:
        return f"TrueRange()"
