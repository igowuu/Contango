# Contango

Contango is a python engine for backtesting, optimizing, and graphing trading strategies. This covers everything not already in the README - the strategy/event module, optimizer, brokers, calenders, indicators, and how to read the generated graphs.

If you are new, start with the **Getting Started** section. If you already have a strategy running and want to understand a specific piece (events, the optimizer, a graph type), jump straight inot the relevant section below.

## Getting Started

- **[Installation](./getting-started/installation.md)** - environment setup, depencencies.

- **[Quickstart](./getting-started/quickstart.md)** - run the demo strategy and serve the generated graphs locally.

## Core Concepts

- **[Engine](./trading/execution/engine.md)** - event types, the event bus, and the `Strategy` base class.

- **[Brokers](./broker/historical-brokers.md)** - how historical brokers (e.g. `Yfinance`) fetch OHLCV data & how to use them.

- **[Calendars](./broker/calendar.md)** - how calendars (e.g. `NYSECalendar`) define tradeable dates, and how the data repository avoids re-fetching cached data.

- **[Backtester](./trading/execution/backtester.md)** - how fills, slippage, and commission are simulations, current limitations, and how the backtester works.

- **[Indicators & State Machines](./trading/indicators/indicators.md)** - built-in indicators (ATR, Bollinger Bands, EMA, RSI, SMA, VWAP, Wilder Average) and the state machines strategies can signal off of.

## Trading

- **[Optimizer](trading/optimizer/analysis.md)** - how the optimizer works & what each computed metric (sharpe, calmar, PnL, expectancy, etc.) means.
- **[Graphing](trading/analyzer/graphing.md)** - how to read each of the seven graph types, what to look for in each of the graphs, and examples to walk through each of the graph types.

## Reference

- **[Reference Documentation](./reference/index.md)**
