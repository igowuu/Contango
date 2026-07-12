from __future__ import annotations

from execution.engine import Strategy, MarketDataEvent

from research.methods.calculations.sma import SMA
from research.methods.state.sma_state import SMAState


class SMADoubleCrossover(Strategy):
    """
    Simple SMA double crossover strategy.

    Rules:
        Position size is based on portfolio value.
        Buys when the fast SMA is above the slow SMA.
        Sells when the fast SMA is below the slow SMA.
    """
    def __init__(self, fast_sma_days: int, slow_sma_days: int, allocation: float) -> None:
        """
        Initializes `SMAStrategy`.

        Args:
            fast_sma_days: The amount of days for the fast SMA (lower = faster).
            slow_sma_days: The amount of days for the slow SMA (higher = slower).
            allocation: The percent of the portfolio cash traded.
        """
        self._fast_sma = SMA(fast_sma_days)
        self._slow_sma = SMA(slow_sma_days)

        self._allocation = allocation

        self._prev_state: SMAState | None = None
        self._prev_event: MarketDataEvent | None = None
    
    def _should_buy(self, previous: SMAState, current: SMAState) -> bool:
        """
        Returns true upon the fast sma crossing above the slow sma & not already being in a position.
        """
        return (
            previous == SMAState.BELOW
            and current == SMAState.ABOVE
            and not self._holding
        )
    
    def _should_sell(self, previous: SMAState, current: SMAState) -> bool:
        """
        Returns true upon the fast sma crossing below the slow sma & already being in a position.
        """
        return (
            previous == SMAState.ABOVE 
            and current == SMAState.BELOW
            and self._holding
        )
    
    @property
    def _holding(self) -> bool:
        """
        Returns True if currently in a position.
        """
        return self.portfolio_snapshot.position > 0

    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Buys upon a SMA crossover up, sells upon a SMA crossover down.
        """
        fast_sma = self._fast_sma.update(event.close)
        slow_sma = self._slow_sma.update(event.close)

        if fast_sma is None or slow_sma is None:
            return

        state = SMAState.get_state(fast_sma, slow_sma)

        # First valid state
        if self._prev_state is None:
            self._prev_state = state
            return

        # Crossover below to above
        if self._should_buy(self._prev_state, state):
            quantity = int((self._allocation * self.portfolio_snapshot.cash) / event.close)
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=quantity,
                reason="SMA bullish crossover"
            )

        # Crossover above to below
        elif self._should_sell(self._prev_state, state):
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="SMA bearish crossover"
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
