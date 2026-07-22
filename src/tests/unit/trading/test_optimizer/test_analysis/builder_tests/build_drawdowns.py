# tests/unit/trading/test_optimizer/test_analysis/builder_tests/build_drawdowns.py — part of Contango, a parameterized backtesting & execution framework
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
from trading.optimizer.analysis.builder import _build_drawdowns


class TestBuildDrawdowns:
    """
    Logic & regression tests for the `_build_drawdowns` function.

    Expected: Builds a chronological sequence of DrawdownPoints tracking the
    running peak and percentage decline from it. The peak never decreases.
    A new all-time high produces a drawdown of 0.0. Recovery back to peak
    also produces 0.0.
    """
    def setup_method(self) -> None:
        self.single_point = (
            EquityPoint(1704067200000, 1000.0),
        )
        self.monotonic_gain = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 1100.0),
            EquityPoint(1704240000000, 1200.0),
        )
        self.monotonic_loss = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 900.0),
            EquityPoint(1704240000000, 800.0),
        )
        self.drawdown_then_recovery = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 800.0),
            EquityPoint(1704240000000, 1000.0),
        )
        self.drawdown_then_new_high = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 800.0),
            EquityPoint(1704240000000, 1100.0),
        )
        self.multiple_peaks = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704153600000, 1200.0),
            EquityPoint(1704240000000, 900.0),
            EquityPoint(1704326400000, 1100.0),
            EquityPoint(1704412800000, 1300.0),
        )

    def test_empty_input_returns_empty(self) -> None:
        result = _build_drawdowns(())
        assert result == ()

    def test_single_point_returns_zero_drawdown(self) -> None:
        result = _build_drawdowns(self.single_point)
        assert len(result) == 1
        assert result[0].drawdown_percent == pytest.approx(0.0)
        assert result[0].peak_equity == pytest.approx(1000.0)

    def test_n_points_returns_n_drawdown_points(self) -> None:
        result = _build_drawdowns(self.monotonic_gain)
        assert len(result) == 3

    def test_monotonic_gain_all_drawdowns_are_zero(self) -> None:
        result = _build_drawdowns(self.monotonic_gain)
        for point in result:
            assert point.drawdown_percent == pytest.approx(0.0)

    def test_monotonic_gain_peak_tracks_current_equity(self) -> None:
        result = _build_drawdowns(self.monotonic_gain)
        assert result[0].peak_equity == pytest.approx(1000.0)
        assert result[1].peak_equity == pytest.approx(1100.0)
        assert result[2].peak_equity == pytest.approx(1200.0)

    def test_monotonic_loss_peak_does_not_decrease(self) -> None:
        result = _build_drawdowns(self.monotonic_loss)
        for point in result:
            assert point.peak_equity == pytest.approx(1000.0)

    def test_monotonic_loss_drawdowns_are_negative(self) -> None:
        result = _build_drawdowns(self.monotonic_loss)
        assert result[0].drawdown_percent == pytest.approx(0.0)
        assert result[1].drawdown_percent == pytest.approx(-0.10)
        assert result[2].drawdown_percent == pytest.approx(-0.20)

    def test_recovery_to_peak_gives_zero_drawdown(self) -> None:
        result = _build_drawdowns(self.drawdown_then_recovery)
        assert result[0].drawdown_percent == pytest.approx(0.0)
        assert result[1].drawdown_percent == pytest.approx(-0.20)
        assert result[2].drawdown_percent == pytest.approx(0.0)

    def test_new_high_after_drawdown_gives_zero_drawdown(self) -> None:
        result = _build_drawdowns(self.drawdown_then_new_high)
        assert result[2].drawdown_percent == pytest.approx(0.0)
        assert result[2].peak_equity == pytest.approx(1100.0)

    def test_drawdown_is_relative_to_running_peak_not_start(self) -> None:
        # After reaching 1200, a drop to 900 is -25% from peak, not -10% from start
        result = _build_drawdowns(self.multiple_peaks)
        assert result[2].peak_equity == pytest.approx(1200.0)
        assert result[2].drawdown_percent == pytest.approx(-0.25)

    def test_timestamps_are_preserved(self) -> None:
        result = _build_drawdowns(self.monotonic_gain)
        assert result[0].timestamp == 1704067200000
        assert result[1].timestamp == 1704153600000
        assert result[2].timestamp == 1704240000000
