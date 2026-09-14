# Contango

<div align="center">
    <img src="https://raw.githubusercontent.com/igowuu/Contango/refs/heads/main/docs/media/metric_distribution.avif" width="32%">
    <img src="https://raw.githubusercontent.com/igowuu/Contango/refs/heads/main/docs/media/equity_curve.avif" width="32%">
    <img src="https://raw.githubusercontent.com/igowuu/Contango/refs/heads/main/docs/media/trade_quality.avif" width="32%">
</div>

<div align="center">
    <img src="https://raw.githubusercontent.com/igowuu/Contango/refs/heads/main/docs/media/parallel_parameter_combinations.avif" width="32%">
    <img src="https://raw.githubusercontent.com/igowuu/Contango/refs/heads/main/docs/media/risk_return_overview.avif" width="32%">
    <img src="https://raw.githubusercontent.com/igowuu/Contango/refs/heads/main/docs/media/underwater_plot.avif" width="32%">
</div>

<h6 align="center">
    <a href="https://igowuu.github.io/Contango/">Documentation</a>
    ·
    <a href="https://github.com/igowuu/Contango/blob/main/LICENSE">License</a>
</h6>

<p align="center">
    <a href="https://github.com/igowuu/Contango/commits/main">
        <img src="https://img.shields.io/github/last-commit/igowuu/Contango" alt="Last Commit">
    </a>
    <img src="https://img.shields.io/badge/python-3.11%2B-blue" alt="Python 3.11+">
    <a href="https://github.com/igowuu/Contango">
        <img src="https://img.shields.io/github/stars/igowuu/Contango" alt="Stars">
    </a>
    <a href="https://github.com/igowuu/Contango">
        <img src="https://img.shields.io/pypi/l/contango" alt="License">
    </a>
    
</p>

Contango is a Python framework for backtesting, parameter optimization, and quantitative analysis of trading strategies.

## Features

- Cartesian parameter sweeps by evaluating every combination of selected strategy parameters.
- Local data repository to cache OHLCV data locally for faster repeated backtests and offline research.
- Full Yfinance data support (no API key needed) with easy additional data provider creation.
- An entire metrics & graphing suite (equity curves, drawdown/underwater plots) to evaluate large amounts of strategy results at once.

This is not meant to be an extensive list, so see the [documentation](https://igowuu.github.io/Contango/) for everything not covered above.

## Installation

> Requires: Python 3.11+

```bash
pip install contango
```

> See [developer installation docs](https://igowuu.github.io/Contango/getting-started/installation/) to build the project without pip.

## Quickstart

### Run the demo

```shell
python -m contango.research.demo_strategies cartesian_bollinger_strategy.runner 
```

The demo runs a Bollinger Band strategy across a Cartesian grid of parameters and generates performance and parameter-analysis graphs. The generated graphs (as HTML files) are saved to the root directory. To see the graphs, open the generated files in a browser.

The demo strategy itself is written as a `RuleBasedStrategy`.

### Create a Strategy

The framework has two ways to create strategies. Subclassing `RuleBasedStrategy` allows for less boilerplate with the cost of implicitness, but is generally easier to comprehend at scale. If you would rather have more control (but generally more code to write), subclassing `Strategy` is the best way to do so:

```python
class MyStrategy(Strategy):
    """
    A simplified strategy outline - not all logic is included.
    """
    def on_market_event(self, event: MarketDataEvent) -> None:
        # Strategy market logic here
        if should_buy:
            self.order_api.submit_order(event, "AAPL", quantity=3)
            self.order_api.submit_stoploss_order(event, "AAPL", quantity=-3, stoploss_price=...)
        elif should_sell:
            self.order_api.submit_order(event, "AAPL", quantity=-3)
```

## Usage

See the [documentation](https://igowuu.github.io/Contango/) for an extensive breakdown on how to use the framework.

## Credits

- Historical data is sourced from [Yahoo Finance](https://finance.yahoo.com/).

**Developers:**

<div style="width:100px;">
  <a href="https://github.com/igowuu">
    <img width="100" height="100" src="https://github.com/user-attachments/assets/b507347a-6ba6-446e-be0a-7d2b0b26452e">
  </a>
  <div>
    <a>&nbsp;&nbsp;&nbsp;&nbsp;</a>
    <a href="https://github.com/igowuu">igowuu</a>
  </div>
</div>

## License

See [LICENSE](https://github.com/igowuu/Contango/blob/main/LICENSE)

---
