from __future__ import annotations

import pytest

from contango.stream.indicators.calculations.rsi import RSI
from contango.trading.execution.engine.events.types import MarketDataEvent


def _bar(close: float) -> MarketDataEvent:
    return MarketDataEvent(1000, "AAPL", close, close, close, close, 1000)


def test_returns_none_until_wilder_averages_are_seeded() -> None:
    rsi = RSI(pd=3)

    assert rsi.update(_bar(100.0)) is None  # seeds prev_price only
    assert rsi.update(_bar(102.0)) is None  # gain window not yet full
    assert rsi.update(_bar(101.0)) is None  # gain window not yet full


def test_computes_rsi_once_gain_and_loss_averages_are_seeded() -> None:
    rsi = RSI(pd=3)
    for close in (100.0, 102.0, 101.0):
        rsi.update(_bar(close))

    result = rsi.update(_bar(105.0))

    assert result == pytest.approx(85.714285714)


def test_rsi_updates_correctly_across_subsequent_bars() -> None:
    rsi = RSI(pd=3)
    for close in (100.0, 102.0, 101.0, 105.0):
        rsi.update(_bar(close))

    result = rsi.update(_bar(103.0))

    assert result == pytest.approx(60.0)


def test_rsi_continues_updating_correctly() -> None:
    rsi = RSI(pd=3)
    for close in (100.0, 102.0, 101.0, 105.0, 103.0):
        rsi.update(_bar(close))

    result = rsi.update(_bar(108.0))

    assert result == pytest.approx(81.176470588)


def test_rsi_is_100_when_average_loss_is_zero() -> None:
    rsi = RSI(pd=2)
    for close in (100.0, 101.0, 102.0):
        result = rsi.update(_bar(close))

    assert result == pytest.approx(100.0)
