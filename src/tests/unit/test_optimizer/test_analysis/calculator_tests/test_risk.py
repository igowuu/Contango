# pyright: reportPrivateUsage=false

import pytest

from optimizer.analysis.context import EquityPoint
from optimizer.analysis.calculators.risk import (
    _get_annual_return,
    _get_calmar_ratio,
    _get_monthly_volatility,
    _get_sharpe_ratio,
)


def make_monthly_returns(*percents: float) -> tuple[tuple[int, float], ...]:
    """Helper to build monthly return tuples with dummy timestamps."""
    return tuple((i, p) for i, p in enumerate(percents))


class TestGetMonthlyVolatility:
    """
    Logic & regression tests for the `_get_monthly_volatility` method.

    Expected: The method returns the monthly standard deviation of the provided
    monthly returns. Returns None when input is None or fewer than 2 data points.
    """
    def setup_method(self) -> None:
        self.identical_returns = make_monthly_returns(0.10, 0.10, 0.10)
        self.varying_returns = make_monthly_returns(0.10, -0.10, 0.20, -0.20)
        self.single_return = make_monthly_returns(0.10)
        self.two_returns = make_monthly_returns(0.10, 0.20)

    def test_identical_returns_gives_zero_volatility(self) -> None:
        result = _get_monthly_volatility(self.identical_returns)
        assert result == pytest.approx(0.0)

    def test_varying_returns_gives_nonzero_volatility(self) -> None:
        result = _get_monthly_volatility(self.varying_returns)
        assert result is not None
        assert result > 0.0

    def test_single_return_returns_none(self) -> None:
        result = _get_monthly_volatility(self.single_return)
        assert result is None

    def test_empty_input_returns_none(self) -> None:
        result = _get_monthly_volatility(())
        assert result is None

    def test_none_input_returns_none(self) -> None:
        result = _get_monthly_volatility(None)
        assert result is None

    def test_two_returns_gives_nonzero_volatility(self) -> None:
        result = _get_monthly_volatility(self.two_returns)
        assert result == pytest.approx(0.0707, rel=1e-2)


class TestGetSharpeRatio:
    """
    Logic & regression tests for the `_get_sharpe_ratio` method.

    Expected: The method returns mean(monthly_returns) / monthly_volatility * sqrt(12).
    Returns None when input is None, fewer than 2 returns, or volatility is None or zero.
    """
    def setup_method(self) -> None:
        self.positive_returns = make_monthly_returns(0.10, 0.20, 0.15)
        self.negative_returns = make_monthly_returns(-0.10, -0.20, -0.15)
        self.mixed_returns = make_monthly_returns(0.10, -0.10, 0.20, -0.20)
        self.single_return = make_monthly_returns(0.10)

    def test_positive_returns_gives_positive_sharpe(self) -> None:
        result = _get_sharpe_ratio(self.positive_returns, monthly_volatility=0.05)
        assert result is not None
        assert result > 0.0

    def test_negative_returns_gives_negative_sharpe(self) -> None:
        result = _get_sharpe_ratio(self.negative_returns, monthly_volatility=0.05)
        assert result is not None
        assert result < 0.0

    def test_zero_mean_returns_zero_sharpe(self) -> None:
        result = _get_sharpe_ratio(self.mixed_returns, monthly_volatility=0.05)
        assert result == pytest.approx(0.0)

    def test_zero_volatility_returns_none(self) -> None:
        result = _get_sharpe_ratio(self.positive_returns, monthly_volatility=0.0)
        assert result is None

    def test_none_volatility_returns_none(self) -> None:
        result = _get_sharpe_ratio(self.positive_returns, monthly_volatility=None)
        assert result is None

    def test_single_return_returns_none(self) -> None:
        result = _get_sharpe_ratio(self.single_return, monthly_volatility=0.05)
        assert result is None

    def test_empty_input_returns_none(self) -> None:
        result = _get_sharpe_ratio((), monthly_volatility=0.05)
        assert result is None

    def test_none_input_returns_none(self) -> None:
        result = _get_sharpe_ratio(None, monthly_volatility=0.05)
        assert result is None

    def test_known_values_match_expected(self) -> None:
        # mean = 0.10, volatility = 0.05 → sharpe = 0.10 / 0.05 * sqrt(12) ≈ 6.928
        from math import sqrt
        result = _get_sharpe_ratio(make_monthly_returns(0.10, 0.10, 0.10), monthly_volatility=0.05)
        assert result == pytest.approx(0.10 / 0.05 * sqrt(12))


class TestGetCalmarRatio:
    """
    Logic & regression tests for the `_get_calmar_ratio` method.

    Expected: The method returns annual_return / abs(max_drawdown).
    Returns None when either input is None or max_drawdown is zero.
    """
    def test_positive_annual_return_gives_positive_calmar(self) -> None:
        result = _get_calmar_ratio(annual_return=0.20, max_drawdown=-0.10)
        assert result == pytest.approx(2.0)

    def test_negative_annual_return_gives_negative_calmar(self) -> None:
        result = _get_calmar_ratio(annual_return=-0.20, max_drawdown=-0.10)
        assert result == pytest.approx(-2.0)

    def test_zero_max_drawdown_returns_none(self) -> None:
        result = _get_calmar_ratio(annual_return=0.20, max_drawdown=0.0)
        assert result is None

    def test_none_max_drawdown_returns_none(self) -> None:
        result = _get_calmar_ratio(annual_return=0.20, max_drawdown=None)
        assert result is None

    def test_none_annual_return_returns_none(self) -> None:
        result = _get_calmar_ratio(annual_return=None, max_drawdown=-0.10)
        assert result is None

    def test_zero_annual_return_gives_zero_calmar(self) -> None:
        result = _get_calmar_ratio(annual_return=0.0, max_drawdown=-0.10)
        assert result == pytest.approx(0.0)

    def test_drawdown_sign_does_not_affect_result(self) -> None:
        positive = _get_calmar_ratio(annual_return=0.20, max_drawdown=0.10)
        negative = _get_calmar_ratio(annual_return=0.20, max_drawdown=-0.10)
        assert positive == pytest.approx(negative)


class TestGetAnnualReturn:
    """
    Logic & regression tests for the `_get_annual_return` method.

    Expected: The method returns the CAGR over the full duration of the equity curve.
    Returns None when fewer than 2 points are provided, duration is zero, or
    initial equity is non-positive.
    """
    def setup_method(self) -> None:
        self.one_year_gain = (
            EquityPoint(1672531200000, 1000.0),  # 2023-01-01
            EquityPoint(1704067200000, 1100.0),  # 2024-01-01
        )
        self.one_year_loss = (
            EquityPoint(1672531200000, 1000.0),
            EquityPoint(1704067200000, 900.0),
        )
        self.two_year_gain = (
            EquityPoint(1640995200000, 1000.0),  # 2022-01-01
            EquityPoint(1704067200000, 1210.0),  # 2024-01-01
        )
        self.same_timestamp = (
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704067200000, 1100.0),
        )
        self.multi_point = (
            EquityPoint(1640995200000, 1000.0),  # 2022-01-01
            EquityPoint(1654041600000, 800.0),   # 2022-06-01
            EquityPoint(1685577600000, 1300.0),  # 2023-06-01
            EquityPoint(1704067200000, 1210.0),  # 2024-01-01
        )

    def test_one_year_gain_returns_correct_cagr(self) -> None:
        result = _get_annual_return(self.one_year_gain)
        assert result == pytest.approx(0.10, rel=1e-2)

    def test_one_year_loss_returns_negative_cagr(self) -> None:
        result = _get_annual_return(self.one_year_loss)
        assert result == pytest.approx(-0.10, rel=1e-2)

    def test_two_year_gain_compounds_correctly(self) -> None:
        # 1000 → 1210 over 2 years: CAGR = (1210/1000)^(1/2) - 1 = 0.10
        result = _get_annual_return(self.two_year_gain)
        assert result == pytest.approx(0.10, rel=1e-2)

    def test_same_timestamp_returns_none(self) -> None:
        result = _get_annual_return(self.same_timestamp)
        assert result is None

    def test_single_point_returns_none(self) -> None:
        result = _get_annual_return((EquityPoint(1704067200000, 1000.0),))
        assert result is None

    def test_empty_input_returns_none(self) -> None:
        result = _get_annual_return(())
        assert result is None

    def test_zero_initial_equity_returns_none(self) -> None:
        result = _get_annual_return((
            EquityPoint(1672531200000, 0.0),
            EquityPoint(1704067200000, 1000.0),
        ))
        assert result is None

    def test_only_first_and_last_points_matter(self) -> None:
        result = _get_annual_return(self.multi_point)
        assert result == pytest.approx(
            _get_annual_return((self.multi_point[0], self.multi_point[-1]))
        )
    
    def test_sub_day_duration_returns_none(self) -> None:
        result = _get_annual_return((
            EquityPoint(1704067200000, 1000.0),
            EquityPoint(1704067200000 + 3_600_000, 1100.0),  # 1 hour later
        ))
        assert result is None
