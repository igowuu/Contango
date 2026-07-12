from __future__ import annotations

import pandas as pd

from typing import cast, Any

from execution.engine.events.events import MarketDataEvent
from execution.engine.events.event_bus import EventBus


ticker = str
time_unix_ms = int
units = int


class MarketDataFeed:
    """
    Allows an OHLCV dataframe to be sequentially iterated over & validated for structure.
    """
    def __init__(self, data: pd.DataFrame, event_bus: EventBus):
        """
        Initializes `MarketDataFeed`.
        
        Args:
            data: The OHLCV `DataFrame` to validate & iterate over.
            event_bus: The event bus to publish `MarketDataEvent` instances to.

        Raises:
            ValueError: Upon the OHLCV `DataFrame` failing validation.
        """
        _validate_market_data(data)

        self._data = data
        self._event_bus = event_bus

    def _get_event_for_row(self, row: Any) -> MarketDataEvent:
        """
        Returns a `MarketDataEvent` for a row in a pandas `DataFrame`.
        """
        # cast() is used here because the data was pre-validated & pandas is dynamically typed.
        bar_timestamp = cast(time_unix_ms, row.Index)
        bar_symbol = cast(ticker, row.symbol)
        bar_open = cast(units, row.open)
        bar_high = cast(units, row.high)
        bar_low = cast(units, row.low)
        bar_close = cast(units, row.close)
        bar_volume = cast(units, row.volume)

        market_data = MarketDataEvent(
            timestamp=bar_timestamp,
            symbol=bar_symbol,
            open=bar_open,
            high=bar_high,
            low=bar_low,
            close=bar_close,
            volume=bar_volume
        )

        return market_data

    def get_initial_event(self) -> MarketDataEvent:
        """
        Returns the first `MarketDataEvent` in the OHLCV data.
        """
        first_row = next(self._data.itertuples(index=True))
        return self._get_event_for_row(first_row)

    def run(self) -> None:
        """
        Iterates through the provided data, publishing `MarketDataEvent` objects for each DF row.
        """
        for row in self._data.itertuples(index=True):
            event = self._get_event_for_row(row)
            self._event_bus.publish(event)


def _validate_market_data(data: pd.DataFrame) -> None:
    """
    Checks structure, data types, and value constraints of an OHLCV data structure for the codebase.
    
    Args:
        data: Pandas DataFrame to be validated. 
            - Must contain only one ticker type.
            - Must contain columns: [`symbol`, `open`, `high`, `low`, `close`, `volume`]
            - Must contain `timestamp` as the index
            - The `timestamp` indicies must be sorted in ascending order
            - The `timestamp` indicies must be the time since unix (ms)
            - No columns, rows, or values must be None or NaN.
        
            - [`open`, `high`, `low`, `close`] -> **float**
            - [`symbol`] -> **str**
            - [`volume`] -> **int**
    
    Raises:
        ValueError: If schema is invalid or data types cannot be derived.
    """
    if data.empty:
        raise ValueError(
            f"Provided data is empty! Data given: {data}"
        )

    required_columns = {
        "symbol",
        "open",
        "high",
        "low",
        "close",
        "volume",
    }

    missing = required_columns - set(data.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    symbols = data["symbol"].unique()
    if len(symbols) != 1:
        raise ValueError(
            f"Backtester currently supports exactly one symbol. Got: {sorted(symbols)}"
        )

    if not pd.api.types.is_integer_dtype(data.index):
        raise ValueError(
            "Market data index (timestamp) must be an int (time since unix in ms)."
        )

    if not data.index.is_monotonic_increasing:
        raise ValueError(
            "Market data timestamps must be sorted ascending."
        )

    if not pd.api.types.is_string_dtype(data["symbol"]):
        raise ValueError(
            "'symbol' column must contain strings."
        )
    
    if not pd.api.types.is_integer_dtype(data["volume"]):
        raise ValueError(
            "'volume' column must be an int."
        )

    decimal_columns = [
        "open",
        "high",
        "low",
        "close"
    ]

    for column in decimal_columns:
        if not pd.api.types.is_float_dtype(data[column]):
            raise ValueError(
                f"'{column}' column must contain floats. "
                f"Got {data[column].dtype}."
            )

    if data.isna().any().any():
        null_columns = data.columns[data.isna().any()].tolist()
        raise ValueError(
            f"Market data contains missing values in: {null_columns}"
        )
