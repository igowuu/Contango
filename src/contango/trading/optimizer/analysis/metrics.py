# trading/optimizer/analysis/metrics.py — part of Contango, a parameterized backtesting & execution framework
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

from typing import NamedTuple


percent = float
USD = float
time_unix_ms = int


class Metrics(NamedTuple):
    """
    The metrics of a single backtest, used to identify the effectiveness of a strategy.
    
    Attributes:
        returns: The return (cash, units) metrics for the strategy.
        risk: The risk (reliability) metrics for the strategy.
        drawdowns: The drawdown (losses) metrics for the strategy.
        trades: The number of trades made, losses, wins, profits, etc.
    """
    returns: ReturnMetrics
    risk: RiskMetrics
    drawdowns: DrawdownMetrics
    trades: TradeMetrics

    def __repr__(self) -> str:
        """
        Returns a string representation of the metrics.
        """
        def fmt_f(val: float | None) -> str:
            return f"{val:.2f}" if val is not None else "N/A"

        return (
            "Backtest Metrics:\n"
            f"  Total Return: {fmt_f(self.returns.total_return)}\n"
            f"  Annual Return: {fmt_f(self.risk.annual_return)}\n"
            f"  Volatility: {fmt_f(self.risk.monthly_volatility)}\n"
            f"  Sharpe Ratio: {fmt_f(self.risk.sharpe_ratio)}\n"
            f"  Calmar Ratio: {fmt_f(self.risk.calmar_ratio)}\n"
            f"  Max Drawdown: {fmt_f(self.drawdowns.max_drawdown)}\n"
            f"  Average Drawdown: {fmt_f(self.drawdowns.average_drawdown)}\n"
            f"  Trades: {self.trades.trade_count}\n"
            f"  Win Rate: {fmt_f(self.trades.win_rate)}\n"
            f"  Profit Factor: {fmt_f(self.trades.profit_factor)}\n"
            f"  Expectancy: {fmt_f(self.trades.expectancy)}\n"
            f"  Average Holding Period: {fmt_f(self.trades.average_holding_period)}"
        )


class ReturnMetrics(NamedTuple):
    """
    The resulting returns from the backtest.
    Holds the actual returned property and value from a strategy over time.

    Attributes:
        total_return: The percent returned from the backtest at the end of execution.
        monthly_returns: A sequence of the total returns per month of the strategy.
        equity_curve: The account value over time (total value of cash + units).
    """
    total_return: percent | None
    monthly_returns: tuple[tuple[time_unix_ms, percent], ...] | None
    equity_curve: tuple[tuple[time_unix_ms, USD], ...]


class RiskMetrics(NamedTuple):
    """
    The risk factor metrics from a backtest.
    Determines how reliable a strategy was over the backtest.

    Attributes:
        annual_return: The CAGR (annualized compound return) for the backtest.
        monthly_volatility: Measure of how intensely returns move per month.
        sharpe_ratio: Measure of how much excess return received per unit of risk taken (annaul).
        calmar_ratio: Measure of much return an investment has generated relative to its worst possible loss.
    """
    annual_return: percent | None
    monthly_volatility: percent | None
    sharpe_ratio: float | None
    calmar_ratio: float | None


class DrawdownMetrics(NamedTuple):
    """
    The drawdown metrics for a backtest.
    Holds the worst possible risk and volatility of a strategy.
    
    Attributes:
        max_drawdown: The worst single historical loss of the strategy.
        average_drawdown: The average of historical losses of the strategy.
    """
    max_drawdown: percent | None
    average_drawdown: percent | None


class TradeMetrics(NamedTuple):
    """
    The basic trading metrics for a backtest.
    Holds the actual number of trades made, wins, losses, and profits.
    
    Attrubtes:
        trade_count: The total number of trades the strategy made during the backtest.
        win_rate: The percent of trades that the strategy was profitable.
        profit_factor: The gross profit from winning trades to gross losses from losing trades.
        expectancy: The expected profit per trade with the strategy.
        average_win: The average percent made per win.
        average_loss: The average percent lost per loss.
        average_holding_period: The average amount of time that the strategy holds a trade for.
    """
    trade_count: int
    win_rate: percent | None
    profit_factor: float | None
    expectancy: percent | None
    average_win: percent | None
    average_loss: percent | None
    average_holding_period: time_unix_ms | None
