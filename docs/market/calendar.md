# Calendars

## What is it?

A calendar is a set of available trading dates for a certain method of trading. For example, one calendar may include only weekdays from 9:00AM to 4:00PM excluding holidays (stocks). They allow for the [database](../data/repository.md) to retrieve any necessary data that isn't already in the storage, effectively limiting the amount of historical API calls made.

See [calendar reference](../reference/market/calendar/calendar.md)

### NYSE Calendar

The NYSE calendar includes all weekdays from 9:00AM to 4:00PM, excluding holidays. This is commonly used for trading stocks.

See [NYSE calendar reference](../reference/market/calendar/nyse_calendar.md)


## Creating a Calendar

To create your own calendar, subclass the `Calendar` abstract class and implement the `get_expected_timestamps` method:


```python
class MyCalendar(Calendar):
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
        # Your implementation here
        ...
```

One recommended resource for implementing your own calendars is the `exchange_calendars` library, which is used for the NYSE calendar and is a dependency for the project.
