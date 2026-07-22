# tests/unit/trading/test_optimizer/test_analysis/calculator_tests/test_drawdown.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.optimizer.analysis.context import DrawdownPoint
from trading.optimizer.analysis.calculators.drawdown import _get_average_drawdown, _get_max_drawdown


class TestGetAverageDrawdown:
    """
    Logic & regression tests for the `get_average_drawdown` method.

    Expected: The method returns the mean of all negative values, not taking into account
    positive or zero values. Returns None when no negative values exist.
    """
    def setup_method(self) -> None:
        self.single_negative = (
            self._make_drawdown_point(-0.05),
        )
        self.all_negative = (
            self._make_drawdown_point(-0.10),
            self._make_drawdown_point(-0.20),
            self._make_drawdown_point(-0.30),
        )
        self.all_positive = (
            self._make_drawdown_point(0.10),
            self._make_drawdown_point(0.20),
        )
        self.mixed = (
            self._make_drawdown_point(-0.10),
            self._make_drawdown_point(0.05),
            self._make_drawdown_point(-0.30),
            self._make_drawdown_point(0.20),
        )
        self.with_zeros = (
            self._make_drawdown_point(0.0),
            self._make_drawdown_point(-0.20),
            self._make_drawdown_point(0.0),
        )

    def _make_drawdown_point(self, drawdown_percent: float, peak_equity: float = 1000.0) -> DrawdownPoint:
        return DrawdownPoint(
            timestamp=1704067200000,
            peak_equity=peak_equity,
            drawdown_percent=drawdown_percent,
        )

    def test_all_negative_returns_mean(self) -> None:
        result = _get_average_drawdown(self.all_negative)
        assert result == pytest.approx(-0.20)

    def test_mixed_signs_excludes_positives(self) -> None:
        result = _get_average_drawdown(self.mixed)
        assert result == pytest.approx(-0.20)

    def test_all_positive_returns_none(self) -> None:
        result = _get_average_drawdown(self.all_positive)
        assert result is None

    def test_empty_input_returns_none(self) -> None:
        result = _get_average_drawdown(())
        assert result is None

    def test_single_negative_returns_that_value(self) -> None:
        result = _get_average_drawdown(self.single_negative)
        assert result == pytest.approx(-0.05)

    def test_zero_drawdown_is_excluded(self) -> None:
        result = _get_average_drawdown(self.with_zeros)
        assert result == pytest.approx(-0.20)


class TestGetMaxDrawdown:
    """
    Logic & regression tests for the `_get_max_drawdown` method.

    Expected: The method returns the smallest (most negative) drawdown percent,
    ignoring positive and zero values. Returns None when no negative values exist.
    """
    def setup_method(self) -> None:
        self.single_negative = (
            self._make_drawdown_point(-0.05),
        )
        self.all_negative = (
            self._make_drawdown_point(-0.10),
            self._make_drawdown_point(-0.20),
            self._make_drawdown_point(-0.30),
        )
        self.all_positive = (
            self._make_drawdown_point(0.10),
            self._make_drawdown_point(0.20),
        )
        self.mixed = (
            self._make_drawdown_point(-0.10),
            self._make_drawdown_point(0.05),
            self._make_drawdown_point(-0.30),
            self._make_drawdown_point(0.20),
        )
        self.with_zeros = (
            self._make_drawdown_point(0.0),
            self._make_drawdown_point(-0.20),
            self._make_drawdown_point(0.0),
        )

    def _make_drawdown_point(self, drawdown_percent: float, peak_equity: float = 1000.0) -> DrawdownPoint:
        return DrawdownPoint(
            timestamp=1704067200000,
            peak_equity=peak_equity,
            drawdown_percent=drawdown_percent,
        )

    def test_all_negative_returns_minimum(self) -> None:
        result = _get_max_drawdown(self.all_negative)
        assert result == pytest.approx(-0.30)

    def test_mixed_signs_excludes_positives(self) -> None:
        result = _get_max_drawdown(self.mixed)
        assert result == pytest.approx(-0.30)

    def test_all_positive_returns_none(self) -> None:
        result = _get_max_drawdown(self.all_positive)
        assert result is None

    def test_empty_input_returns_none(self) -> None:
        result = _get_max_drawdown(())
        assert result is None

    def test_single_negative_returns_that_value(self) -> None:
        result = _get_max_drawdown(self.single_negative)
        assert result == pytest.approx(-0.05)

    def test_zero_drawdown_is_excluded(self) -> None:
        result = _get_max_drawdown(self.with_zeros)
        assert result == pytest.approx(-0.20)
