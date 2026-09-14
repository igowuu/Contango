from __future__ import annotations

from typing import Generic, TypeVar
from collections import deque
from typing import Deque

from contango.stream.stream import Stream
from contango.trading.execution.engine.events.types import MarketDataEvent


R = TypeVar("R")


class HistoricalStream(Stream[R], Generic[R]):
    """
    Wraps any stream and records a window of its past values.

    Attributes:
        R: The return type for the historical stream.
    """
    def __init__(self, source: Stream[R], window: int) -> None:
        """
        Initializes `HistoricalStream`.
        
        Args:
            source: The stream source to wrap.
            window: The maximum amount of lookback for the history of the stream.
        """
        self._source = source
        self._history: Deque[R] = deque(maxlen=window)

    def update(self, event: MarketDataEvent) -> R:
        """
        Updates the state of the historical stream given a market data event.
        """
        self._source.update(event)
        self._history.append(self._source.value)
        return self.value

    @property
    def value(self) -> R:
        """
        Returns the most recent value of the historical stream.
        """
        return self._history[-1]

    def previous(self, n: int = 1) -> R | None:
        """
        Returns the previous n amount of values backwards.
        For example, n=1 will be the previous value relative to the current one.
        
        Args:
            n: The amount of lookback.
        
        Returns:
            R: The stream value at n amount of lookback.
            None: If the history deque is shorter than the amount of lookback.
        """
        idx = -1 - n
        if len(self._history) <= n:
            return None
        return self._history[idx]

    def __getitem__(self, n: int) -> R | None:
        return self.value if n == 0 else self.previous(n)
