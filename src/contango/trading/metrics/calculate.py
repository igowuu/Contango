from __future__ import annotations

from contango.trading.execution.engine import ExecutionData

from contango.trading.metrics.builder import build_context
from contango.trading.metrics.calculators.returns import get_return_metrics
from contango.trading.metrics.calculators.risk import get_risk_metrics
from contango.trading.metrics.calculators.drawdown import get_drawdown_metrics
from contango.trading.metrics.calculators.trades import get_trade_metrics
from contango.trading.metrics.metrics import Metrics


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
