# broker/historical_brokers/historical_broker.py — part of Contango, a parameterized backtesting & execution framework
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

from typing import Generic, TypeVar, Iterable
from abc import ABC, abstractmethod
from datetime import datetime

from contango.trading.execution.engine.events import MarketDataEvent
from contango.broker.historical_brokers.config_type import Config


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
    
    @abstractmethod
    def get_expected_timestamps(
        self,
        config: TConfig,
    ) -> Iterable[datetime]:
        """
        Returns an Iterable of the expected timestamps for the start & finishing timestamps of a configuration.
        """
        ...
