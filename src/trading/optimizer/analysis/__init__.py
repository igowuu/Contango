# trading/optimizer/analysis/__init__.py — part of Contango, a parameterized backtesting & execution framework
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

# SPDX-FileCopyrightText: 2026 Jacob Taylor
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

from trading.optimizer.analysis.builder import build_context
from trading.optimizer.analysis.calculate_metrics import calculate_metrics
from trading.optimizer.analysis.context import AnalysisContext, TradePoint, EquityPoint, ReturnPoint, DrawdownPoint
from trading.optimizer.analysis.metrics import Metrics, RiskMetrics, TradeMetrics, ReturnMetrics, DrawdownMetrics


__all__ = [
    'build_context', 'calculate_metrics',
    'AnalysisContext', 'TradePoint', 'EquityPoint', 'ReturnPoint', 'DrawdownPoint',
    'Metrics', 'RiskMetrics', 'TradeMetrics', 'ReturnMetrics', 'DrawdownMetrics'
]
