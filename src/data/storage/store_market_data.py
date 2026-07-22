# data/storage/store_market_data.py — part of Contango, a parameterized backtesting & execution framework
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

import sqlite3
from types import TracebackType
from pathlib import Path
from datetime import datetime, timezone
from typing import Iterable

from trading.execution.engine.events.events import MarketDataEvent


class DataStorage:
    """
    Allows for the storage of OHLCV data without to prevent re-polling API data that
    has already been recieved before.
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

    def __init__(self, database_path: str | Path = "data/storage/database_storage.db") -> None:
        """
        Initializes `DataStorage`.
        
        Args:
            database_path: The path to save all data in the database to.
        """
        self._connection = sqlite3.connect(database_path)

        self._create_tables()

    def _create_tables(self) -> None:
        """
        Creates an empty table with no data inside of it under the database.
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

        self._connection.commit()

    def add_data_to_storage(
        self,
        interval: str,
        data: list[MarketDataEvent],
    ) -> None:
        """
        Adds market data to storage. Existing candles with the same symbol/interval/timestamp are ignored.

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
        Retrieves market data in chronological order by timestamp.

        Args:
            symbol: The symbol to derive data from.
            interval: The interval to retrieve data from for the symbol (i.e. `1m`, `5m`, etc).
            start_timestamp: The start timestamp in unix ms.
            end_timestamp: The end timestamp in unix ms.
        
        Returns:
            list[MarketDataEvent]: The data for the provided parameters, if any.
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
    ) -> list[int]:
        """
        Returns the timestamps that are NOT currently stored for the given
        symbol/interval, out of a caller-supplied set of expected timestamps.
        Callers are responsible for generating the correct expected schedule.

        Args:
            symbol: The symbol to check.
            interval: The interval to check (i.e. `1m`, `5m`, etc).
            expected_timestamps: The datetimes candles are expected to exist
                for. Must be timezone-aware (or assumed UTC if naive) since
                stored timestamps are unix ms in UTC.

        Returns:
            list[int]: Sorted list of missing timestamps (unix ms). Empty if
                fully cached.
        """
        expected_ms = {
            int(
                (ts if ts.tzinfo else ts.replace(tzinfo=timezone.utc))
                .timestamp() * 1000
            )
            for ts in expected_timestamps
        }

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

    def close(self) -> None:
        """
        Closes the connection to the database.
        """
        self._connection.close()
