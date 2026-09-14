from __future__ import annotations

from contango.stream.indicators.state.bollinger_bands_state import BollingerState
from contango.stream.indicators.calculations.bollinger_bands import BollingerBandSnapshot


def _bands() -> BollingerBandSnapshot:
    return BollingerBandSnapshot(upper=110.0, middle=100.0, lower=90.0, stdev=5.0)


def test_price_below_lower_band() -> None:
    assert BollingerState.get_state(89.0, _bands()) is BollingerState.BELOW_LOWER


def test_price_exactly_at_lower_band_is_between_lower_and_middle() -> None:
    assert BollingerState.get_state(90.0, _bands()) is BollingerState.BETWEEN_LOWER_AND_MIDDLE


def test_price_between_lower_and_middle() -> None:
    assert BollingerState.get_state(95.0, _bands()) is BollingerState.BETWEEN_LOWER_AND_MIDDLE


def test_price_exactly_at_middle_band_is_between_middle_and_higher() -> None:
    assert BollingerState.get_state(100.0, _bands()) is BollingerState.BETWEEN_MIDDLE_AND_HIGHER


def test_price_between_middle_and_upper() -> None:
    assert BollingerState.get_state(105.0, _bands()) is BollingerState.BETWEEN_MIDDLE_AND_HIGHER


def test_price_exactly_at_upper_band_is_above_higher() -> None:
    assert BollingerState.get_state(110.0, _bands()) is BollingerState.ABOVE_HIGHER


def test_price_above_upper_band() -> None:
    assert BollingerState.get_state(111.0, _bands()) is BollingerState.ABOVE_HIGHER
