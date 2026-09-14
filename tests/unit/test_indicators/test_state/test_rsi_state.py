from __future__ import annotations

from contango.stream.indicators.state.rsi_state import RSIState


def test_rsi_below_lower_threshold_is_oversold() -> None:
    assert RSIState.get_state(29.9, lower_threshold=30.0, upper_threshold=70.0) is RSIState.OVERSOLD


def test_rsi_exactly_at_lower_threshold_is_neutral() -> None:
    assert RSIState.get_state(30.0, lower_threshold=30.0, upper_threshold=70.0) is RSIState.NEUTRAL


def test_rsi_between_thresholds_is_neutral() -> None:
    assert RSIState.get_state(50.0, lower_threshold=30.0, upper_threshold=70.0) is RSIState.NEUTRAL


def test_rsi_exactly_at_upper_threshold_is_neutral() -> None:
    assert RSIState.get_state(70.0, lower_threshold=30.0, upper_threshold=70.0) is RSIState.NEUTRAL


def test_rsi_above_upper_threshold_is_overbought() -> None:
    assert RSIState.get_state(70.1, lower_threshold=30.0, upper_threshold=70.0) is RSIState.OVERBOUGHT
