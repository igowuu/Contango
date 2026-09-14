# Strategies

The `Strategy` subclass is the most dynamic and least opinionated method of creating strategies; however, it has the cost of being verbose. All logic must be implemented by the user, essentially.

Subclasses of `Strategy` can implement event handlers to initialize state, process market data, and react to order/trade events. The possible hooks / fields to be overriden or accessed respectively are:

- `on_start()`: called once before any data is processed.
- `on_end()`: called once after all data has been processed.
- `on_market_event()`: triggered upon a market event (bar).
- `on_order_event()`: triggered when an order is submitted.
- `on_fill_event()`: triggered when an order is filled.

- `order_api`: allows for communication with the engine to make orders.
- `portfolio_snapshot`: the current snapshot of the account that holds all positions & cash.

See [strategy reference](../reference/strategy/strategy.md)

## Example & design process

Firstly, you want to determine what state your strategy actually needs to maintain. Unlike a rule-based strategy, a normal `Strategy` subclass does not provide streams, rules, intents, or position sizing automatically. All of this logic is left to the strategy itself.

For a Bollinger Band Mean Reversion strategy, we need access to the Bollinger Bands indicator, the previous Bollinger Band snapshot, and the previous market event. We also need to know whether the portfolio is currently holding a position:

```python
self._bollinger_bands = BollingerBands(
    bollinger_bands_period, 
    bollinger_bands_stdev
)

self._previous_snapshot: BollingerBandSnapshot | None = None
self._previous_event: MarketDataEvent | None = None
```

Next, we need to determine the actual conditions for buying and selling. Since a normal `Strategy` has no concept of rules or predicates, this logic can be implemented however the developer prefers. For our strategy, we can separate the buy and sell conditions into their own methods:

```python
def _should_buy(
    self, 
    prev_close: float,
    current_close: float,
    previous: BollingerBandSnapshot, 
    current: BollingerBandSnapshot, 
    holding: bool
) -> bool:
    return (
        prev_close >= previous.lower
        and current_close < current.lower
        and not holding
    )

def _should_sell(
    self, 
    prev_close: float,
    current_close: float,
    previous: BollingerBandSnapshot, 
    current: BollingerBandSnapshot, 
    holding: bool
) -> bool:
    return (
        prev_close <= previous.middle
        and current_close > current.middle
        and holding
    )
```

These methods essentially perform the same job as the rules in a rule-based strategy. **If** the previous close was above the lower band and the current close is below it, we want to buy. **If** the previous close was below the middle band and the current close is above it, we want to sell.

However, because this is a normal `Strategy` subclass, we must also handle updating indicators, maintaining historical state, determining position sizes, and submitting orders ourselves.

The `on_market_event()` method is where the majority of this logic can be implemented. First, the Bollinger Bands need to be updated with the current market event:

```python
close = event.close
snapshot = self._bollinger_bands.update(event)
```

We then need to make sure that we have enough historical information to compare the current market event against the previous one. If the indicator is not ready, or this is the first event received, we simply save the current state and wait for the next event:

```python
if self._previous_event is None or self._previous_snapshot is None or snapshot is None:
    self._previous_event = event
    self._previous_snapshot = snapshot
    return
```

Once the required state is available, we can determine whether the strategy is currently holding a position and evaluate the buy/sell conditions:

```python
prev_close = self._previous_event.close
holding = self.portfolio_snapshot.position > 0
prev_snapshot = self._previous_snapshot

if self._should_buy(prev_close, close, prev_snapshot, snapshot, holding):
    ...
elif self._should_sell(prev_close, close, prev_snapshot, snapshot, holding):
    ...
```

If a buy signal occurs, the strategy must also determine how many units to purchase. In this example, the strategy uses an allocation percentage of the currently available cash:

```python
units_to_buy = int(self._allocation * self.portfolio_snapshot.cash / close)
self.order_api.submit_order(event, self._symbol, units_to_buy)
```

Likewise, when a sell signal occurs, the strategy can directly submit an order for the entire current position:

```python
units_to_sell = self.portfolio_snapshot.position
self.order_api.submit_order(event, self._symbol, -units_to_sell)
```

Finally, the previous market event and indicator snapshot need to be updated so they are available during the next call to `on_market_event()`:

```python
self._previous_snapshot = snapshot
self._previous_event = event
```

One additional consideration is what happens when the strategy reaches the end of the data. Since this strategy is intended to hold no position after the backtest has finished, `on_end()` can close any remaining position. Rule-based strategies do this implicitly, but it must be expicitly done here:

```python
def on_end(self) -> None:
    holding = self.portfolio_snapshot.position > 0
    final_event = self._previous_event
    
    if final_event is None:
        raise ValueError("The final market data event was never set.")

    if holding:
        units_to_sell = self.portfolio_snapshot.position
        self.order_api.submit_order(final_event, self._symbol, -units_to_sell)
```

A full strategy for a Bollinger Band Mean Reversion would look like this:

```python
class BollingerBandMeanReversion(Strategy):
    def __init__(
        self,
        bollinger_bands_period: int,
        bollinger_bands_stdev: float,
        allocation: float,
        symbol: str
    ) -> None:
        self._bollinger_bands = BollingerBands(
            bollinger_bands_period,
            bollinger_bands_stdev
        )
        self._allocation = allocation
        self._symbol = symbol

        self._previous_snapshot: BollingerBandSnapshot | None = None
        self._previous_event: MarketDataEvent | None = None

    def _should_buy(
        self, 
        prev_close: float,
        current_close: float,
        previous: BollingerBandSnapshot, 
        current: BollingerBandSnapshot, 
        holding: bool
    ) -> bool:
        return (
            prev_close >= previous.lower
            and current_close < current.lower
            and not holding
        )
    
    def _should_sell(
        self, 
        prev_close: float,
        current_close: float,
        previous: BollingerBandSnapshot, 
        current: BollingerBandSnapshot, 
        holding: bool
    ) -> bool:
        return (
            prev_close <= previous.middle
            and current_close > current.middle
            and holding
        )

    def on_market_event(self, event: MarketDataEvent) -> None:
        close = event.close
        snapshot = self._bollinger_bands.update(event)

        if self._previous_event is None or self._previous_snapshot is None or snapshot is None:
            self._previous_event = event
            self._previous_snapshot = snapshot
            return

        prev_close = self._previous_event.close
        holding = self.portfolio_snapshot.position > 0
        prev_snapshot = self._previous_snapshot

        if self._should_buy(prev_close, close, prev_snapshot, snapshot, holding):
            units_to_buy = int(self._allocation * self.portfolio_snapshot.cash / close)
            self.order_api.submit_order(event, self._symbol, units_to_buy)
        elif self._should_sell(prev_close, close, prev_snapshot, snapshot, holding):
            units_to_sell = self.portfolio_snapshot.position
            self.order_api.submit_order(event, self._symbol, -units_to_sell)
        
        self._previous_snapshot = snapshot
        self._previous_event = event

    def on_end(self) -> None:
        holding = self.portfolio_snapshot.position > 0
        final_event = self._previous_event
        
        if final_event is None:
            raise ValueError("The final market data event was never set.")

        if holding:
            units_to_sell = self.portfolio_snapshot.position
            self.order_api.submit_order(final_event, self._symbol, -units_to_sell)
```
