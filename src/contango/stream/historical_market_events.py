from __future__ import annotations

from contango.stream.historical_stream import HistoricalStream
from contango.stream.stream import Stream
from contango.trading.execution.engine.events.types import MarketDataEvent


class HistoricalMarketEvents(HistoricalStream[MarketDataEvent]):
    """
    A historical stream of market data events.
    """
    def __init__(self, window: int) -> None:
        """
        Initializes `HistoricalMarketEvents`.
        
        Args:
            window: The maximum amount of lookback for the history of the stream.
        """
        super().__init__(source=_MarketEventRelay(), window=window)


class _MarketEventRelay(Stream[MarketDataEvent]):
    def __init__(self) -> None:
        self._value: MarketDataEvent | None = None

    def update(self, event: MarketDataEvent) -> MarketDataEvent:
        self._value = event
        return self._value

    @property
    def value(self) -> MarketDataEvent:
        if self._value is None:
            raise ValueError("MarketDataEvent was never set in .update() before the value was accessed.")

        return self._value
