from __future__ import annotations

from contango.stream.indicators.state.sma_state import SMAState


def test_fast_above_slow() -> None:
    assert SMAState.get_state(fast_sma=10.0, slow_sma=5.0) is SMAState.ABOVE


def test_fast_below_slow() -> None:
    assert SMAState.get_state(fast_sma=5.0, slow_sma=10.0) is SMAState.BELOW


def test_fast_equal_to_slow_is_below() -> None:
    assert SMAState.get_state(fast_sma=5.0, slow_sma=5.0) is SMAState.BELOW
