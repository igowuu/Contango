# research/research_strategies/bollinger_band_mean_reversion/strategy.py — part of Contango, a parameterized backtesting & execution framework
# Copyright (C) 2026  Jacob Taylor
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

from contango.trading.execution.engine import Strategy

from contango.trading.execution.engine.events.events import MarketDataEvent
from contango.trading.indicators.calculations import BollingerBands, BollingerBandSnapshot


class BollingerBandMeanReversion(Strategy):
    """
    A bare-bones bollinger band mean reversion strategy.
    
    Buys long upon the closing price crossing below the lower band.
    Sells upon the closing price reverting to above the middle band.
    A fixed allocation of the portfolio is traded.
    No pyramiding is allowed (so only one trade at a time), and only one ticker symbol can be traded.
    """
    def __init__(
        self,
        bollinger_bands_period: int,
        bollinger_bands_stdev: float,
        allocation: float,
        symbol: str
    ) -> None:
        """
        Initializes `BollingerBandMeanReversion` with the bollinger bands indicator.
        """
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
        """
        Returns `True` if the close price crosses from above the lower band to below it, while not already
        having been in a position.
        """
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
        """
        Returns `True` if the close price crosses from below the middle band to above it, while currently
        being in a position.
        """
        return (
            prev_close <= previous.middle
            and current_close > current.middle
            and holding
        )

    def on_market_event(self, event: MarketDataEvent) -> None:
        """
        Method called every market event (bar) - main execution logic should go here.
        """
        close = event.close
        snapshot = self._bollinger_bands.update(close)

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
        """
        Method called after all bars are finished - sells any persisting orders at the end, if any.
        """
        holding = self.portfolio_snapshot.position > 0
        final_event = self._previous_event
        
        if final_event is None:
            raise ValueError("The final market data event was never set.")

        if holding:
            units_to_sell = self.portfolio_snapshot.position
            self.order_api.submit_order(final_event, self._symbol, -units_to_sell)
