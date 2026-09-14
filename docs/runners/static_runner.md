# Static Runner

The static runner is designed to run a singular strategy instance that will not be parameterized over different parameter combinations. This is useful for singular tests for already-established strategies rather than fine-tuning strategies.

## Usage

First, data must be retrieved from a specified source. Either `fetch_data` (for one ticker) or `fetch_data_multi` (for multiple tickers) may be called to fetch the data to test.

Next, the `run()` method should be called to perform the backtest & retrieve the results for each parameter combination:

```python
def run(
    ohlcv_data: list[MarketDataEvent], 
    strategy: Strategy, 
    backtester_config: BacktesterConfig
) -> Metrics:
```

This, provided a singualar strategy instance and backtester config, runs the strategy through the backtester once and returns the metrics for that strategy instance.

See [static runner reference](../reference/runners/static/static_runner.md)
