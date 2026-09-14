from __future__ import annotations

from contango.strategy.strategy import Strategy

from contango.trading.execution.engine.events.types import MarketDataEvent
from contango.stream.indicators.calculations import BollingerBands, BollingerBandSnapshot


class BollingerBandMeanReversion(Strategy):
    def __init__(
        self,
        bollinger_bands_period: int,
        bollinger_bands_stdev: float,
        allocation: float,
        symbol: str
    ) -> None:
        self._bollinger_bands = BollingerBands(bollinger_bands_period, bollinger_bands_stdev)
        self._allocation = allocation
        self._symbol = symbol

        self._previous_snapshot: BollingerBandSnapshot | None = None
        self._previous_event: MarketDataEvent | None = None

    def _should_buy(
        self, 
        prev_close: float,
        current_close: float,
        previous: BollingerBandSnapshot, 
        current: BollingerBandSnapshot, 
        holding: bool
    ) -> bool:
        return (
            prev_close >= previous.lower
            and current_close < current.lower
            and not holding
        )
    
    def _should_sell(
        self, 
        prev_close: float,
        current_close: float,
        previous: BollingerBandSnapshot, 
        current: BollingerBandSnapshot, 
        holding: bool
    ) -> bool:
        return (
            prev_close <= previous.middle
            and current_close > current.middle
            and holding
        )

    def on_market_event(self, event: MarketDataEvent) -> None:
        close = event.close
        snapshot = self._bollinger_bands.update(event)

        if self._previous_event is None or self._previous_snapshot is None or snapshot is None:
            self._previous_event = event
            self._previous_snapshot = snapshot
            return

        prev_close = self._previous_event.close
        holding = self.portfolio_snapshot.position > 0
        prev_snapshot = self._previous_snapshot

        if self._should_buy(prev_close, close, prev_snapshot, snapshot, holding):
            units_to_buy = int(self._allocation * self.portfolio_snapshot.cash / close)
            self.order_api.submit_order(event, self._symbol, units_to_buy)
        elif self._should_sell(prev_close, close, prev_snapshot, snapshot, holding):
            units_to_sell = self.portfolio_snapshot.position
            self.order_api.submit_order(event, self._symbol, -units_to_sell)
        
        self._previous_snapshot = snapshot
        self._previous_event = event

    def on_end(self) -> None:
        holding = self.portfolio_snapshot.position > 0
        final_event = self._previous_event
        
        if final_event is None:
            raise ValueError("The final market data event was never set.")

        if holding:
            units_to_sell = self.portfolio_snapshot.position
            self.order_api.submit_order(final_event, self._symbol, -units_to_sell)
