# trading/optimizer/analysis/calculate_metrics.py — part of Contango, a parameterized backtesting & execution framework
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

from contango.trading.execution.engine import ExecutionData

from contango.trading.optimizer.analysis.builder import build_context
from contango.trading.optimizer.analysis.calculators.returns import get_return_metrics
from contango.trading.optimizer.analysis.calculators.risk import get_risk_metrics
from contango.trading.optimizer.analysis.calculators.drawdown import get_drawdown_metrics
from contango.trading.optimizer.analysis.calculators.trades import get_trade_metrics
from contango.trading.optimizer.analysis.metrics import Metrics


def calculate_metrics(data: ExecutionData) -> Metrics:
    """
    Calculates readable metrics for backtest data.
    
    Args:
        data: The backtest data to derive metrics from.
    
    Returns:
        Metrics: A metrics object representing returns, drawdown, risks, and trade information about the strategy.
    """
    analysis_context = build_context(data)
    return_metrics = get_return_metrics(analysis_context)
    drawdown_metrics = get_drawdown_metrics(analysis_context)
    risk_metrics = get_risk_metrics(analysis_context, return_metrics.monthly_returns, drawdown_metrics.max_drawdown)
    trade_metrics = get_trade_metrics(analysis_context)
    return Metrics(
        returns=return_metrics,
        risk=risk_metrics,
        drawdowns=drawdown_metrics,
        trades=trade_metrics
    )
