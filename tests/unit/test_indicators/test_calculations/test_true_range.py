from __future__ import annotations

from contango.stream.indicators.calculations.true_range import TrueRange
from contango.trading.execution.engine.events.types import MarketDataEvent


def _bar(high: float, low: float, close: float) -> MarketDataEvent:
    return MarketDataEvent(1000, "AAPL", close, high, low, close, 1000)


def test_first_bar_uses_high_minus_low_with_no_previous_close() -> None:
    tr = TrueRange()

    assert tr.update(_bar(high=110.0, low=100.0, close=105.0)) == 10.0


def test_subsequent_bar_takes_max_of_the_three_true_range_components() -> None:
    tr = TrueRange()
    tr.update(_bar(high=110.0, low=100.0, close=105.0))

    result = tr.update(_bar(high=112.0, low=104.0, close=108.0))

    assert result == 8.0


def test_gap_down_is_captured_via_low_minus_previous_close() -> None:
    tr = TrueRange()
    tr.update(_bar(high=110.0, low=100.0, close=105.0))
    tr.update(_bar(high=112.0, low=104.0, close=108.0))

    result = tr.update(_bar(high=100.0, low=90.0, close=95.0))

    assert result == 18.0


def test_value_property_reflects_the_latest_update() -> None:
    tr = TrueRange()

    tr.update(_bar(high=110.0, low=100.0, close=105.0))

    assert tr.value == 10.0
