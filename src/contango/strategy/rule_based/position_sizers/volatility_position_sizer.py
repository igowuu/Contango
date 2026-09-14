from __future__ import annotations

import math

from contango.strategy.rule_based.position_sizers.position_sizer import PositionSizer
from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.stream.indicators.calculations.average_true_range import AverageTrueRange
from contango.trading.execution.engine.events.types import MarketDataEvent


class VolatilityPositionSizer(PositionSizer[TradingContext]):
    """
    Sizes positions inversely to volatility.
    """
    def __init__(
        self,
        vol_indicator: AverageTrueRange,
        target_vol: float,
        periods_per_year: int = 252,
    ) -> None:
        """
        Initializes `VolatilityPositionSizer`.

        Args:
            vol_indicator: An indicator producing the periodic return volatility.
            target_vol: The desired annualized volatility contribution of a full position.
            periods_per_year: The number of periods per year, used to annualize the indicator's per-period volatility.
        """
        self._vol_indicator = vol_indicator
        self._target_vol = target_vol
        self._periods_per_year = periods_per_year

    def update(self, event: MarketDataEvent) -> None:
        self._vol_indicator.update(event)

    def size(self, context: TradingContext) -> int:
        """
        Returns units sized so the position's annualized volatility = target_vol.
        """
        atr = self._vol_indicator.value
        price = context.event.close

        if atr is None or atr <= 0 or price <= 0:
            return 0

        periodic_vol = atr / price
        annualized_vol = periodic_vol * math.sqrt(self._periods_per_year)
        equity = context.portfolio.equity

        if equity is None:
            return 0

        dollar_exposure = (self._target_vol / annualized_vol) * equity
        return int(dollar_exposure / price)

    def __str__(self) -> str:
        return f"VolSizer(target_vol={self._target_vol})"
