from __future__ import annotations

from execution.engine import Strategy, MarketDataEvent

from research.methods.calculations.rsi import RSI
from research.methods.state.rsi_state import RSIState



class RSIMeanReversion(Strategy):
    """
    RSI mean reversion strategy.

    Rules:
        - Position size is based on portfolio value.
        - Buy when RSI goes from an oversold to neutral state.
        - Sell when RSI goes from an overbought to neutral state.
    """
    def __init__(
        self,
        period: int = 14,
        lower_threshold: float = 30.0,
        upper_threshold: float = 70.0,
        allocation: float = 1.0
    ) -> None:
        """
        Args:
            period: RSI lookback period.
            lower_threshold: Oversold boundary.
            upper_threshold: Overbought boundary.
            allocation: The percent of the portfolio cash traded.
        """
        self._rsi = RSI(period)

        self._lower = lower_threshold
        self._upper = upper_threshold
        self._allocation = allocation

        self._prev_state: RSIState | None = None
        self._prev_event: MarketDataEvent | None = None

    def _should_buy(self, previous: RSIState, current: RSIState) -> bool:
        """
        Returns true upon the rsi transitioning away from oversold not already being in a position.
        """
        return (
            previous == RSIState.OVERSOLD
            and current == RSIState.NEUTRAL
            and not self._holding
        )

    def _should_sell(self, previous: RSIState, current: RSIState) -> bool:
        """
        Returns true upon the rsi transitioning away from overbought & having been in a position.
        """
        return (
            previous == RSIState.OVERBOUGHT
            and current == RSIState.NEUTRAL
            and self._holding
        )
    
    @property
    def _holding(self) -> bool:
        """
        Returns if currently in a position.
        """
        return self.portfolio_snapshot.position > 0

    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Generates trades based on RSI threshold transitions.
        """
        rsi = self._rsi.update(event.close)

        if rsi is None:
            return
        
        state = RSIState.get_state(rsi, self._lower, self._upper)

        # Initial state
        if self._prev_state is None:
            self._prev_state = state
            return

        # Price transitions from oversold to neutral
        if self._should_buy(self._prev_state, state):
            quantity = int((self._allocation * self.portfolio_snapshot.cash) / event.close)
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=quantity,
                reason="RSI exit oversold"
            )

        # Price transitions from overbought to neutral
        elif self._should_sell(self._prev_state, state):
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="RSI exit overbought"
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
