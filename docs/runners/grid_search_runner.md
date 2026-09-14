# Grid Search Runner

The grid search runner runs all possible combinations for a strategy instance, given lists of the parameters to run. This is a pure cartesian search, meaning that all combinations (order does not matter) are tested amonst themselves.

## Usage

First, data must be retrieved from a specified source. Either `fetch_data` (for one ticker) or `fetch_data_multi` (for multiple tickers) may be called to fetch the data to test.

Next, the `run()` method should be called to perform the backtest & retrieve the results for each parameter combination:

```python
def run(
    ohlcv_data: Mapping[str, list[MarketDataEvent]],
    strategy_cls: type[StrategyT],
    param_grid: Mapping[str, Sequence[Any]],
    backtester_config: BacktesterConfig,
    base_label: str | None = None,
    verbose: bool = True
) -> list[ExperimentResult]:
```

Most of the parameters are self-explanatory. The `param_grid` is a mapping (dictionary) of parameter names for the strategy class to the parameters you want to test. For example:

```python
results = GridSearchRunner.run(
    ohlcv_data=data,
    strategy_cls=BollingerBandMeanReversion,
    param_grid={
        "bollinger_bands_period": [15, 20, 25],
        "bollinger_bands_stdev": [1.0, 1.5, 2.0, 2.5],
        "allocation": [0.25, 0.5, 0.75],
        "symbol": tickers
    },
    ...
)
```

Each string (i.e. "bollinger_bands_period") is a parameter kwarg inside of the `BollingerBandMeanReversion` class, and each of those parameters in the corresponding list will be tested. In this specific case, for example, 3 * 4 * 3 * len(tickers) will be tested.

See [grid search reference](../reference/runners/grid/grid_search_runner.md)
