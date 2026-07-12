# pyright: reportPrivateUsage=false

import pytest

from optimizer.analysis.context import TradePoint
from optimizer.analysis.calculators.trades import (
    _get_average_holding_period,
    _get_average_loss,
    _get_average_win,
    _get_expectancy,
    _get_profit_factor,
    _get_trade_count,
    _get_trade_returns,
    _get_win_rate,
)

ONE_DAY_MS = 86_400_000


class TestGetTradeReturns:
    """
    Logic & regression tests for the `_get_trade_returns` method.

    Expected: The method returns a tuple of percent returns per trade,
    calculated as (exit_price - entry_price) / entry_price. Returns None
    for empty input.
    """
    def setup_method(self) -> None:
        self.single_win = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
        )
        self.single_loss = (
            self._make_trade(entry_price=100.0, exit_price=90.0),
        )
        self.mixed = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=90.0),
            self._make_trade(entry_price=200.0, exit_price=250.0),
        )
        self.breakeven = (
            self._make_trade(entry_price=100.0, exit_price=100.0),
        )

    def _make_trade(
        self,
        entry_price: float = 100.0,
        exit_price: float = 110.0,
        quantity: int = 1,
        entry_time: int = 1704067200000,
        exit_time: int = 1704153600000,
    ) -> TradePoint:
        return TradePoint(
            entry_time=entry_time,
            exit_time=exit_time,
            entry_price=entry_price,
            exit_price=exit_price,
            quantity=quantity,
        )

    def test_single_win_returns_positive_percent(self) -> None:
        result = _get_trade_returns(self.single_win)
        assert result == pytest.approx((0.10,))

    def test_single_loss_returns_negative_percent(self) -> None:
        result = _get_trade_returns(self.single_loss)
        assert result == pytest.approx((-0.10,))

    def test_mixed_trades_returns_all_percents(self) -> None:
        result = _get_trade_returns(self.mixed)
        assert result == pytest.approx((0.10, -0.10, 0.25))

    def test_breakeven_trade_returns_zero(self) -> None:
        result = _get_trade_returns(self.breakeven)
        assert result == pytest.approx((0.0,))

    def test_empty_input_returns_none(self) -> None:
        result = _get_trade_returns(())
        assert result is None


class TestGetTradeCount:
    """
    Logic & regression tests for the `_get_trade_count` method.

    Expected: The method returns the number of trades in the tuple.
    """
    def setup_method(self) -> None:
        self.single = (self._make_trade(),)
        self.multiple = (self._make_trade(), self._make_trade(), self._make_trade())

    def _make_trade(self) -> TradePoint:
        return TradePoint(
            entry_time=1704067200000,
            exit_time=1704153600000,
            entry_price=100.0,
            exit_price=110.0,
            quantity=1,
        )

    def test_empty_input_returns_zero(self) -> None:
        result = _get_trade_count(())
        assert result == 0

    def test_single_trade_returns_one(self) -> None:
        result = _get_trade_count(self.single)
        assert result == 1

    def test_multiple_trades_returns_correct_count(self) -> None:
        result = _get_trade_count(self.multiple)
        assert result == 3


class TestGetWinRate:
    """
    Logic & regression tests for the `_get_win_rate` method.

    Expected: The method returns the fraction of trades where exit_price > entry_price.
    Returns None for empty input.
    """
    def setup_method(self) -> None:
        self.all_wins = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=120.0),
        )
        self.all_losses = (
            self._make_trade(entry_price=100.0, exit_price=90.0),
            self._make_trade(entry_price=100.0, exit_price=80.0),
        )
        self.mixed = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=90.0),
            self._make_trade(entry_price=100.0, exit_price=120.0),
            self._make_trade(entry_price=100.0, exit_price=80.0),
        )
        self.with_breakeven = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=100.0),
            self._make_trade(entry_price=100.0, exit_price=90.0),
        )

    def _make_trade(self, entry_price: float = 100.0, exit_price: float = 110.0) -> TradePoint:
        return TradePoint(
            entry_time=1704067200000,
            exit_time=1704153600000,
            entry_price=entry_price,
            exit_price=exit_price,
            quantity=1,
        )

    def test_all_wins_returns_one(self) -> None:
        result = _get_win_rate(self.all_wins)
        assert result == pytest.approx(1.0)

    def test_all_losses_returns_zero(self) -> None:
        result = _get_win_rate(self.all_losses)
        assert result == pytest.approx(0.0)

    def test_mixed_returns_correct_rate(self) -> None:
        result = _get_win_rate(self.mixed)
        assert result == pytest.approx(0.50)

    def test_breakeven_trades_not_counted_as_wins(self) -> None:
        result = _get_win_rate(self.with_breakeven)
        assert result == pytest.approx(1/3)

    def test_empty_input_returns_none(self) -> None:
        result = _get_win_rate(())
        assert result is None


class TestGetProfitFactor:
    """
    Logic & regression tests for the `_get_profit_factor` method.

    Expected: The method returns gross_profit / gross_loss weighted by quantity.
    Returns None for empty input or when there are no losses.
    """
    def setup_method(self) -> None:
        self.all_wins = (
            self._make_trade(entry_price=100.0, exit_price=110.0, quantity=1),
            self._make_trade(entry_price=100.0, exit_price=120.0, quantity=1),
        )
        self.all_losses = (
            self._make_trade(entry_price=100.0, exit_price=90.0, quantity=1),
            self._make_trade(entry_price=100.0, exit_price=80.0, quantity=1),
        )
        self.mixed_equal = (
            self._make_trade(entry_price=100.0, exit_price=110.0, quantity=1),
            self._make_trade(entry_price=100.0, exit_price=90.0, quantity=1),
        )
        self.quantity_weighted = (
            self._make_trade(entry_price=100.0, exit_price=110.0, quantity=3),
            self._make_trade(entry_price=100.0, exit_price=90.0, quantity=1),
        )

    def _make_trade(self, entry_price: float, exit_price: float, quantity: int) -> TradePoint:
        return TradePoint(
            entry_time=1704067200000,
            exit_time=1704153600000,
            entry_price=entry_price,
            exit_price=exit_price,
            quantity=quantity,
        )

    def test_all_wins_no_losses_returns_none(self) -> None:
        result = _get_profit_factor(self.all_wins)
        assert result is None

    def test_all_losses_returns_zero_profit_factor(self) -> None:
        result = _get_profit_factor(self.all_losses)
        assert result == pytest.approx(0.0)

    def test_equal_profit_and_loss_returns_one(self) -> None:
        result = _get_profit_factor(self.mixed_equal)
        assert result == pytest.approx(1.0)

    def test_quantity_is_factored_into_result(self) -> None:
        # profit: 10 * 3 = 30, loss: 10 * 1 = 10 → profit factor = 3.0
        result = _get_profit_factor(self.quantity_weighted)
        assert result == pytest.approx(3.0)

    def test_empty_input_returns_none(self) -> None:
        result = _get_profit_factor(())
        assert result is None


class TestGetExpectancy:
    """
    Logic & regression tests for the `_get_expectancy` method.

    Expected: The method returns (win_rate * avg_win) - (loss_rate * avg_loss).
    Returns None for empty input.
    """
    def setup_method(self) -> None:
        self.all_wins = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=120.0),
        )
        self.all_losses = (
            self._make_trade(entry_price=100.0, exit_price=90.0),
            self._make_trade(entry_price=100.0, exit_price=80.0),
        )
        self.mixed_equal = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=90.0),
        )
        self.positive_edge = (
            self._make_trade(entry_price=100.0, exit_price=120.0),
            self._make_trade(entry_price=100.0, exit_price=120.0),
            self._make_trade(entry_price=100.0, exit_price=90.0),
        )

    def _make_trade(self, entry_price: float = 100.0, exit_price: float = 110.0) -> TradePoint:
        return TradePoint(
            entry_time=1704067200000,
            exit_time=1704153600000,
            entry_price=entry_price,
            exit_price=exit_price,
            quantity=1,
        )

    def test_all_wins_returns_positive_expectancy(self) -> None:
        result = _get_expectancy(self.all_wins)
        assert result is not None
        assert result > 0.0

    def test_all_losses_returns_negative_expectancy(self) -> None:
        result = _get_expectancy(self.all_losses)
        assert result is not None
        assert result < 0.0

    def test_equal_wins_and_losses_returns_zero(self) -> None:
        result = _get_expectancy(self.mixed_equal)
        assert result == pytest.approx(0.0)

    def test_positive_edge_returns_positive_expectancy(self) -> None:
        # win_rate=2/3, avg_win=0.20, loss_rate=1/3, avg_loss=0.10
        # expectancy = (2/3 * 0.20) - (1/3 * 0.10) ≈ 0.10
        result = _get_expectancy(self.positive_edge)
        assert result == pytest.approx(0.10, rel=1e-3)

    def test_empty_input_returns_none(self) -> None:
        result = _get_expectancy(())
        assert result is None


class TestGetAverageWin:
    """
    Logic & regression tests for the `_get_average_win` method.

    Expected: The method returns the mean return percent across winning trades only.
    Returns None when there are no winning trades or input is empty.
    """
    def setup_method(self) -> None:
        self.all_wins = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=130.0),
        )
        self.all_losses = (
            self._make_trade(entry_price=100.0, exit_price=90.0),
            self._make_trade(entry_price=100.0, exit_price=80.0),
        )
        self.mixed = (
            self._make_trade(entry_price=100.0, exit_price=120.0),
            self._make_trade(entry_price=100.0, exit_price=90.0),
        )

    def _make_trade(self, entry_price: float = 100.0, exit_price: float = 110.0) -> TradePoint:
        return TradePoint(
            entry_time=1704067200000,
            exit_time=1704153600000,
            entry_price=entry_price,
            exit_price=exit_price,
            quantity=1,
        )

    def test_all_wins_returns_mean_return(self) -> None:
        result = _get_average_win(self.all_wins)
        assert result == pytest.approx(0.20)

    def test_all_losses_returns_none(self) -> None:
        result = _get_average_win(self.all_losses)
        assert result is None

    def test_mixed_excludes_losses(self) -> None:
        result = _get_average_win(self.mixed)
        assert result == pytest.approx(0.20)

    def test_empty_input_returns_none(self) -> None:
        result = _get_average_win(())
        assert result is None


class TestGetAverageLoss:
    """
    Logic & regression tests for the `_get_average_loss` method.

    Expected: The method returns the mean return percent across losing trades only (negative value).
    Returns None when there are no losing trades or input is empty.
    """
    def setup_method(self) -> None:
        self.all_losses = (
            self._make_trade(entry_price=100.0, exit_price=90.0),
            self._make_trade(entry_price=100.0, exit_price=70.0),
        )
        self.all_wins = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=120.0),
        )
        self.mixed = (
            self._make_trade(entry_price=100.0, exit_price=110.0),
            self._make_trade(entry_price=100.0, exit_price=80.0),
        )

    def _make_trade(self, entry_price: float = 100.0, exit_price: float = 90.0) -> TradePoint:
        return TradePoint(
            entry_time=1704067200000,
            exit_time=1704153600000,
            entry_price=entry_price,
            exit_price=exit_price,
            quantity=1,
        )

    def test_all_losses_returns_negative_mean(self) -> None:
        result = _get_average_loss(self.all_losses)
        assert result == pytest.approx(-0.20)

    def test_all_wins_returns_none(self) -> None:
        result = _get_average_loss(self.all_wins)
        assert result is None

    def test_mixed_excludes_wins(self) -> None:
        result = _get_average_loss(self.mixed)
        assert result == pytest.approx(-0.20)

    def test_empty_input_returns_none(self) -> None:
        result = _get_average_loss(())
        assert result is None


class TestGetAverageHoldingPeriod:
    """
    Logic & regression tests for the `_get_average_holding_period` method.

    Expected: The method returns the mean duration in milliseconds across all trades.
    Returns None for empty input.
    """
    def setup_method(self) -> None:
        self.single_day = (
            self._make_trade(
                entry_time=1704067200000,
                exit_time=1704067200000 + ONE_DAY_MS,
            ),
        )
        self.uniform = (
            self._make_trade(
                entry_time=1704067200000,
                exit_time=1704067200000 + 5 * ONE_DAY_MS,
            ),
            self._make_trade(
                entry_time=1706745600000,
                exit_time=1706745600000 + 5 * ONE_DAY_MS,
            ),
        )
        self.mixed_durations = (
            self._make_trade(
                entry_time=1704067200000,
                exit_time=1704067200000 + ONE_DAY_MS,
            ),
            self._make_trade(
                entry_time=1706745600000,
                exit_time=1706745600000 + 3 * ONE_DAY_MS,
            ),
        )

    def _make_trade(
        self,
        entry_time: int = 1704067200000,
        exit_time: int = 1704153600000,
    ) -> TradePoint:
        return TradePoint(
            entry_time=entry_time,
            exit_time=exit_time,
            entry_price=100.0,
            exit_price=110.0,
            quantity=1,
        )

    def test_single_trade_returns_its_duration(self) -> None:
        result = _get_average_holding_period(self.single_day)
        assert result == ONE_DAY_MS

    def test_uniform_durations_returns_that_duration(self) -> None:
        result = _get_average_holding_period(self.uniform)
        assert result == 5 * ONE_DAY_MS

    def test_mixed_durations_returns_mean(self) -> None:
        # (1 day + 3 days) / 2 = 2 days
        result = _get_average_holding_period(self.mixed_durations)
        assert result == 2 * ONE_DAY_MS

    def test_empty_input_returns_none(self) -> None:
        result = _get_average_holding_period(())
        assert result is None
