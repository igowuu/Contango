from __future__ import annotations

from typing import Sequence

from contango.strategy.rule_based.rule_based_strategy import RuleBasedStrategy
from contango.strategy.rule_based.rules.rule import Rule
from contango.strategy.rule_based.conditions.predicate import Predicate
from contango.strategy.rule_based.actions.emit import Emit
from contango.strategy.rule_based.intents.enter_long_intent import EnterLongIntent
from contango.strategy.rule_based.intents.exit_long_intent import ExitLongIntent
from contango.strategy.rule_based.position_sizers.allocation_position_sizer import AllocationPositionSizer
from contango.stream.indicators.calculations.bollinger_bands import BollingerBands
from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.strategy.rule_based.intents.intent import Intent
from contango.stream.indicators.historical_indicator import HistoricalIndicator
from contango.stream.historical_market_events import HistoricalMarketEvents


class BollingerBandMeanReversion(RuleBasedStrategy):
    def __init__(
        self, 
        bollinger_bands_period: int, 
        bollinger_bands_stdev: float,
        allocation: float,
        symbol: str
    ) -> None:
        self.bollinger = HistoricalIndicator(
            source=BollingerBands(
                bollinger_bands_period, 
                bollinger_bands_stdev
            ), 
            window=2
        )
        self.events = HistoricalMarketEvents(window=2)

        rules: Sequence[Rule[TradingContext, Intent]] = [
            Rule(
                when=Predicate(self.price_crosses_below_lower_band),
                then=Emit(EnterLongIntent(symbol=symbol))
            ),
            Rule(
                when=Predicate(self.price_crosses_above_middle_band),
                then=Emit(ExitLongIntent(symbol=symbol)),
            )
        ]

        super().__init__(
            streams=[self.bollinger, self.events],
            rules=rules,
            position_sizer=AllocationPositionSizer(allocation),
        )

    def price_crosses_below_lower_band(self, context: TradingContext) -> bool:
        current_bb, prev_bb = self.bollinger.value, self.bollinger.previous()
        current_event, prev_event = context.event, self.events.previous()

        if current_bb is None or prev_bb is None or prev_event is None:
            return False

        return prev_event.close >= prev_bb.lower and current_event.close < current_bb.lower

    def price_crosses_above_middle_band(self, context: TradingContext) -> bool:
        current_bb, prev_bb = self.bollinger.value, self.bollinger.previous()
        current_event, prev_event = context.event, self.events.previous()

        if current_bb is None or prev_bb is None or prev_event is None:
            return False

        return prev_event.close <= prev_bb.middle and current_event.close > current_bb.middle
