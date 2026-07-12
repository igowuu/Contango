# pyright: reportPrivateUsage=false

import pytest

from optimizer.analysis.context import EquityPoint
from optimizer.analysis.builder import _build_returns


class TestBuildReturns:
    """
    Logic & regression tests for the `_build_returns` function.

    Expected: Builds a sequence of period-over-period ReturnPoints from an
    equity curve. Each return is relative to the immediately preceding point,
    not the starting equity. Raises ValueError if any equity point is zero.
    """
    def setup_method(self) -> None:
        self.single_point = (
            EquityPoint(1704067200000, 1000.0),
        )
        self.two_points_gain = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 1100.0),
        )
        self.two_points_loss = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 900.0),
        )
        self.three_points = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 1100.0),
            EquityPoint(1704240000000, 1045.0),
        )
        self.period_over_period = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 1100.0),
            EquityPoint(1704240000000, 1210.0),
        )
        self.with_zero_equity = (
            EquityPoint(1704067200000, 0.0),
            EquityPoint(1704153600000, 1000.0),
        )

    def test_empty_input_returns_empty(self) -> None:
        result = _build_returns(())
        assert result == ()

    def test_single_point_returns_empty(self) -> None:
        result = _build_returns(self.single_point)
        assert result == ()

    def test_two_points_gain_returns_single_return(self) -> None:
        result = _build_returns(self.two_points_gain)
        assert len(result) == 1
        assert result[0].return_percent == pytest.approx(0.10)

    def test_two_points_loss_returns_negative_return(self) -> None:
        result = _build_returns(self.two_points_loss)
        assert len(result) == 1
        assert result[0].return_percent == pytest.approx(-0.10)

    def test_n_points_returns_n_minus_one_returns(self) -> None:
        result = _build_returns(self.three_points)
        assert len(result) == 2

    def test_returns_are_period_over_period_not_since_start(self) -> None:
        # 1000 → 1100 → 1210: each period is +10%, not +10% then +21%
        result = _build_returns(self.period_over_period)
        assert result[0].return_percent == pytest.approx(0.10)
        assert result[1].return_percent == pytest.approx(0.10)

    def test_timestamps_are_preserved(self) -> None:
        result = _build_returns(self.two_points_gain)
        assert result[0].timestamp == 1704153600000

    def test_zero_equity_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            _build_returns(self.with_zero_equity)
