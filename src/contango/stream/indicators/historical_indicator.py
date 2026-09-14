from __future__ import annotations

from typing import TypeVar, Generic

from contango.stream.indicators.indicator import Indicator
from contango.stream.historical_stream import HistoricalStream


R = TypeVar("R")


class HistoricalIndicator(HistoricalStream[R], Generic[R]):
    """
    A historical stream that allows historical access of indicators.

    Attributes:
        R: The return type for the historical indicator.
    """
    def __init__(self, source: Indicator[R], window: int) -> None:
        self._source = source
        super().__init__(source=source, window=window)

    def __repr__(self) -> str:
        return self._source.__repr__()
