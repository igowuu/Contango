from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime

from contango.market.data_providers.config import Interval


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
    ) -> tuple[datetime, ...]:
        """
        Returns the expected available timestamps in a calendar for a specified period.
        
        Args:
            start_timestamp: The start time in unix ms.
            end_timestamp: The end time in unix ms.
            interval: The bar interval type.
        
        Returns:
            tuple[datetime]: The dates & times of the available trading bars for the designated period.
        """
        ...
