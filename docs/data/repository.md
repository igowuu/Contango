# Data Repository

## What is it?

The data repository allows for OHLCV data (`MarketDataEvent` instances) to be stored and easily retrieved instead of always polling historical brokers. Further, it permits the use of data offline if retrieving historical data through the internet is not accessible at the time.

The `get_data_and_store` method must be called with a broker, the brokers respective configuration, and the expected timestamps for the call (generally derived from the `calender` attribute in a broker instance). The `get_data_and_store` method will check the storage, use any data available in the storage first, and then poll brokers for the additional data. The additional data will then be fed into the storage for further use.

See [data repository reference](../reference/data/data_repository.md)
