# Streams

A stream can be defined as anything that needs a constant feed of `MarketDataEvent` instances as they come. This is particularly useful for indicators or historical caches that need constant flows of data. 

## Usage

Streams can only be used with rule-based strategies, as it is not set up anywhere else. If used elsewhere (such as with static strategies), all streams must be updated manually via the `.update` method.

To create your own stream, inheret from the `Stream` abstract class:

```python
class MyStream(Generic[R]):
    """
    A stream that accepts market data events as they are released and produces some type of output.

    Attributes:
        R: The output type for the stream.
    """
    def update(self, event: MarketDataEvent) -> R:
        """
        Updates the state of the stream given a market data event.

        Returns:    
            The updated value.
        """
        # Some implementation here
        ...
    
    @property
    @abstractmethod
    def value(self) -> R:
        """
        Returns the most recent value of the stream.
        """
        # Some implementation here
        ...
```

See [stream reference](../reference/stream/stream.md)

## Historical Streams

A historical stream maintains a lookback, given a `Stream` implementation. It maintains the n amount of previous values efficiently and allows them to be accessed through accessors. 

One example of this is the [historical market events stream](../reference/stream/historical_market_events.md), which maintains the last n amount of market events by creating a dummy stream specifically to store market events.

See [historical stream reference](../reference/stream/historical_stream.md)
