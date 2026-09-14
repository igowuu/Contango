from __future__ import annotations

import sqlite3
from types import TracebackType
from pathlib import Path
from datetime import datetime, timezone
from typing import Iterable

from platformdirs import user_data_dir

from contango.trading.execution.engine.events.types import MarketDataEvent


_DEFAULT_DB_FILENAME = "database_storage.db"


def _default_database_path() -> Path:
    """
    Resolves the database path.
    """
    return Path(user_data_dir("contango", "contango")) / _DEFAULT_DB_FILENAME


class DataStorage:
    """
    Allows for the storage of OHLCV data to prevent re-polling API data that
    has already been received before.
    """
    def __enter__(self) -> DataStorage:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None
    ) -> None:
        self.close()

    def __init__(self, database_path: str | Path | None = None) -> None:
        """
        Initializes `DataStorage`.

        Args:
            database_path: Where to store the database. If not provided, falls
                           back to the OS-standard user data directory.
        """
        resolved_path = Path(database_path) if database_path is not None else _default_database_path()
        resolved_path.parent.mkdir(parents=True, exist_ok=True)

        self._connection = sqlite3.connect(resolved_path)
        self.database_path = resolved_path

        self._create_tables()

    def _create_tables(self) -> None:
        """
        Creates the empty tables under the database if they don't already exist.
        """
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS market_data (
                symbol TEXT NOT NULL,
                interval TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL,
                close REAL NOT NULL,
                volume INTEGER NOT NULL,

                PRIMARY KEY(symbol, interval, timestamp)
            )
            """
        )

        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS symbol_coverage (
                symbol TEXT NOT NULL,
                interval TEXT NOT NULL,
                earliest_available_timestamp INTEGER NOT NULL,

                PRIMARY KEY(symbol, interval)
            )
            """
        )

        self._connection.commit()

    def add_data_to_storage(
        self,
        interval: str,
        data: list[MarketDataEvent],
    ) -> None:
        """
        Adds market data to storage. Any existig candles with the same symbol/interval/timestamp are ignored.

        Args:
            interval: The interval to save the data as (i.e. `1m`, `5m`, etc).
            data: The data to save into the database.
        """
        self._connection.executemany(
            """
            INSERT OR IGNORE INTO market_data
            (
                symbol,
                interval,
                timestamp,
                open,
                high,
                low,
                close,
                volume
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    event.symbol,
                    interval,
                    event.timestamp,
                    event.open,
                    event.high,
                    event.low,
                    event.close,
                    event.volume,
                )
                for event in data
            ],
        )

        self._connection.commit()

    def get_data(
        self,
        symbol: str,
        interval: str,
        start_timestamp: int,
        end_timestamp: int,
    ) -> list[MarketDataEvent]:
        """
        Retrieves market data in order by timestamp.

        Args:
            symbol: The symbol to derive data from.
            interval: The interval to retrieve data from for the symbol (i.e. `1m`, `5m`, etc).
            start_timestamp: The start timestamp in unix ms.
            end_timestamp: The end timestamp in unix ms.

        Returns:
            list[MarketDataEvent]: The data for the provided parameters.
        """
        cursor = self._connection.execute(
            """
            SELECT
                timestamp,
                symbol,
                open,
                high,
                low,
                close,
                volume
            FROM market_data
            WHERE symbol = ?
              AND interval = ?
              AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp ASC
            """,
            (
                symbol,
                interval,
                start_timestamp,
                end_timestamp,
            ),
        )

        return [
            MarketDataEvent(
                timestamp=row[0],
                symbol=row[1],
                open=row[2],
                high=row[3],
                low=row[4],
                close=row[5],
                volume=row[6],
            )
            for row in cursor.fetchall()
        ]

    def get_missing_timestamps(
        self,
        symbol: str,
        interval: str,
        expected_timestamps: Iterable[datetime],
        earliest_available: int | None = None,
    ) -> list[int]:
        """
        Returns the timestamps that are NOT currently stored for the given
        symbol or interval, out of a supplied set of expected timestamps.

        Args:
            symbol: The symbol to check.
            interval: The interval to check (i.e. `1m`, `5m`, etc).
            expected_timestamps: The datetimes candles are expected to exist
                                 for. Must be timezone-aware (or assumed UTC if naive) since
                                 stored timestamps are unix ms in UTC.
            earliest_available: If provided, expected timestamps earlier than
                                this (unix ms) are dropped before the missing-check,
                                since they're already known to have no data
                                available from the provider.

        Returns:
            list[int]: Sorted list of missing timestamps (unix ms).
        """
        expected_ms = {
            int(
                (ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc))
                .timestamp() * 1000
            )
            for ts in expected_timestamps
        }

        if earliest_available is not None:
            expected_ms = {ts for ts in expected_ms if ts >= earliest_available}

        if not expected_ms:
            return []

        cursor = self._connection.execute(
            """
            SELECT timestamp
            FROM market_data
            WHERE symbol = ?
            AND interval = ?
            AND timestamp BETWEEN ? AND ?
            """,
            (
                symbol,
                interval,
                min(expected_ms),
                max(expected_ms),
            ),
        )

        existing = {row[0] for row in cursor.fetchall()}

        return sorted(expected_ms - existing)

    def get_earliest_available(self, symbol: str, interval: str) -> int | None:
        """
        Returns the earliest timestamp (unix ms) known to be a valid lower
        bound for this symbol/interval's data, if one has been recorded. None if never recorded.
        """
        cursor = self._connection.execute(
            """
            SELECT earliest_available_timestamp
            FROM symbol_coverage
            WHERE symbol = ? AND interval = ?
            """,
            (symbol, interval),
        )
        row = cursor.fetchone()
        return row[0] if row is not None else None

    def set_earliest_available(self, symbol: str, interval: str, timestamp: int) -> None:
        """
        Records the earliest known-valid lower bound (unix ms) for the
        symbol/interval.
        """
        self._connection.execute(
            """
            INSERT INTO symbol_coverage (symbol, interval, earliest_available_timestamp)
            VALUES (?, ?, ?)
            ON CONFLICT(symbol, interval) DO UPDATE SET earliest_available_timestamp = excluded.earliest_available_timestamp
            """,
            (symbol, interval, timestamp),
        )
        self._connection.commit()

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        self._connection.close()
