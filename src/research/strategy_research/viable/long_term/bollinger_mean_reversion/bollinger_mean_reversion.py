from __future__ import annotations

from execution.engine import Strategy, MarketDataEvent
from research.methods.calculations.bollinger_bands import BollingerBands
from research.methods.state.bollinger_bands_state import BollingerState


class BollingerMeanReversion(Strategy):
    """
    Bollinger mean reversion strategy.

    Rules:
        Position size is based on portfolio value (allocation).
        Buys when the price closes below the lower bollinger band.
        Sells when the price closes above the lower bollinger band.
    """
    def __init__(self, period: int, num_stdevs: float, allocation: float) -> None:
        """
        Initializes `BollingerMeanReversion`.

        Args:
            period: The lookback window for the bollinger bands.
            num_stdevs: The number of stdevs for the band width (K constant).
            allocation: The percent of the portfolio cash traded.
        """
        self._bollinger_bands = BollingerBands(period, num_stdevs)

        self._allocation = allocation
        self._prev_zone: BollingerState | None = None
        self._prev_event: MarketDataEvent | None = None

    def _should_buy(self, previous: BollingerState, current: BollingerState) -> bool:
        """
        Returns `True` upon the current band dropping below the lower band without being in a position.
        """
        return (
            previous != BollingerState.BELOW_LOWER
            and current == BollingerState.BELOW_LOWER
            and not self._holding
        )

    def _should_sell(self, previous: BollingerState, current: BollingerState) -> bool:
        """
        Returns `True` when price recovers above the lower band while being in a position.
        """
        return (
            previous == BollingerState.BELOW_LOWER
            and current != BollingerState.BELOW_LOWER
            and self._holding
        )

    @property
    def _holding(self) -> bool:
        """
        Returns `True` if currently in a position (position above zero).
        """
        return self.portfolio_snapshot.position > 0

    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Buys shares for the current market event (bar) based on the allocation & bollinger band state.
        """
        bollinger_snapshot = self._bollinger_bands.update(event.close)

        if bollinger_snapshot is None:
            return

        zone = BollingerState.get_state(event.close, bollinger_snapshot)

        # First valid zone
        if self._prev_zone is None:
            self._prev_zone = zone
            return

        # Price dips to below the lowest bollinger band
        if self._should_buy(self._prev_zone, zone):
            quantity = int(self._allocation * self.portfolio_snapshot.cash / event.close)
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=quantity,
                reason="Price crossed below the lowest bollinger band"
            )

        # Price crosses above the lower bollinger band
        elif self._should_sell(self._prev_zone, zone):
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="Price crossed above the lower bolinger band"
            )

        self._prev_zone = zone
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
