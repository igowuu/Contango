from __future__ import annotations

from execution.engine.events.events import MarketDataEvent
from execution.engine.events.event_bus import EventBus


class MarketDataFeed:
    """
    Allows an OHLCV dataframe to be sequentially iterated over and published.
    """
    def __init__(self, data: list[MarketDataEvent], event_bus: EventBus):
        """
        Initializes `MarketDataFeed`.
        
        Args:
            data: The OHLCV list of `MarketDataEvent` to iterate over.
            event_bus: The event bus to publish `MarketDataEvent` instances to.
        """
        self._data = data
        self._event_bus = event_bus

    def get_initial_event(self) -> MarketDataEvent:
        """
        Returns the first `MarketDataEvent` in the OHLCV data.
        """
        return self._data[0]

    def run(self) -> None:
        """
        Iterates through the provided data & publishes 'MarketDataEvent` instances for each bar.
        """
        for event in self._data:
            self._event_bus.publish(event)
