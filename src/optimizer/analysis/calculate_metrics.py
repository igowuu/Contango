from __future__ import annotations

from execution.engine import ExecutionData

from optimizer.analysis.builder import build_context
from optimizer.analysis.calculators.returns import get_return_metrics
from optimizer.analysis.calculators.risk import get_risk_metrics
from optimizer.analysis.calculators.drawdown import get_drawdown_metrics
from optimizer.analysis.calculators.trades import get_trade_metrics
from optimizer.analysis.metrics import Metrics


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
