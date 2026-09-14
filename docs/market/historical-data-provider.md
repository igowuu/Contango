# Historical Data Providers

## What is it?

A historical data provider provides OHLCV data from an external API at the lowest level. Each `HistoricalDataProvider` instance converts the actual data provider's format into the expected format for the rest of the code - a list of `MarketDataEvent` instances. Each data provider corresponds to a separate source - for example, a `Yfinance` HistoricalDataProvider derives data from exclusively Yahoo Finance.

Each historical data provider has a corresponding config, which allows for unique parameters to be passed to each instance.

See [historical data provdier reference](../reference/market/data_providers/historical_data_provider.md).

## Yfinance

The `Yfinance` data provider allows for access to historical data without the necessity of an API key. However, Yfinance has its limitations; data may be sparse (as in, it may occasionally skip bars), strict data and rate limits are enforced, and not all symbols are supported (nor give accurate data).

See [Yfinance reference](../reference/market/data_providers/yfinance/yfinance.md)


## Creating a Historical Data Provider

```python
class MyDataProvider(Generic[TConfig]):
    """
    A data provider from a single source.

    Attributes:
        TConfig: A corresponding config to the data provider. I.e. 
                 Yfinance -> YfinanceConfig.
    """
    @abstractmethod
    def get_bars(self, config: TConfig) -> list[MarketDataEvent]:
        """
        Returns a list of market data events for any configuration parameters. This polls the actual source and converts the results from the source into `MarketDataEvent` instances.
        """
        # Your implementation here.
        ...
    
    @abstractmethod
    def get_expected_timestamps(
        self,
        config: TConfig,
    ) -> Iterable[datetime]:
        """
        Returns an Iterable of the expected timestamps for the start & finishing timestamps of a configuration. Typically speaking, this comes from a designated `Calendar` implementation supplied during initialization.
        """
        ...
```
