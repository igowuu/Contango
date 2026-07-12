from __future__ import annotations

from execution.engine import Strategy, MarketDataEvent

from research.methods.calculations.ema import EMA
from research.methods.state.ema_state import EMAState


class EMADoubleCrossover(Strategy):
    """
    Simple EMA double crossover strategy.

    Rules:
        Position size is based on portfolio value.
        Buys when the fast EMA is above the slow EMA.
        Sells when the fast EMA is below the slow EMA.
    """
    def __init__(self, fast_ema_days: int, slow_ema_days: int, allocation: float) -> None:
        """
        Initializes `EMADoubleCrossover`.

        Args:
            fast_ema_days: The period for the fast EMA.
            slow_ema_days: The period for the slow EMA.
            allocation: The percent of the portfolio cash traded.
        """
        self._fast_ema = EMA(fast_ema_days)
        self._slow_ema = EMA(slow_ema_days)

        self._allocation = allocation

        self._prev_state: EMAState | None = None
        self._prev_event: MarketDataEvent | None = None

    def _should_buy(self, previous: EMAState, current: EMAState) -> bool:
        """
        Returns true upon the fast ema crossing above the slow ema & not already being in a position.
        """
        return (
            previous == EMAState.BELOW 
            and current == EMAState.ABOVE
            and not self._holding
        )
    
    def _should_sell(self, previous: EMAState, current: EMAState) -> bool:
        """
        Returns true upon the fast ema crossing below the slow ema & already being in a position.
        """
        return (
            previous == EMAState.ABOVE 
            and current == EMAState.BELOW
            and self._holding
        )
    
    @property
    def _holding(self) -> bool:
        """
        Returns True if currently in a position (units held above zero).
        """
        return self.portfolio_snapshot.position > 0

    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Buys upon an EMA crossover up, sells upon an EMA crossover down.
        """
        fast_ema = self._fast_ema.update(event.close)
        slow_ema = self._slow_ema.update(event.close)

        state = EMAState.get_state(fast_ema, slow_ema)

        # First valid state
        if self._prev_state is None:
            self._prev_state = state
            return

        # Crossover below -> above
        if self._should_buy(self._prev_state, state):
            quantity = int((self._allocation * self.portfolio_snapshot.cash) / event.close)
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=quantity,
                reason="EMA bullish crossover"
            )

        # Crossover above -> below
        elif self._should_sell(self._prev_state, state):
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="EMA bearish crossover"
            )

        self._prev_state = state
        self._prev_event = event

    def on_end(self) -> None:
        """
        Sells any orders that still exist.
        """
        if self._prev_event is None:
            raise RuntimeError("Previous event was never set.")

        if self._holding:
            self.order_api.submit_order(
                market_data=self._prev_event,
                symbol=self._prev_event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="Sold all remaining shares at the end of the strategy."
            )
