from __future__ import annotations

from datetime import datetime, timezone
from typing import cast
from zoneinfo import ZoneInfo

import exchange_calendars as xcals  # pyright: ignore[reportMissingTypeStubs]
import pandas as pd

from contango.broker.historical_brokers.config_type import Interval
from contango.broker.calendar.calendar import Calendar


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
            list[datetime]: The close times of the available NYSE trading bars for the designated period.
        """
        start_ny = pd.Timestamp(start_timestamp, unit="ms", tz=ZoneInfo("UTC")).tz_convert(ZoneInfo("America/New_York"))
        end_ny = pd.Timestamp(end_timestamp, unit="ms", tz=ZoneInfo("UTC")).tz_convert(ZoneInfo("America/New_York"))

        start_date = start_ny.tz_localize(None).normalize()
        end_date = end_ny.tz_localize(None).normalize()

        frequency = pd.Timedelta(interval.value)

        raw_index = self._calendar.trading_index(
            start=start_date,
            end=end_date,
            period=frequency,
            intervals=True,
            force=True,
        )

        close_timestamps: pd.DatetimeIndex
        if isinstance(raw_index, pd.IntervalIndex):
            close_timestamps = cast(pd.DatetimeIndex, raw_index.right)
        else:
            close_timestamps = raw_index.tz_localize(timezone.utc)

        start_utc = start_ny.tz_convert(ZoneInfo("UTC"))
        end_utc = end_ny.tz_convert(ZoneInfo("UTC"))

        close_times: list[datetime] = [
            ts.to_pydatetime().astimezone(timezone.utc)
            for ts in close_timestamps
            if start_utc <= ts <= end_utc
        ]

        return close_times
