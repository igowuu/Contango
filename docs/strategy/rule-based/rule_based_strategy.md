# Rule-Based Strategies

A rule-based strategy provides a higher-level interface for building strategies from streams, rules, intents, and position sizing. It has similar, if not identical capabilities to a typical `Strategy` subclass with less boilerplate and more modularity. Essentially, it makes it easier to create strategies if rapidly iterating to find a profitable one.

The rule-based strategy system, however, is slightly more opinionated than a normal `Strategy` subclass. It inherently wraps some logic and may have small limitations; however, given that all of the base classes are subclassable, it should be quite easy to add to the framework without touching the codebase internals.

See [rule-based strategy reference](../../reference/strategy/rule_based/rule_based_strategy.md)

## How to create rule-based strategies

Every rule-based strategy must have the following, as illustrated in the `__init__` method for the class:

```python
def __init__(
    self,
    streams: Sequence[Stream[Any]],
    rules: Sequence[Rule[TradingContext, Intent | None]],
    position_sizer: PositionSizer[TradingContext],
)
```

It should have some source of [streams](../../stream/streams.md) (anything that needs to be updated with `MarketDataEvent` instances as they're published), [rules](../../strategy/rule-based/rules.md) that determine when to buy & sell in a strategy, and a [position sizer](../../strategy/rule-based/position_sizers.md) to determine how many units to buy upon a buy/sell [intent](../../strategy/rule-based/intents.md) being published.

### Example & design process

Firstly, you want declare what **streams** your strategy may need. Does it need historical access to market events (most strategies do)? Does it need specific indicators to function? These are all questions that you should clarify before building the actual strategy logic. For a Bollinger Band Mean Reversion strategy, we need historical access to previous market events to detect previous crosses in price and, of course, access to the Bollinger Bands indicator:

```python
self.bollinger = HistoricalIndicator(
    source=BollingerBands(
        bollinger_bands_period, 
        bollinger_bands_stdev
    ), 
    window=2
)
self.events = HistoricalMarketEvents(window=2)
```

Next, we need to create the actual **rules** for the strategy. For our Bollinger Band Mean Reversion strategy, we want to buy upon the close crossing below the lower band, and sell upon the close crossing back above the middle band. This can be expressed like English:

```python
rules: Sequence[Rule[TradingContext, Intent]] = [
    Rule(
        when=Predicate(self.price_crosses_below_lower_band),
        then=Emit(EnterLongIntent(symbol=symbol))
    ),
    Rule(
        when=Predicate(self.price_crosses_above_middle_band),
        then=Emit(ExitLongIntent(symbol=symbol)),
    )
]
```

Essentially, it reads exactly like psuedocode: **when** the close crosses the lower band, **then** emit an `EnterLongIntent` for a given symbol. **When** the close goes back above the middle band, **then** emit an `ExitLongIntent` for a given symbol. This is the beauty of rule-based strategies: they're incredibly easy to reason about and understand, even for new developers.

Because RuleBasedStrategy performs the framework initialization in its constructor, subclasses must call `super().__init__()` with their streams, rules, and position sizer.

```python
super().__init__(
    streams=[self.bollinger, self.events],
    rules=rules,
    position_sizer=AllocationPositionSizer(allocation),
)
```

Bundling everything together, a full strategy for a Bollinger Band Mean Reversion would look like this:

```python
class BollingerBandMeanReversion(RuleBasedStrategy):
    def __init__(
        self, 
        bollinger_bands_period: int, 
        bollinger_bands_stdev: float,
        allocation: float,
        symbol: str
    ) -> None:
        self.bollinger = HistoricalIndicator(
            source=BollingerBands(
                bollinger_bands_period, 
                bollinger_bands_stdev
            ), 
            window=2
        )
        self.events = HistoricalMarketEvents(window=2)

        rules: Sequence[Rule[TradingContext, Intent]] = [
            Rule(
                when=Predicate(self.price_crosses_below_lower_band),
                then=Emit(EnterLongIntent(symbol=symbol))
            ),
            Rule(
                when=Predicate(self.price_crosses_above_middle_band),
                then=Emit(ExitLongIntent(symbol=symbol)),
            )
        ]

        super().__init__(
            streams=[self.bollinger, self.events],
            rules=rules,
            position_sizer=AllocationPositionSizer(allocation),
        )

    def price_crosses_below_lower_band(self, context: TradingContext) -> bool:
        current_bb, prev_bb = self.bollinger.value, self.bollinger.previous()
        current_event, prev_event = context.event, self.events.previous()

        if current_bb is None or prev_bb is None or prev_event is None:
            return False

        return prev_event.close >= prev_bb.lower and current_event.close < current_bb.lower

    def price_crosses_above_middle_band(self, context: TradingContext) -> bool:
        current_bb, prev_bb = self.bollinger.value, self.bollinger.previous()
        current_event, prev_event = context.event, self.events.previous()

        if current_bb is None or prev_bb is None or prev_event is None:
            return False

        return prev_event.close <= prev_bb.middle and current_event.close > current_bb.middle
```
