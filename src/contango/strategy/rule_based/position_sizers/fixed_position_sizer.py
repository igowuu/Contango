from __future__ import annotations

from contango.strategy.rule_based.position_sizers.position_sizer import PositionSizer
from contango.strategy.rule_based.contexts.trading_context import TradingContext


class FixedPositionSizer(PositionSizer[TradingContext]):
    """
    A position sizer with a fixed amount of units.
    """
    def __init__(self, fixed_units: int) -> None:
        """
        Initializes `FixedPositionSizer.
        
        Args:
            fixed_units: The unchanging amount of units to order for every trade.
        """
        self._fixed_units = fixed_units

    def size(self, context: TradingContext) -> int:
        """
        Returns the fixed size set during initialization.
        """
        return self._fixed_units

    def __str__(self) -> str:
        return f"FixedSizer({self._fixed_units})"
