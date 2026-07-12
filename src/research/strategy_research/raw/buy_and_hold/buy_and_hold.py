from __future__ import annotations

from execution.engine import Strategy, MarketDataEvent


class BuyAndHold(Strategy):
    """
    Simple buy & hold strategy.

    Rules:
        Position size is based on portfolio value.
        Buys once in the beginning and sells at the end.
    """
    def __init__(self, allocation: float) -> None:
        """
        Initializes `BuyAndHold`.

        Args:
            allocation: The percent of the portfolio cash traded.
        """
        self._allocation = allocation
        self._bought = False
        self._prev_event: MarketDataEvent | None = None

    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Buys once at the start and sells at the end.
        """
        if not self._bought:
            quantity = int((self._allocation * self.portfolio_snapshot.cash) / event.close)
            self.order_api.submit_order(event, event.symbol, quantity, "Initial buy")
            self._bought = True
        self._prev_event = event

    def on_end(self) -> None:
        """
        Sells the final position at the end.
        """
        if self._prev_event is None:
            raise RuntimeError("Previous event was never set.")

        self.order_api.submit_order(
            market_data=self._prev_event, 
            symbol=self._prev_event.symbol, 
            quantity=-self.portfolio_snapshot.position,
            reason="Final sell"
        )
