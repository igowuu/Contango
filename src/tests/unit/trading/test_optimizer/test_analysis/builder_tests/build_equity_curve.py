# tests/unit/trading/test_optimizer/test_analysis/builder_tests/build_equity_curve.py — part of Contango, a parameterized backtesting & execution framework
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

from trading.execution.engine import PortfolioSnapshotEvent, ExecutionData

from trading.optimizer.analysis.context import EquityPoint
from trading.optimizer.analysis.builder import _build_equity_curve


class TestBuildEquityCurve:
    """
    Logic & regression tests for the `_build_equity_curve` function.

    Expected: Builds a chronological sequence of EquityPoints from portfolio
    snapshot events, skipping any snapshots where equity is None.
    """
    def setup_method(self) -> None:
        self.single_snapshot = self._make_data([
            (1704067200000, 1000.0),
        ])
        self.multiple_snapshots = self._make_data([
            (1704067200000, 1000.0),
            (1704153600000, 1100.0),
            (1704240000000, 1050.0),
        ])
        self.leading_none = self._make_data([
            (1704067200000, None),
            (1704153600000, 1000.0),
            (1704240000000, 1100.0),
        ])
        self.mixed_nones = self._make_data([
            (1704067200000, None),
            (1704153600000, 1000.0),
            (1704240000000, None),
            (1704326400000, 1100.0),
        ])
        self.all_nones = self._make_data([
            (1704067200000, None),
            (1704153600000, None),
        ])

    def _make_snapshot(self, timestamp: int, equity: float | None):
        s = PortfolioSnapshotEvent(
            timestamp=timestamp,
            cash=0.0,
            position=0,
            equity=equity
        )
        return s

    def _make_data(self, snapshots: list[tuple[int, float | None]]):
        d = ExecutionData(
            accepted_fill_events=(),
            rejected_fill_events=(),
            order_events=(),
            market_data_events=(),
            initial_portfolio_snapshot_event=PortfolioSnapshotEvent(0, 0, 0, 0),
            portfolio_snapshot_events=tuple(self._make_snapshot(ts, eq) for ts, eq in snapshots)
        )
        return d

    def test_single_snapshot_returns_single_point(self) -> None:
        result = _build_equity_curve(self.single_snapshot)
        assert len(result) == 1
        assert result[0] == EquityPoint(1704067200000, 1000.0)

    def test_multiple_snapshots_returns_all_points(self) -> None:
        result = _build_equity_curve(self.multiple_snapshots)
        assert len(result) == 3
        assert result[0] == EquityPoint(1704067200000, 1000.0)
        assert result[1] == EquityPoint(1704153600000, 1100.0)
        assert result[2] == EquityPoint(1704240000000, 1050.0)

    def test_leading_none_snapshot_is_skipped(self) -> None:
        result = _build_equity_curve(self.leading_none)
        assert len(result) == 2
        assert result[0].timestamp == 1704153600000

    def test_none_snapshots_in_middle_are_skipped(self) -> None:
        result = _build_equity_curve(self.mixed_nones)
        assert len(result) == 2
        assert result[0] == EquityPoint(1704153600000, 1000.0)
        assert result[1] == EquityPoint(1704326400000, 1100.0)

    def test_all_none_snapshots_returns_empty(self) -> None:
        result = _build_equity_curve(self.all_nones)
        assert result == ()

    def test_empty_snapshots_returns_empty(self) -> None:
        result = _build_equity_curve(self._make_data([]))
        assert result == ()

    def test_ordering_is_preserved(self) -> None:
        result = _build_equity_curve(self.multiple_snapshots)
        timestamps = [p.timestamp for p in result]
        assert timestamps == sorted(timestamps)
