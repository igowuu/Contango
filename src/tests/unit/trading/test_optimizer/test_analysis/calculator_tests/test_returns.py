# tests/unit/trading/test_optimizer/test_analysis/calculator_tests/test_returns.py — part of Contango, a parameterized backtesting & execution framework
# Copyright (C) 2026  Jacob Taylor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# pyright: reportPrivateUsage=false

import pytest

from trading.optimizer.analysis.context import EquityPoint
from trading.optimizer.analysis.calculators.returns import _get_monthly_returns, _get_total_return


class TestGetMonthlyReturns:
    """
    Logic & regression tests for the `_get_monthly_returns` method.

    Expected: The method returns a tuple of (unix_ms, percent) pairs representing
    the return for each calendar month present in the equity curve. Returns None
    for empty input.
    """
    def setup_method(self) -> None:
        self.single_month_gain = (
            EquityPoint(1704067200000, 1000.0),  # 2024-01-01
            EquityPoint(1706659200000, 1100.0),  # 2024-01-31
        )
        self.single_month_loss = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1706659200000, 900.0),
        )
        self.two_months_gains = (
            EquityPoint(1704067200000, 1000.0),  # 2024-01-01
            EquityPoint(1706659200000, 1100.0),  # 2024-01-31
            EquityPoint(1706745600000, 1100.0),  # 2024-02-01
            EquityPoint(1709078400000, 1210.0),  # 2024-02-28
        )
        self.mixed_months = (
            EquityPoint(1704067200000, 1000.0),  # 2024-01-01
            EquityPoint(1706659200000, 1100.0),  # 2024-01-31
            EquityPoint(1706745600000, 1100.0),  # 2024-02-01
            EquityPoint(1709078400000, 990.0),   # 2024-02-28
        )
        self.flat_month = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1706659200000, 1000.0),
        )

    def test_single_month_gain_returns_correct_percent(self) -> None:
        result = _get_monthly_returns(self.single_month_gain)
        assert result is not None
        assert len(result) == 1
        assert result[0][1] == pytest.approx(0.10)

    def test_single_month_loss_returns_negative_percent(self) -> None:
        result = _get_monthly_returns(self.single_month_loss)
        assert result is not None
        assert result[0][1] == pytest.approx(-0.10)

    def test_two_months_gains_returns_both(self) -> None:
        result = _get_monthly_returns(self.two_months_gains)
        assert result is not None
        assert len(result) == 2
        assert result[0][1] == pytest.approx(0.10)
        assert result[1][1] == pytest.approx(0.10)

    def test_mixed_months_returns_gain_and_loss(self) -> None:
        result = _get_monthly_returns(self.mixed_months)
        assert result is not None
        assert result[0][1] == pytest.approx(0.10)
        assert result[1][1] == pytest.approx(-0.10)

    def test_flat_month_returns_zero(self) -> None:
        result = _get_monthly_returns(self.flat_month)
        assert result is not None
        assert result[0][1] == pytest.approx(0.0)

    def test_each_entry_has_unix_ms_timestamp(self) -> None:
        result = _get_monthly_returns(self.two_months_gains)
        assert result is not None
        for timestamp, _ in result:
            assert isinstance(timestamp, int)

    def test_empty_input_returns_none(self) -> None:
        result = _get_monthly_returns(())
        assert result is None


class TestGetTotalReturn:
    """
    Logic & regression tests for the `_get_total_return` method.

    Expected: The method returns the total return (positive or negative) from
    the backtest at the end of execution, or None for degenerate inputs.
    """
    def setup_method(self) -> None:
        self.gain = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1717200000000, 1500.0),
        )
        self.loss = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1717200000000, 800.0),
        )
        self.flat = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1717200000000, 1000.0),
        )
        self.multi_point_gain = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1709251200000, 1200.0),
            EquityPoint(1711929600000, 1100.0),
            EquityPoint(1717200000000, 1500.0),
        )

    def test_gain_returns_positive_percent(self) -> None:
        result = _get_total_return(self.gain)
        assert result == pytest.approx(0.50)

    def test_loss_returns_negative_percent(self) -> None:
        result = _get_total_return(self.loss)
        assert result == pytest.approx(-0.20)

    def test_flat_returns_zero(self) -> None:
        result = _get_total_return(self.flat)
        assert result == pytest.approx(0.0)

    def test_empty_input_returns_none(self) -> None:
        result = _get_total_return(())
        assert result is None

    def test_single_point_returns_none(self) -> None:
        result = _get_total_return((EquityPoint(1704067200000, 1000.0),))
        assert result is None

    def test_only_first_and_last_points_matter(self) -> None:
        result = _get_total_return(self.multi_point_gain)
        assert result == pytest.approx(0.50)

    def test_zero_initial_equity_returns_none(self) -> None:
        curve = (
            EquityPoint(1704067200000, 0.0),
            EquityPoint(1717200000000, 1000.0),
        )
        result = _get_total_return(curve)
        assert result is None
