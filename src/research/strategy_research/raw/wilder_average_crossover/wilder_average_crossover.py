from __future__ import annotations

from execution.engine import Strategy, MarketDataEvent

from research.methods.calculations.wilder_average import WilderAverage
from research.methods.state.wilder_average_state import WilderState


class WilderAverageCrossover(Strategy):
    """
    Simple Wilder Average double crossover strategy.

    Rules:
        Position size is based on portfolio value.
        Buys when the fast Wilder Average is above the slow Wilder Average.
        Sells when the fast Wilder Average is below the slow Wilder Average.
    """
    def __init__(self, fast_wilder_days: int, slow_wilder_days: int, allocation: float) -> None:
        """
        Initializes `WilderAverageCrossover`.

        Args:
            fast_wilder_days: The period for the fast Wilder Average.
            slow_wilder_days: The period for the slow Wilder Average.
            allocation: The percent of the portfolio cash traded.
        """
        self._fast_wilder = WilderAverage(fast_wilder_days)
        self._slow_wilder = WilderAverage(slow_wilder_days)

        self._allocation = allocation

        self._prev_state: WilderState | None = None
        self._prev_event: MarketDataEvent | None = None

    def _should_buy(self, previous: WilderState, current: WilderState) -> bool:
        """
        Returns true upon the fast wilder crossing above the slow wilder & not already being in a position.
        """
        return (
            previous == WilderState.BELOW 
            and current == WilderState.ABOVE
            and not self._holding
        )
    
    def _should_sell(self, previous: WilderState, current: WilderState) -> bool:
        """
        Returns true upon the fast wilder crossing below the slow wilder & already being in a position.
        """
        return (
            previous == WilderState.ABOVE 
            and current == WilderState.BELOW
            and self._holding
        )

    def _get_wilder_state(self, fast_wilder: float, slow_wilder: float) -> WilderState:
        """
        Returns the wilder state (above or below the slow wilder) of the fast wilder.
        """
        if fast_wilder > slow_wilder:
            return WilderState.ABOVE
        else:
            return WilderState.BELOW
    
    @property
    def _holding(self) -> bool:
        """
        Returns True if currently in a position (units held above zero).
        """
        return self.portfolio_snapshot.position > 0

    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Buys upon an Wilder Average crossover up, sells upon an Wilder Average crossover down.
        """
        fast_wilder = self._fast_wilder.update(event.close)
        slow_wilder = self._slow_wilder.update(event.close)

        if fast_wilder is None or slow_wilder is None:
            return

        state = self._get_wilder_state(fast_wilder, slow_wilder)

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
                reason="Wilder bullish crossover"
            )

        # Crossover above -> below
        elif self._should_sell(self._prev_state, state):
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="Wilder bearish crossover"
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
