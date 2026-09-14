from __future__ import annotations

from contango.strategy.rule_based.position_sizers.fixed_position_sizer import FixedPositionSizer
from contango.strategy.rule_based.position_sizers.allocation_position_sizer import AllocationPositionSizer

from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.trading.execution.engine.events.types import MarketDataEvent, PortfolioSnapshotEvent


def _create_context(cash: float, close: float) -> TradingContext:
    return TradingContext(
        event=MarketDataEvent(1000, "AAPL", close, close, close, close, 1000),
        portfolio=PortfolioSnapshotEvent(1000, cash, 0, cash),
    )


def test_fixed_position_sizer_always_returns_the_configured_units() -> None:
    sizer = FixedPositionSizer(fixed_units=7)

    assert sizer.size(_create_context(cash=1000.0, close=50.0)) == 7
    assert sizer.size(_create_context(cash=0.0, close=1.0)) == 7


def test_allocation_position_sizer_converts_cash_allocation_to_units() -> None:
    sizer = AllocationPositionSizer(allocation=0.5)

    assert sizer.size(_create_context(cash=1000.0, close=100.0)) == 5


def test_allocation_position_sizer_truncates_fractional_units() -> None:
    sizer = AllocationPositionSizer(allocation=1.0)

    assert sizer.size(_create_context(cash=1000.0, close=99.0)) == 10


def test_allocation_position_sizer_returns_zero_when_close_is_zero() -> None:
    sizer = AllocationPositionSizer(allocation=1.0)

    assert sizer.size(_create_context(cash=1000.0, close=0.0)) == 0


def test_allocation_position_sizer_returns_zero_when_allocated_cash_below_one_unit() -> None:
    sizer = AllocationPositionSizer(allocation=0.001)

    assert sizer.size(_create_context(cash=1000.0, close=100.0)) == 0
