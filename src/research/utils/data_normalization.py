from __future__ import annotations

import yfinance as yf   # type: ignore[reportMissingStubs]
import pandas as pd


def normalize_yfinance_data(yf_data: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """
    Normalizes yfinance data into the expected `Backtester` format with a single symbol.
    
    Args:
        yf_data: The dataframe from `yfinance`.
        symbol: The single symbol for the dataframe.
    
    Returns:
        The normalized dataframe.
    """
    df = yf_data.copy()

    # ('Close', 'AAPL') -> 'Close'
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # ['close', 'high', 'low', 'open', 'volume']
    df.columns = [c.lower() for c in df.columns]

    # Verify that the expected columns exist
    required = {"open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required yfinance columns: {missing}")
    
    # Get rid of any extra columns that might exist
    df = df[list(required)]

    # Create the symbol column & rename the index to timestamp (expected name)
    df["symbol"] = symbol
    df.index.name = "timestamp"

    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("Expected DatetimeIndex from yfinance")
    
    # Sort by index if not already
    df = df.sort_index()

    # Convert unix timestamp in seconds to millesconds.
    # When converting pandas DatetimeIndex objects to int64, unix seconds is returned.
    # Multiplying by 1000 ensures that the data is in ms, which is what the codebase expects.
    # Nanoseconds is what would be expected to be returned, but this is not the case; it may
    # be a logical issue within yfinance itself, or a quirk that I (the programmer) am unaware about.
    # Either way, this DOES yield correct dates after empirically testing.
    df.index = pd.Index([int(x) for x in df.index.astype("int64") * 1000])
    return df
