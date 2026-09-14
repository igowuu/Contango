from __future__ import annotations

from contango.stream.indicators.state.vwap_state import VWAPState
from contango.stream.indicators.calculations.vwap import VWAPSnapshot


def _snapshot() -> VWAPSnapshot:
    return VWAPSnapshot(vwap=100.0, upper=110.0, lower=90.0)


def test_price_below_lower_band() -> None:
    assert VWAPState.get_state(89.0, _snapshot()) is VWAPState.BELOW_LOWER


def test_price_exactly_at_lower_band_is_between_lower_and_vwap() -> None:
    assert VWAPState.get_state(90.0, _snapshot()) is VWAPState.BETWEEN_LOWER_AND_VWAP


def test_price_between_lower_and_vwap() -> None:
    assert VWAPState.get_state(95.0, _snapshot()) is VWAPState.BETWEEN_LOWER_AND_VWAP


def test_price_exactly_at_vwap_is_above_vwap() -> None:
    assert VWAPState.get_state(100.0, _snapshot()) is VWAPState.ABOVE_VWAP


def test_price_above_vwap() -> None:
    assert VWAPState.get_state(105.0, _snapshot()) is VWAPState.ABOVE_VWAP
