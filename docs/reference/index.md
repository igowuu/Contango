# Project Documentation

This project is organized into five main areas: a broker layer for direct access to historical / live data, a data layer for storage, a research layer for strategy prototyping, and a trading layer for execution/backtesting/optimization.

## Market calendars and historical data providers.

- **Calendar**
  - [Calendar](broker/calendar/calendar.md)
  - [NYSE Calendar](broker/calendar/nyse_calendar.md)
- **Historical Brokers**
  - [Config Type](broker/historical_brokers/config_type.md)
  - [Historical Broker](broker/historical_brokers/historical_broker.md)
  - **Yfinance**
    - [yfinance](broker/historical_brokers/yfinance/yfinance.md)
    - [yfinance Config](broker/historical_brokers/yfinance/yfinance_config.md)

## Market data access and storage.

- [Data Repository](data/data_repository.md)
- **Storage**
  - [Store Market Data](data/storage/store_market_data.md)

## Strategy research and experimentation.

- [Research Runner](research/research_runner.md)
- **Research Strategies**
  - **Bollinger Band Mean Reversion**
    - [Runner](research/research_strategies/bollinger_band_mean_reversion/runner.md)
    - [Strategy](research/research_strategies/bollinger_band_mean_reversion/strategy.md)

## Trading engine: analysis, execution, indicators, and optimization.

- **Data**
  - [Analyze and Graph](trading/analyzer/data/analyze_and_graph.md)
  - [Data Prep](trading/analyzer/data/data_prep.md)
- **Graphing**
  - [Equity Curve Overlay](trading/analyzer/graphing/equity_curve_overlay.md)
  - [Metric Distribution](trading/analyzer/graphing/metric_distribution.md)
  - [Pairwise Heatmap Grid](trading/analyzer/graphing/pairwise_heatmap_grid.md)
  - [Parallel Coordinates](trading/analyzer/graphing/parallel_coordinates.md)
  - [Parameter Importance](trading/analyzer/graphing/parameter_importance.md)
  - [Risk / Return Overview](trading/analyzer/graphing/risk_return_overview.md)
  - [Trade Quality Scatter](trading/analyzer/graphing/trade_quality_scatter.md)
  - [Underwater Drawdown](trading/analyzer/graphing/underwater_drawdown.md)

## Trading execution

- **Backtester**
  - [Config](trading/execution/backtester/config.md)
  - **Market**
    - [Feed](trading/execution/backtester/market/feed.md)
  - **Orders**
    - [Order Filler](trading/execution/backtester/orders/order_filler.md)
    - [Stop-Loss Order Manager](trading/execution/backtester/orders/stoploss_order_manager.md)
  - **Portfolio**
    - [Portfolio](trading/execution/backtester/portfolio/portfolio.md)
  - [Strategy Backtester](trading/execution/backtester/strategy_backtester.md)
- **Engine**
  - **Events**
    - [Event Bus](trading/execution/engine/events/event_bus.md)
    - [Events](trading/execution/engine/events/events.md)
  - **Orders**
    - [Order API](trading/execution/engine/orders/order_api.md)
  - **Results**
    - [Execution Data](trading/execution/engine/results/execution_data.md)
    - [Results Collector](trading/execution/engine/results/results_collector.md)
  - **Strategy**
    - [Strategy](trading/execution/engine/strategy/strategy.md)
    - [Strategy Injector](trading/execution/engine/strategy/strategy_injector.md)

## Indicators & indicator state

- **Calculations**
  - [Average True Range](trading/indicators/calculations/average_true_range.md)
  - [Bollinger Bands](trading/indicators/calculations/bollinger_bands.md)
  - [EMA](trading/indicators/calculations/ema.md)
  - [RSI](trading/indicators/calculations/rsi.md)
  - [SMA](trading/indicators/calculations/sma.md)
  - [True Range](trading/indicators/calculations/true_range.md)
  - [VWAP](trading/indicators/calculations/vwap.md)
  - [Wilder Average](trading/indicators/calculations/wilder_average.md)
- [Indicator](trading/indicators/indicator.md)
- **State**
  - [Bollinger Bands State](trading/indicators/state/bollinger_bands_state.md)
  - [EMA State](trading/indicators/state/ema_state.md)
  - [RSI State](trading/indicators/state/rsi_state.md)
  - [SMA State](trading/indicators/state/sma_state.md)
  - [VWAP State](trading/indicators/state/vwap_state.md)
  - [Wilder Average State](trading/indicators/state/wilder_average_state.md)

## Strategy optimization, experiments, & metrics

- **Analysis**
  - [Builder](trading/optimizer/analysis/builder.md)
  - [Calculate Metrics](trading/optimizer/analysis/calculate_metrics.md)
  - **Calculators**
    - [Drawdown](trading/optimizer/analysis/calculators/drawdown.md)
    - [Returns](trading/optimizer/analysis/calculators/returns.md)
    - [Risk](trading/optimizer/analysis/calculators/risk.md)
    - [Trades](trading/optimizer/analysis/calculators/trades.md)
  - [Context](trading/optimizer/analysis/context.md)
  - [Metrics](trading/optimizer/analysis/metrics.md)
- **Experiments**
  - [Backtest Experiment](trading/optimizer/experiments/backtest_experiment.md)
  - [Backtest Experiment Grid](trading/optimizer/experiments/backtest_experiment_grid.md)
  - [Backtest Experiment Result](trading/optimizer/experiments/backtest_experiment_result.md)
  - [Backtest Experiment Runner](trading/optimizer/experiments/backtest_experiment_runner.md)
