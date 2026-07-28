# Optimizer Analysis

The optimizer generates metrics to help with both graphing (visual analysis) & strategy optimization. It contains the necessary information, derived from raw events, to determine profitability, risk, and factor out any results that indicate overfitting or unreliability.

# Metrics

A tuple containing the generated metrics for a strategy execution. It holds the strategy metrics for the following sub-categories:

- `Return Metrics`: Metrics relating to returns (total return, monthy returns, equity curve, etc).
- `Risk Metrics`: Metrics relating to reliability (annual return, sharpe ratio, monthly volatility, calmar ratio, etc).
- `Drawdown Metrics`: Metrics relating to the worst possible outcomes of the strategy (max drawdown, average drawdown).
- `Trade Metrics`: Metrics relating to the general profitability of the strategy (trade count, win rate, profit factor, expectancy, average loss, average win, average holding period, etc).

## Metric Definitions

You may not be familiar with what these metric terms indicate or mean. Here are definitions and interpretations of all of them:

### Return Metrics

- `total return`: The percent of cash that your strategy generated over a time period. Generally speaking, a higher total return is better.
- `monthly returns`: The percent of cash that your strategy generated for each individual month. Consistency across the months is ideal; inconsistencies may point to the strategy favoring specific timestamps rather than others.
- `equity curve`: The cash in your portfolio for every bar timestamp. This shows you how your portfolio fended over time - if there are extreme dips or extreme increases in cash, that may indicate a few massive trades rather than consistent small ones being made.

### Risk metrics

- `annual return`: The average percent of cash that your strategy generates per year. A higher annual return is better; this helps measure consistency across a time period if you see deviations elsewhere.
- `sharpe ratio`: The sharpe ratio is the risk-adjusted return of a strategy - it shows how much excess return an investment generates per unit of total risk taken. Generally speaking, a sharpe ratio over 1.0 is considered good. Below 1.0 suggests that the investment may not justify the risk taken.
- `monthly volatility`: Volatility measures how rapidly and unpredictably your returns move per month. A lower monthly volatility suggests consistency in results; a higher monthly volatility may indicate massive swings and returns rather than consistency.
- `calmar ratio`: The risk-adjusted performance metric that measures an investments annualized return relative to its maximum drawdown. Similarly to the sharpe ratio, it shows if a strategies profits are worth it given it's maximum possible drawdown (loss). Generally speaking, a calmar ratio over 1.0 is considered good.

### Drawdown Metrics

- `max drawdown`: The maximum drawdown is the maximum loss that the strategy made over a backtest. A lower max drawdown indicates a strategy that can handle unfavorable environments without losing hard.
- `average drawdown`: The average of all the drawdowns for a strategy made over a backtest. A lower average drawdown indicates that a strategy consistently handles and reduces losses.

### Trade Metrics

- `trade count`: The amount of trades made over a backtest. A lower trade count may point to the results being inaccurate because of a lack of tests to verify it over.
- `win rate`: The percent chance that a strategy generates a win (over 0.0 profit). A higher win rate is generally better, but it does not always indicate a profitable strategy; you must look at the profit factor first.
- `profit factor`: The profit made per trade compared to the gross loss. For example, a PnL of 1.63 would indicate that the strategy made $1.63 for every $1.0 loss. A PnL below 1.0 is unprofitable, 1.2-1.5 signifies a decent edge, and above that points to a very strong edge (assuming other metrics match).
- `expectancy`: The expected profit per trade with the strategy. A higher expectancy is better as it indicates that a strategy yields consistent profits.
- `average loss`: The average percent lost per loss. An average loss closer to 0.0 is better.
- `average win`: The average percent won per win. A higher average win is better.
- `average holding period`: The average amount of time that a strategy holds per trade. This is proportional to the trade count, and could be either a good or bad sign for your strategy (depending on what you expect your strategy to do).

See [metrics reference](../../reference/trading/optimizer/analysis/metrics.md)
