from __future__ import annotations

from typing import Any, Sequence, final

from contango.strategy.strategy import Strategy

from contango.stream.stream import Stream

from contango.trading.execution.engine.events.types import MarketDataEvent

from contango.strategy.rule_based.rules.rule import Rule
from contango.strategy.rule_based.contexts.trading_context import TradingContext
from contango.strategy.rule_based.intents.intent import Intent
from contango.strategy.rule_based.intents.enter_long_intent import EnterLongIntent
from contango.strategy.rule_based.intents.exit_long_intent import ExitLongIntent
from contango.strategy.rule_based.position_sizers.position_sizer import PositionSizer


class RuleBasedStrategy(Strategy):
    """
    Allows rules to be executed upon and intents to be executed.
    """
    def __init__(
        self,
        streams: Sequence[Stream[Any]],
        rules: Sequence[Rule[TradingContext, Intent | None]],
        position_sizer: PositionSizer[TradingContext],
    ) -> None:
        """
        Initializes `RuleBasedStrategy`.
        
        Args:
            streams: A list of streams to be updated with context every market data event.
            rules: A sequence of rules, where each rule returns their intent type or None (executed in order).
            position_sizer: The sizing rule for all trades made.
        """
        self._streams = streams
        self._rules = rules
        self._position_sizer = position_sizer
        self._last_event: MarketDataEvent | None = None

    @final
    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Updates all streams, executes rules, and executes intents every event.
        """
        self._last_event = event

        for stream in self._streams:
            stream.update(event)
        self._position_sizer.update(event)

        context = TradingContext(
            event=event,
            portfolio=self.portfolio_snapshot,
        )

        for rule in self._rules:
            intent = rule.evaluate(context)
            if intent is not None:
                self._translate(intent, context)

    @final
    def _translate(self, intent: Intent, context: TradingContext) -> None:
        """
        Executes the provided intent type.
        
        Raises:
            RuntimeError: Upon an unhandled intent.
        """
        match intent:
            case EnterLongIntent(symbol=symbol):
                size = self._position_sizer.size(context)
                self.order_api.submit_order(context.event, symbol, size)
            case ExitLongIntent(symbol=symbol):
                size = self.portfolio_snapshot.position
                if size > 0:
                    self.order_api.submit_order(context.event, symbol, -size)
            case _:
                raise RuntimeError(f"Unhandled intent in RuleBasedStrategy: {intent}")

    @final
    def on_end(self) -> None:
        """
        Closes any open long position at the final market event.
        """
        final_event = self._last_event

        if final_event is None:
            raise ValueError("The final market data event was never set.")

        size = self.portfolio_snapshot.position
        if size > 0:
            self.order_api.submit_order(final_event, final_event.symbol, -size)
