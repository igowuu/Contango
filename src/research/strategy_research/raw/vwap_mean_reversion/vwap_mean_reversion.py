from __future__ import annotations

from execution.engine import Strategy, MarketDataEvent

from research.methods.calculations.vwap import VWAP
from research.methods.state.vwap_state import VWAPState


class VWAPMeanReversion(Strategy):
    """
    VWAP mean reversion strategy.

    Rules:
        Resets VWAP at the start of each new trading session.
        Buys when price closes below the lower VWAP band.
        Sells when price crosses back above the lower VWAP band.
    """
    def __init__(self, k: float, allocation: float) -> None:
        """
        Initializes `VWAPMeanReversion`.

        Args:
            k: Band-width multiplier in standard deviations.
            allocation: The percent of portfolio cash traded.
        """
        self._vwap = VWAP(k)
        self._allocation = allocation

        self._prev_zone: VWAPState | None = None
        self._prev_event: MarketDataEvent | None = None
        self._prev_day: int | None = None

    def _get_day(self, timestamp: int) -> int:
        """
        Extracts the UTC date in days from a unix ms timestamp.
        """
        return timestamp // (1000 * 60 * 60 * 24)

    def _is_new_session(self, event: MarketDataEvent) -> bool:
        """
        Returns True if this bar belongs to a new trading day.
        """
        current_day = self._get_day(event.timestamp)
        if self._prev_day is None or current_day != self._prev_day:
            self._prev_day = current_day
            return True
        return False

    def _should_buy(self, previous: VWAPState, current: VWAPState) -> bool:
        """
        Returns True when price crosses below the lower band and not already holding.
        """
        return (
            previous != VWAPState.BELOW_LOWER
            and current == VWAPState.BELOW_LOWER
            and not self._holding
        )

    def _should_sell(self, previous: VWAPState, current: VWAPState) -> bool:
        """
        Returns True when price crosses back above the lower band while holding.
        """
        return (
            previous == VWAPState.BELOW_LOWER
            and current != VWAPState.BELOW_LOWER
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
        Resets VWAP on new sessions, then applies mean reversion logic.
        """
        if self._is_new_session(event):
            self._vwap.reset()
            # Force exit any open position at the start of a new day
            if self._holding and self._prev_event is not None:
                self.order_api.submit_order(
                    market_data=event,
                    symbol=event.symbol,
                    quantity=-self.portfolio_snapshot.position,
                    reason="Session ended with open position"
                )
            self._prev_zone = None

        snapshot = self._vwap.update(
            high=event.high,
            low=event.low,
            close=event.close,
            volume=event.volume
        )

        if snapshot is None:
            self._prev_event = event
            return

        zone = VWAPState.get_state(event.close, snapshot)

        if self._prev_zone is None:
            self._prev_zone = zone
            self._prev_event = event
            return

        if self._should_buy(self._prev_zone, zone):
            quantity = int(self._allocation * self.portfolio_snapshot.cash / event.close)
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=quantity,
                reason="Price crossed below lower VWAP band"
            )

        elif self._should_sell(self._prev_zone, zone):
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="Price crossed above lower VWAP band"
            )

        self._prev_zone = zone
        self._prev_event = event

    def on_end(self) -> None:
        """
        Sells any remaining position at end of backtest.
        """
        if self._prev_event is None:
            raise RuntimeError("Previous event was never set.")

        if self._holding:
            self.order_api.submit_order(
                market_data=self._prev_event,
                symbol=self._prev_event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="Sold all remaining shares at end of strategy."
            )
