# broker/calendar/calendar.py — part of Contango, a parameterized backtesting & execution framework
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

from abc import ABC, abstractmethod
from datetime import datetime

from contango.broker.historical_brokers.config_type import Interval


class Calendar(ABC):
    """
    A delegation of the available trading times for calendar type (i.e. NYSE or Crypto).
    """
    @abstractmethod
    def get_expected_timestamps(
        self,
        start_timestamp: int,
        end_timestamp: int,
        interval: Interval,
    ) -> list[datetime]:
        """
        Returns the expected available timestamps in a calendar for a specified period.
        
        Args:
            start_timestamp: The start time in unix ms.
            end_timestamp: The end time in unix ms.
            interval: The bar interval type.
        
        Returns:
            list[datetime]: The dates & times of the available trading bars for the designated period.
        """
        ...
