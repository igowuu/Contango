# broker/calendar/nyse_calendar.py — part of Contango, a parameterized backtesting & execution framework
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

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import exchange_calendars as xcals  # type: ignore[missingTypeStubs]
import pandas as pd

from broker.historical_brokers.config_type import Interval
from broker.calendar.calendar import Calendar


class NYSECalendar(Calendar):
    """
    Trading calendar for the New York Stock Exchange (9:00AM-4:00PM on weekdays, holidays taken into account).
    """
    def __init__(self) -> None:
        """
        Initializes `NYSECalendar.
        """
        self._calendar = xcals.get_calendar("XNYS", start="1990-01-01")

    def get_expected_timestamps(
        self,
        start_timestamp: int,
        end_timestamp: int,
        interval: Interval,
    ) -> list[datetime]:
        """
        Returns the expected available NYSE timestamps for the specified period.
        
        Args:
            start_timestamp: The start time in unix ms.
            end_timestamp: The end time in unix ms.
            interval: The bar interval type.
        
        Returns:
            list[datetime]: The dates & times of the available NYSE trading bar times for the designated period.
        """
        start_ny = pd.Timestamp(start_timestamp, unit="ms", tz=ZoneInfo("UTC")).tz_convert(ZoneInfo("America/New_York"))
        end_ny = pd.Timestamp(end_timestamp, unit="ms", tz=ZoneInfo("UTC")).tz_convert(ZoneInfo("America/New_York"))

        start_date = start_ny.tz_localize(None).normalize()
        end_date = end_ny.tz_localize(None).normalize()

        frequency = pd.Timedelta(interval.value)

        timestamps = self._calendar.trading_index(
            start=start_date,
            end=end_date,
            period=frequency,
            force=True,
        )

        return [
            ts.to_pydatetime().astimezone(timezone.utc) # type: ignore[unknownMemberType]
            for ts in timestamps
        ]
