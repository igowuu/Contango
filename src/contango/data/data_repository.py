from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Generic, TypeVar, Iterable
from datetime import datetime

from contango.market.data_providers.config import Config
from contango.market.data_providers.historical_data_provider import HistoricalDataProvider

from contango.trading.execution.engine.events.types import MarketDataEvent

from contango.data.storage.store_market_data import DataStorage


TConfig = TypeVar("TConfig", bound=Config)


class DataRepository(Generic[TConfig]):
    """
    Retrieves data from either internal storage, a data provider, or both.
    Data that is not already in storage is automatically added.
    """
    @staticmethod
    def get_data_and_store(
        provider: HistoricalDataProvider[TConfig],
        config: TConfig,
        expected_timestamps: Iterable[datetime],
        database_path: str | Path | None = None,
    ) -> list[MarketDataEvent]:
        """
        Retrieves data from either the database, a provider, or both.
        Any data not in the database that is retrieved from the provider is then put into storage for further use.

        Args:
            provider: The historical provider to derive data from if necessary.
            config: The corresponding config to the historical provider.
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
            interval_ms = int(config.interval.value.total_seconds() * 1000)

            earliest_available = storage.get_earliest_available(ticker, interval)

            missing_timestamps = storage.get_missing_timestamps(
                ticker, interval, expected_timestamps, earliest_available=earliest_available
            )
            if len(missing_timestamps) != 0:
                min_timestamp = min(missing_timestamps)
                max_timestamp = max(missing_timestamps)
                new_config = replace(
                    config,
                    start_timestamp=min_timestamp,
                    end_timestamp=max(max_timestamp + interval_ms, min_timestamp + interval_ms),
                )

                try:
                    new_data = provider.get_bars(new_config)
                except Exception:
                    new_data = []

                if new_data:
                    storage.add_data_to_storage(interval, new_data)
                    discovered_earliest = min(event.timestamp for event in new_data)
                    if earliest_available is None or discovered_earliest < earliest_available:
                        storage.set_earliest_available(ticker, interval, discovered_earliest)
                        earliest_available = discovered_earliest
                else:
                    confirmed_empty_bound = new_config.end_timestamp + interval_ms
                    if earliest_available is None or confirmed_empty_bound > earliest_available:
                        storage.set_earliest_available(ticker, interval, confirmed_empty_bound)
                        earliest_available = confirmed_empty_bound

            data = storage.get_data(ticker, interval, start_timestamp, end_timestamp)

        return data
