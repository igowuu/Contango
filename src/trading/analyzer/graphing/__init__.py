# trading/analyzer/graphing/__init__.py — part of Contango, a parameterized backtesting & execution framework
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

from __future__ import annotations

from trading.analyzer.graphing.risk_return_overview import build_risk_return_overview
from trading.analyzer.graphing.parameter_importance import build_parameter_importance, compute_parameter_importance
from trading.analyzer.graphing.parallel_coordinates import build_parallel_coordinates
from trading.analyzer.graphing.pairwise_heatmap_grid import build_pairwise_heatmap_grid
from trading.analyzer.graphing.metric_distribution import build_metric_distribution
from trading.analyzer.graphing.equity_curve_overlay import build_equity_curve_overlay
from trading.analyzer.graphing.underwater_drawdown import build_underwater_plot
from trading.analyzer.graphing.trade_quality_scatter import build_trade_quality_scatter
from trading.analyzer.graphing.final_comparison_radar import build_final_comparison_radar


__all__ = [
    'build_risk_return_overview', 'build_parameter_importance', 'compute_parameter_importance',
    'build_parallel_coordinates', 'build_pairwise_heatmap_grid', 'build_metric_distribution',
    'build_equity_curve_overlay', 'build_underwater_plot', 'build_trade_quality_scatter', 'build_final_comparison_radar'
]
