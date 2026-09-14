from __future__ import annotations

import pytest

from contango.stream.indicators.calculations.average_true_range import AverageTrueRange
from contango.trading.execution.engine.events.types import MarketDataEvent


def _bar(high: float, low: float, close: float) -> MarketDataEvent:
    return MarketDataEvent(1000, "AAPL", close, high, low, close, 1000)


def test_returns_none_until_wilder_average_is_seeded() -> None:
    atr = AverageTrueRange(pd=3)

    assert atr.update(_bar(high=110.0, low=100.0, close=105.0)) is None
    assert atr.update(_bar(high=112.0, low=104.0, close=108.0)) is None


def test_returns_wilder_average_of_true_ranges_once_seeded() -> None:
    atr = AverageTrueRange(pd=3)
    atr.update(_bar(high=110.0, low=100.0, close=105.0))  # tr = 10
    atr.update(_bar(high=112.0, low=104.0, close=108.0))  # tr = 8

    result = atr.update(_bar(high=100.0, low=90.0, close=95.0))

    assert result == pytest.approx(12.0)


def test_smooths_subsequent_true_ranges_via_wilder_formula() -> None:
    atr = AverageTrueRange(pd=3)
    atr.update(_bar(high=110.0, low=100.0, close=105.0))
    atr.update(_bar(high=112.0, low=104.0, close=108.0))
    atr.update(_bar(high=100.0, low=90.0, close=95.0))  # seeds at 12.0

    result = atr.update(_bar(high=105.0, low=95.0, close=100.0))

    assert result == pytest.approx(11.333333333)
