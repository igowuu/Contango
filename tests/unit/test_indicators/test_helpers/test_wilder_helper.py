from __future__ import annotations

import pytest

from contango.stream.indicators.helpers.wilder_helper import WilderHelper


def test_returns_none_until_period_is_reached() -> None:
    helper = WilderHelper(period=3)

    assert helper.update(10.0) is None
    assert helper.update(20.0) is None


def test_first_full_window_seeds_with_simple_average() -> None:
    helper = WilderHelper(period=3)
    helper.update(10.0)
    helper.update(20.0)

    assert helper.update(30.0) == pytest.approx(20.0)


def test_subsequent_updates_use_wilder_smoothing_formula() -> None:
    helper = WilderHelper(period=3)
    for price in (10.0, 20.0, 30.0):
        helper.update(price)

    result = helper.update(40.0)

    assert result == pytest.approx(26.666666667)


def test_smoothing_compounds_correctly_across_multiple_updates() -> None:
    helper = WilderHelper(period=3)
    for price in (10.0, 20.0, 30.0, 40.0):
        helper.update(price)

    result = helper.update(50.0)

    assert result == pytest.approx(34.444444444)


def test_value_property_reflects_latest_update() -> None:
    helper = WilderHelper(period=2)
    helper.update(10.0)
    helper.update(20.0)

    assert helper.value == pytest.approx(15.0)
