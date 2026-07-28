# Historical Brokers

## What is it?

A historical broker provides OHLCV data from an external API at the lowest level. Each `HistoricalBroker` instance converts the actual data provider's format into the expected format for the rest of the code - a list of `MarketDataEvent` instances. Each broker corresponds to a separate data provider - for example, the `Yfinance` broker derives data from exclusively Yahoo Finance.

Each historical broker has a corresponding config, which allows for unique parameters to be passed to each broker instance.

See [broker reference](../reference/broker/historical_brokers/historical_broker.md).

## Yfinance

The `Yfinance` broker allows for access to historical data without the necessity of an API key. However, Yfinance has its limitations; data may be sparse (as in, it may occasionally skip bars), strict data and rate limits are enforced, and not all symbols are supported (nor give accurate data).

See [Yfinance reference](../reference/broker/historical_brokers/yfinance/yfinance.md)
