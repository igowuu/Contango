# Engine

The engine holds the events, results, strategy base classes, and any other universal API / utility for a mode of trading. For example, one mode of trading showcased in this project is the backtester. The idea is that a strategy can be written through the engine, and any mode of trading can handle the same exact logic however it would like.

## Events

Events are tuples of data that can be published and subscribed to by different modules & methods through an event bus. 

For example, a `MarketDataEvent` can be published by one method, and all of its subscribers will receive the event sequentially by their explicit priorities. This allows for chaining of different event types without synchronously in a codebase, which significantly declutters the code and prioritizes readability.

Some of the main events (but not necessarily limited to):

- `MarketDataEvent` - Emitted for every OHLCV bar in a dataset (contains the close, open, high, low, volume, for a single symbol).
- `OrderEvent` - A simple market order emitted after a user submits it through the order API. 
- `StoplossOrderEvent` - A stoploss order emitted after a user submits it through the order API.
- `AcceptedFillEvent` - An accepted and filled order.
- `RejectedFillEvent` - An order that was rejected and was not filled.
- `PortfolioSnapshotEvent` - A snapshot of the portfolio for the current period in time.

See [event reference](../../reference/trading/execution/engine/events/events.md)
and [event bus reference](../../reference/trading/execution/engine/events/event_bus.md)

## Orders

Orders are published by the order API component. The order API has a separate method for each event type that it can publish to the bus - for example, `OrderEvent` and `StoplossOrderEvent`. The order API is traditionally injected into a `Strategy` implementation by a separate component so that it can create orders and publish order events.

See [order API reference](../../reference/trading/execution/engine/orders/order_api.md)

## Results

The engine inherently returns raw tuples of the events published for an execution. The results will always be in order by timestamp made or executed. Other modules must interpret these raw events; the execution engine does not hold this responsibility.

See [execution data reference](../../reference/trading/execution/engine/results/execution_data.md)

## Strategy

A strategy is the base class that creates orders for the rest of the engine or mode to handle. Custom logic is made to determine when these orders should be made; the execution engine handles the data collection & event logic. 

Variables such as `order_api` and `portfolio_snapshot` are injected and updated consistently to allow orders to be made and access the updated portfolio state respectively.

See [strategy reference](../../reference/trading/execution/engine/strategy/strategy.md)

## See More

[Backtester](./backtester.md)
