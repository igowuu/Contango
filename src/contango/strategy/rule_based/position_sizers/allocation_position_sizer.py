from __future__ import annotations

from contango.strategy.rule_based.position_sizers.position_sizer import PositionSizer
from contango.strategy.rule_based.contexts.trading_context import TradingContext


class AllocationPositionSizer(PositionSizer[TradingContext]):
    """
    A position sizer with an allocation of the portfolio cash.
    """
    def __init__(self, allocation: float) -> None:
        """
        Initializes `FixedPositionSizer.
        
        Args:
            allocation: The allocation of the portfolio cash to trade.
        """
        self._allocation = allocation

    def size(self, context: TradingContext) -> int:
        """
        Returns the allocation percent of the portfolio cash (converted to units).
        """
        cash = context.portfolio.cash * self._allocation

        if context.event.close == 0.0:
            return 0

        units = int(cash / context.event.close)
        return units

    def __str__(self) -> str:
        return f"AllocSizer({self._allocation})"
