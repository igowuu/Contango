from __future__ import annotations

import pandas as pd
import pytest

from execution.backtester.market.feed import MarketDataFeed
from execution.engine.events.event_bus import EventBus
from execution.engine.events.events import MarketDataEvent


def _create_valid_dataframe() -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "symbol": ["AAPL", "AAPL"],
            "open": [100.0, 101.0],
            "high": [101.0, 102.0],
            "low": [99.0, 100.0],
            "close": [100.5, 101.5],
            "volume": [1000, 1100],
        },
        index=pd.Index([1000, 2000], name="timestamp"),
    )

    return df.astype(
        {
            "open": "float64",
            "high": "float64",
            "low": "float64",
            "close": "float64",
            "volume": "int64",
            "symbol": "object",
        }
    )


def test_get_initial_event_returns_first_row() -> None:
    feed = MarketDataFeed(_create_valid_dataframe(), EventBus())

    event = feed.get_initial_event()

    assert event == MarketDataEvent(1000, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000)


def test_run_publishes_all_rows_in_order() -> None:
    bus = EventBus()
    received: list[MarketDataEvent] = []
    bus.subscribe(MarketDataEvent, received.append, priority=0)

    feed = MarketDataFeed(_create_valid_dataframe(), bus)
    feed.run()

    assert received == [
        MarketDataEvent(1000, "AAPL", 100.0, 101.0, 99.0, 100.5, 1000),
        MarketDataEvent(2000, "AAPL", 101.0, 102.0, 100.0, 101.5, 1100),
    ]


def test_empty_dataframe_raises_value_error() -> None:
    df = _create_valid_dataframe().iloc[0:0]

    with pytest.raises(ValueError):
        MarketDataFeed(df, EventBus())


def test_missing_required_column_raises_value_error() -> None:
    df = _create_valid_dataframe().drop(columns=["volume"])

    with pytest.raises(ValueError):
        MarketDataFeed(df, EventBus())


def test_multiple_symbols_raises_value_error() -> None:
    df = _create_valid_dataframe()
    df.loc[2000, "symbol"] = "MSFT"

    with pytest.raises(ValueError):
        MarketDataFeed(df, EventBus())


def test_unsorted_index_raises_value_error() -> None:
    df = _create_valid_dataframe().iloc[::-1]

    with pytest.raises(ValueError):
        MarketDataFeed(df, EventBus())