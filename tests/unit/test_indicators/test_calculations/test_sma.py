from __future__ import annotations

import pytest

from contango.stream.indicators.calculations.sma import SMA
from contango.trading.execution.engine.events.types import MarketDataEvent


def _bar(close: float) -> MarketDataEvent:
    return MarketDataEvent(1000, "AAPL", close, close, close, close, 1000)


def test_returns_none_until_window_is_full() -> None:
    sma = SMA(pd=3)

    assert sma.update(_bar(10.0)) is None
    assert sma.update(_bar(20.0)) is None


def test_returns_average_once_window_is_full() -> None:
    sma = SMA(pd=3)
    sma.update(_bar(10.0))
    sma.update(_bar(20.0))

    assert sma.update(_bar(30.0)) == pytest.approx(20.0)


def test_rolls_the_window_and_evicts_the_oldest_price() -> None:
    sma = SMA(pd=3)
    for close in (10.0, 20.0, 30.0):
        sma.update(_bar(close))

    result = sma.update(_bar(40.0))

    assert result == pytest.approx(30.0)


def test_value_property_reflects_latest_update() -> None:
    sma = SMA(pd=2)
    sma.update(_bar(10.0))
    sma.update(_bar(20.0))

    assert sma.value == pytest.approx(15.0)