# Contango

Contango is a python engine to backtest, parameterize, and graph trading strategies.

## Getting Started

- [Installation](getting-started/installation.md)

## Strategies

There's two ways to build a strategy. If you want full control, subclass `Strategy` directly and write everything yourself. If you'd rather create strategies quicker, `RuleBasedStrategy` gives you streams, conditions, rules, intents, and position sizing so you can compose a strategy without writing as much boilerplate.

- [Strategy](strategy/strategy.md)
- [Rule-Based Strategy](strategy/rule-based/rule_based_strategy.md)
    - [Streams](stream/streams.md)
    - [Conditions](strategy/rule-based/conditions.md)
    - [Actions](strategy/rule-based/actions.md)
    - [Rules](strategy/rule-based/rules.md)
    - [Intents](strategy/rule-based/intents.md)
    - [Position Sizers](strategy/rule-based/position_sizers.md)
    - [Contexts](strategy/rule-based/contexts.md)
- [Indicators](stream/indicators/indicators.md)

## Data

Historical data comes from a data provider (Yfinance works with no API key needed), gets checked against a calendar for expected timestamps, and gets cached locally so you're not polling the same data.

- [Data Repository](data/repository.md)
- [Historical Data Providers](market/historical-data-provider.md)
- [Calendars](market/calendar.md)

## Running Backtests

- [Engine](trading/execution/engine.md)
- [Backtester](trading/execution/backtester.md)
- [Static Runner](runners/static_runner.md) - runs a single strategy once.
- [Grid Search Runner](runners/grid_search_runner.md) - runs every combination of a parameter grid.

## Analysis

- [Metric Generation](trading/metrics/generation.md)
- [Graphing](trading/analysis/graphing.md)
