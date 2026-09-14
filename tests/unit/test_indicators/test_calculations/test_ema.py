from __future__ import annotations

import pytest

from contango.stream.indicators.calculations.ema import EMA
from contango.trading.execution.engine.events.types import MarketDataEvent


def _bar(close: float) -> MarketDataEvent:
    return MarketDataEvent(1000, "AAPL", close, close, close, close, 1000)


def test_first_update_seeds_directly_from_price_unsmoothed() -> None:
    ema = EMA(pd=3)

    assert ema.update(_bar(10.0)) == pytest.approx(10.0)


def test_subsequent_updates_apply_exponential_smoothing() -> None:
    ema = EMA(pd=3)  # alpha = 2 / (3 + 1) = 0.5
    ema.update(_bar(10.0))

    assert ema.update(_bar(20.0)) == pytest.approx(15.0)


def test_smoothing_compounds_across_multiple_updates() -> None:
    ema = EMA(pd=3)
    ema.update(_bar(10.0))
    ema.update(_bar(20.0))

    result = ema.update(_bar(30.0))

    assert result == pytest.approx(22.5)


def test_larger_period_reacts_more_slowly_to_price_changes() -> None:
    fast = EMA(pd=2)   # alpha = 2/3
    slow = EMA(pd=10)  # alpha = 2/11
    for ema in (fast, slow):
        ema.update(_bar(100.0))
        ema.update(_bar(200.0))

    assert fast.value is not None and slow.value is not None
    assert fast.value > slow.value


def test_value_property_reflects_latest_update() -> None:
    ema = EMA(pd=3)
    ema.update(_bar(10.0))

    assert ema.value == pytest.approx(10.0)
