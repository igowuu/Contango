# pyright: reportPrivateUsage=false

import pytest

from execution.engine import (
    AcceptedFillEvent, 
    ExecutionData, 
    MarketDataEvent, 
    OrderEvent,
    PortfolioSnapshotEvent
)

from optimizer.analysis.builder import _build_trades


class TestBuildTrades:
    """
    Logic & regression tests for the `_build_trades` function.

    Expected: Builds a tuple of TradePoints from accepted fill events using
    FIFO lot matching. Buys open lots; sells close them in the order they
    were opened. Raises ValueError if a sell exceeds the current position.
    """
    def setup_method(self) -> None:
        self.single_buy_sell = self._make_data([
            self._make_fill(1704067200000, quantity=10, price=100.0),
            self._make_fill(1704153600000, quantity=-10, price=110.0),
        ])
        self.single_buy_partial_sell = self._make_data([
            self._make_fill(1704067200000, quantity=10, price=100.0),
            self._make_fill(1704153600000, quantity=-4, price=110.0),
        ])
        self.single_buy_two_partial_sells = self._make_data([
            self._make_fill(1704067200000, quantity=10, price=100.0),
            self._make_fill(1704153600000, quantity=-4, price=110.0),
            self._make_fill(1704240000000, quantity=-6, price=120.0),
        ])
        self.two_buys_one_sell = self._make_data([
            self._make_fill(1704067200000, quantity=5, price=100.0),
            self._make_fill(1704153600000, quantity=5, price=110.0),
            self._make_fill(1704240000000, quantity=-10, price=120.0),
        ])
        self.two_buys_sell_spans_both = self._make_data([
            self._make_fill(1704067200000, quantity=3, price=100.0),
            self._make_fill(1704153600000, quantity=7, price=110.0),
            self._make_fill(1704240000000, quantity=-10, price=120.0),
        ])
        self.buy_only = self._make_data([
            self._make_fill(1704067200000, quantity=10, price=100.0),
        ])
        self.oversell = self._make_data([
            self._make_fill(1704067200000, quantity=5, price=100.0),
            self._make_fill(1704153600000, quantity=-10, price=110.0),
        ])
        self.multiple_independent_trades = self._make_data([
            self._make_fill(1704067200000, quantity=10, price=100.0),
            self._make_fill(1704153600000, quantity=-10, price=110.0),
            self._make_fill(1704240000000, quantity=10, price=105.0),
            self._make_fill(1704326400000, quantity=-10, price=95.0),
        ])

    def _make_market_event(self, timestamp: int) -> MarketDataEvent:
        return MarketDataEvent(
            timestamp=timestamp,
            symbol="TEST",
            open=100.0,
            high=110.0,
            low=90.0,
            close=100.0,
            volume=1000,
        )

    def _make_fill(
        self,
        timestamp: int,
        quantity: int,
        price: float,
    ) -> AcceptedFillEvent:
        return AcceptedFillEvent(
            timestamp=timestamp,
            market_event=self._make_market_event(timestamp),
            order_event=OrderEvent(
                timestamp=timestamp,
                symbol="TEST",
                quantity=quantity,
            ),
            fill_price=price,
            total_cost=0.0  # unused
        )

    def _make_data(self, fills: list[AcceptedFillEvent]) -> ExecutionData:
        return ExecutionData(
            accepted_fill_events=tuple(fills),
            rejected_fill_events=(),
            order_events=(),
            market_data_events=(),
            initial_portfolio_snapshot_event=PortfolioSnapshotEvent(0, 0, 0, 0),
            portfolio_snapshot_events=(),
        )

    def test_empty_fills_returns_empty(self) -> None:
        result = _build_trades(self._make_data([]))
        assert result == ()

    def test_buy_only_no_sell_returns_empty(self) -> None:
        result = _build_trades(self.buy_only)
        assert result == ()

    def test_single_buy_sell_returns_one_trade(self) -> None:
        result = _build_trades(self.single_buy_sell)
        assert len(result) == 1

    def test_single_buy_sell_entry_fields_are_correct(self) -> None:
        result = _build_trades(self.single_buy_sell)
        assert result[0].entry_time == 1704067200000
        assert result[0].entry_price == pytest.approx(100.0)

    def test_single_buy_sell_exit_fields_are_correct(self) -> None:
        result = _build_trades(self.single_buy_sell)
        assert result[0].exit_time == 1704153600000
        assert result[0].exit_price == pytest.approx(110.0)

    def test_single_buy_sell_quantity_is_correct(self) -> None:
        result = _build_trades(self.single_buy_sell)
        assert result[0].quantity == 10

    def test_partial_sell_returns_one_trade(self) -> None:
        result = _build_trades(self.single_buy_partial_sell)
        assert len(result) == 1

    def test_partial_sell_quantity_matches_sold_units(self) -> None:
        result = _build_trades(self.single_buy_partial_sell)
        assert result[0].quantity == 4

    def test_two_partial_sells_return_two_trades(self) -> None:
        result = _build_trades(self.single_buy_two_partial_sells)
        assert len(result) == 2

    def test_two_partial_sells_quantities_sum_to_original_buy(self) -> None:
        result = _build_trades(self.single_buy_two_partial_sells)
        assert sum(t.quantity for t in result) == 10

    def test_two_partial_sells_have_correct_exit_prices(self) -> None:
        result = _build_trades(self.single_buy_two_partial_sells)
        assert result[0].exit_price == pytest.approx(110.0)
        assert result[1].exit_price == pytest.approx(120.0)

    def test_two_partial_sells_share_same_entry(self) -> None:
        result = _build_trades(self.single_buy_two_partial_sells)
        assert result[0].entry_time == 1704067200000
        assert result[1].entry_time == 1704067200000
        assert result[0].entry_price == pytest.approx(100.0)
        assert result[1].entry_price == pytest.approx(100.0)

    def test_two_buys_one_sell_returns_two_trades(self) -> None:
        # One sell consuming two lots produces one TradePoint per lot
        result = _build_trades(self.two_buys_one_sell)
        assert len(result) == 2

    def test_two_buys_one_sell_fifo_order_is_correct(self) -> None:
        result = _build_trades(self.two_buys_one_sell)
        assert result[0].entry_time == 1704067200000
        assert result[0].entry_price == pytest.approx(100.0)
        assert result[1].entry_time == 1704153600000
        assert result[1].entry_price == pytest.approx(110.0)

    def test_two_buys_one_sell_quantities_are_correct(self) -> None:
        result = _build_trades(self.two_buys_one_sell)
        assert result[0].quantity == 5
        assert result[1].quantity == 5

    def test_sell_spanning_two_lots_exit_times_are_identical(self) -> None:
        # Both TradePoints produced by a single sell share the same exit time
        result = _build_trades(self.two_buys_sell_spans_both)
        assert result[0].exit_time == result[1].exit_time == 1704240000000

    def test_sell_spanning_two_lots_quantities_match_lot_sizes(self) -> None:
        result = _build_trades(self.two_buys_sell_spans_both)
        assert result[0].quantity == 3
        assert result[1].quantity == 7

    def test_multiple_independent_trades_returns_correct_count(self) -> None:
        result = _build_trades(self.multiple_independent_trades)
        assert len(result) == 2

    def test_multiple_independent_trades_first_is_profit(self) -> None:
        result = _build_trades(self.multiple_independent_trades)
        assert result[0].entry_price == pytest.approx(100.0)
        assert result[0].exit_price == pytest.approx(110.0)

    def test_multiple_independent_trades_second_is_loss(self) -> None:
        result = _build_trades(self.multiple_independent_trades)
        assert result[1].entry_price == pytest.approx(105.0)
        assert result[1].exit_price == pytest.approx(95.0)

    def test_oversell_raises_value_error(self) -> None:
        with pytest.raises(ValueError):
            _build_trades(self.oversell)
