from __future__ import annotations

import pytest

from contango.stream.indicators.calculations.vwap import VWAP
from contango.trading.execution.engine.events.types import MarketDataEvent


def _bar(high: float, low: float, close: float, volume: int) -> MarketDataEvent:
    return MarketDataEvent(1000, "AAPL", close, high, low, close, volume)


def test_returns_none_on_the_first_bar_of_a_session() -> None:
    vwap = VWAP(k=1.0)

    assert vwap.update(_bar(high=10.0, low=8.0, close=9.0, volume=100)) is None


def test_computes_vwap_and_bands_from_the_second_bar() -> None:
    vwap = VWAP(k=1.0)
    vwap.update(_bar(high=10.0, low=8.0, close=9.0, volume=100))

    result = vwap.update(_bar(high=11.0, low=9.0, close=10.0, volume=150))

    assert result is not None
    assert result.vwap == pytest.approx(9.6)
    assert result.upper == pytest.approx(10.089897949)
    assert result.lower == pytest.approx(9.110102051)


def test_vwap_updates_correctly_on_a_third_bar() -> None:
    vwap = VWAP(k=1.0)
    vwap.update(_bar(high=10.0, low=8.0, close=9.0, volume=100))
    vwap.update(_bar(high=11.0, low=9.0, close=10.0, volume=150))

    result = vwap.update(_bar(high=12.0, low=10.0, close=11.0, volume=200))

    assert result is not None
    assert result.vwap == pytest.approx(10.222222222)
    assert result.upper == pytest.approx(11.007896)
    assert result.lower == pytest.approx(9.436548)
