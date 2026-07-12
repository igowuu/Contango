from __future__ import annotations

from execution.engine import Strategy, MarketDataEvent

from research.methods.calculations.ema import EMA
from research.methods.calculations.rsi import RSI
from research.methods.state.ema_state import EMAState
from research.methods.state.rsi_state import RSIState


class EMAWithRSI(Strategy):
    """
    Strategy where RSI extremes are the entry trigger and the EMA relationship is a standing regime filter.
    """
    def __init__(
        self,
        fast_ema_period: int,
        slow_ema_period: int,
        rsi_period: int,
        upper_rsi_threshold: float,
        lower_rsi_threshold: float,
        allocation: float
    ) -> None:
        """
        Initializes `EMAWithRSI`.
        
        Args:
            fast_ema_period: The period for the fast EMA.
            slow_ema_period: The period for the slow EMA.
            rsi_period: The period for the RSI.
            upper_rsi_threshold: Bullish boundary.
            lower_rsi_threshold: Bearish boundary.
            allocation: The percent of the portfolio cash traded.
        """
        self._fast_ema = EMA(fast_ema_period)
        self._slow_ema = EMA(slow_ema_period)
        self._rsi = RSI(rsi_period)

        self._upper_rsi_threshold = upper_rsi_threshold
        self._lower_rsi_threshold = lower_rsi_threshold
        self._allocation = allocation

        self._prev_event: MarketDataEvent | None = None

    def _should_buy(self, current_ema_state: EMAState, current_rsi_state: RSIState) -> bool:
        return (
            current_ema_state == EMAState.ABOVE  # trend filter: fast > slow
            and current_rsi_state == RSIState.OVERSOLD  # RSI dipped to oversold
            and not self._holding
        )

    def _should_sell(self, current_ema_state: EMAState, current_rsi_state: RSIState) -> bool:
        return (
            self._holding
            and (
                current_rsi_state == RSIState.OVERBOUGHT  # RSI mean-reverted back up
                or current_ema_state == EMAState.BELOW  # trend filter flipped
            )
        )
    
    def _get_ema_state(self, fast_ema: float, slow_ema: float) -> EMAState:
        """
        Returns the ema state (above or below) of the fast ema.
        """
        if fast_ema > slow_ema:
            return EMAState.ABOVE
        else:
            return EMAState.BELOW
    
    def _get_rsi_state(self, rsi: float) -> RSIState:
        """
        Returns the rsi state (oversold, overbought, or neutral).
        """
        if rsi < self._lower_rsi_threshold:
            return RSIState.OVERSOLD
        elif rsi > self._upper_rsi_threshold:
            return RSIState.OVERBOUGHT
        else:
            return RSIState.NEUTRAL
    
    @property
    def _holding(self) -> bool:
        """
        Returns if currently in a position.
        """
        return self.portfolio_snapshot.position > 0

    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Buys upon an EMA crossover up, sells upon an EMA crossover down.
        """
        fast_ema = self._fast_ema.update(event.close)
        slow_ema = self._slow_ema.update(event.close)
        rsi = self._rsi.update(event.close)

        if rsi is None:
            return

        ema_state = self._get_ema_state(fast_ema, slow_ema)
        rsi_state = self._get_rsi_state(rsi)

        should_buy = self._should_buy(ema_state, rsi_state)
        should_sell = self._should_sell(ema_state, rsi_state)

        if should_buy:
            quantity = int((self._allocation * self.portfolio_snapshot.cash) / event.close)
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=quantity,
                reason="Bullish crossover with RSI confirmation"
            )

        elif should_sell:
            self.order_api.submit_order(
                market_data=event,
                symbol=event.symbol,
                quantity=-self.portfolio_snapshot.position,
                reason="EMA trend reversal or RSI weakness",
            )

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
