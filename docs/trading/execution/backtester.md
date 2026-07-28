# Backtester

The backtester is a "mode" or way to iterate through a dataset using the engine. It allows for data to be processed without actual tools, brokers, or additional software, instead simulating all of it to model real life as accurately as possible.

## Backtester Config

A config is specialized for the backtester to determine simulated portfolio state, fill behavior, slippage modeling, commissions, etc. It must be passed to the strategy backtester upon conducting a backtest.

See [backtester config reference](../../reference/trading/execution/backtester/config.md)

## Strategy Backtester

The main backtester module. Via the static `.backtest(...)` method, a single backtest can be executed given a config, strategy, and OHLCV data. It will return execution data after iterating through the strategy & OHLCV data.

**Nuances**: The backtester does NOT support pyramiding (which means you must sell all of the shares you bought in a previous trade - no exceptions), nor multiple tickers, nor any short trades. This will obviously be changed very soon in the future, although the backtester is powerful nonetheless. Orders that violate these rules will be rejected by the backtester.

See [backtester reference](../../reference/trading/execution/backtester/strategy_backtester.md)
