# Contexts

In a general sense, any context is an immutable value that is supplied to various objects in a rule-based strategy. Specifically, concepts such as position sizers & possibly rules need to be supplied contexts every iteration. A context implementation must contain all of the necessary values for these modules to operate correctly.

See [Context Reference](../../reference/strategy/rule_based/contexts/context.md)

## Trading Context

`TradingContext` is the primary context that almost all modules related to rule-based strategy creation use. It simply contains the current market event (OHCLV bar) and the current snapshot of the portfolio, which is generally enough to compute most essential things in a strategy. The majority, if not all, of the tools included in rule-based strategy creation use exclusively `TradingContext`.

See [Trading Context Reference](../../reference/strategy/rule_based/contexts/trading_context.md)
