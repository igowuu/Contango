from __future__ import annotations

import pytest

from contango.stream.indicators.calculations.bollinger_bands import BollingerBands
from contango.trading.execution.engine.events.types import MarketDataEvent


def _bar(close: float) -> MarketDataEvent:
    return MarketDataEvent(1000, "AAPL", close, close, close, close, 1000)


def test_returns_none_until_window_is_full() -> None:
    bb = BollingerBands(pd=3, k=2.0)

    assert bb.update(_bar(10.0)) is None
    assert bb.update(_bar(12.0)) is None


def test_computes_bands_once_window_is_full() -> None:
    bb = BollingerBands(pd=3, k=2.0)
    bb.update(_bar(10.0))
    bb.update(_bar(12.0))
    result = bb.update(_bar(11.0))

    assert result is not None
    assert result.middle == pytest.approx(11.0)
    assert result.stdev == pytest.approx(0.816496581)
    assert result.upper == pytest.approx(12.632993162)
    assert result.lower == pytest.approx(9.367006838)


def test_rolls_the_window_and_recomputes_bands() -> None:
    bb = BollingerBands(pd=3, k=2.0)
    for close in (10.0, 12.0, 11.0):
        bb.update(_bar(close))

    result = bb.update(_bar(13.0))

    assert result is not None
    assert result.middle == pytest.approx(12.0)
    assert result.upper == pytest.approx(13.632993162)
    assert result.lower == pytest.approx(10.367006838)
