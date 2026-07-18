from __future__ import annotations

from typing import Generic, TypeVar
from abc import ABC, abstractmethod

from execution.engine.events import MarketDataEvent
from broker.historical_brokers.config_type import Config


TConfig = TypeVar("TConfig", bound=Config)


class HistoricalBroker(ABC, Generic[TConfig]):
    """
    A single broker (or data provider) for historical market data.
    """
    @abstractmethod
    def get_bars(self, config: TConfig) -> list[MarketDataEvent]:
        """
        Returns a list of market data events for any configuration parameters.
        """
        ...
