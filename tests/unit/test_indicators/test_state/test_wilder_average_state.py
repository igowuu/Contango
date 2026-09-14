from __future__ import annotations

from contango.stream.indicators.state.wilder_average_state import WilderState


def test_fast_above_slow() -> None:
    assert WilderState.get_state(fast_wilder_average=10.0, slow_wilder_average=5.0) is WilderState.ABOVE


def test_fast_below_slow() -> None:
    assert WilderState.get_state(fast_wilder_average=5.0, slow_wilder_average=10.0) is WilderState.BELOW


def test_fast_equal_to_slow_is_below() -> None:
    assert WilderState.get_state(fast_wilder_average=5.0, slow_wilder_average=5.0) is WilderState.BELOW
