from __future__ import annotations

from typing import Generic, TypeVar, Iterable
from abc import ABC, abstractmethod
from datetime import datetime

from contango.trading.execution.engine.events import MarketDataEvent
from contango.market.data_providers.config import Config


TConfig = TypeVar("TConfig", bound=Config)


class HistoricalDataProvider(ABC, Generic[TConfig]):
    """
    A single broker (or data provider) for historical market data.
    """
    @abstractmethod
    def get_bars(self, config: TConfig) -> list[MarketDataEvent]:
        """
        Returns a list of market data events for any configuration parameters.
        """
        ...
    
    @abstractmethod
    def get_expected_timestamps(
        self,
        config: TConfig,
    ) -> Iterable[datetime]:
        """
        Returns an Iterable of the expected timestamps for the start & finishing timestamps of a configuration.
        """
        ...
