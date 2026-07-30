# data/data_repository.py — part of Contango, a parameterized backtesting & execution framework
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

from dataclasses import replace
from pathlib import Path
from typing import Generic, TypeVar, Iterable
from datetime import datetime

from contango.broker.historical_brokers.config_type import Config
from contango.broker.historical_brokers.historical_broker import HistoricalBroker

from contango.trading.execution.engine.events.events import MarketDataEvent

from contango.data.storage.store_market_data import DataStorage


TConfig = TypeVar("TConfig", bound=Config)


class DataRepository(Generic[TConfig]):
    """
    Retrieves data from either internal storage, a broker, or both.
    Data that is not already in storage is automatically added.
    """
    @staticmethod
    def get_data_and_store(
        broker: HistoricalBroker[TConfig],
        config: TConfig,
        expected_timestamps: Iterable[datetime],
        database_path: str | Path | None = None,
    ) -> list[MarketDataEvent]:
        """
        Retrieves data from either the database, a broker, or both.
        Any data not in the database that is retrieved from the broker is then put into storage for further use.

        Args:
            broker: The historical broker to derive data from if necessary.
            config: The corresponding config to the historical broker.
            expected_timestamps: An iterable of the expected timestamps.
            database_path: Where the database should live. If not provided,
                           DataStorage resolves it via  the OS-standard
                           user data directory.
        """
        with DataStorage(database_path) as storage:
            ticker = config.ticker
            interval = config.interval.__str__()
            start_timestamp = config.start_timestamp
            end_timestamp = config.end_timestamp
            missing_timestamps = storage.get_missing_timestamps(ticker, interval, expected_timestamps)
            if len(missing_timestamps) != 0:
                min_timestamp = min(missing_timestamps)
                max_timestamp = max(missing_timestamps)
                interval_ms = int(config.interval.value.total_seconds() * 1000)
                new_config = replace(
                    config,
                    start_timestamp=min_timestamp,
                    end_timestamp=max(max_timestamp + interval_ms, min_timestamp + interval_ms),
                )
                new_data = broker.get_bars(new_config)
                storage.add_data_to_storage(interval, new_data)

            data = storage.get_data(ticker, interval, start_timestamp, end_timestamp)

        return data
