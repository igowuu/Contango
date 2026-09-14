# Intents

An intent is any emitted behavior for a strategy. For example, entering a specific trade would be an intent. Intents are abstracted in an `Intent` base class so that rule-based strategies can rely on a modular system to communicate with the `Strategy` base class.

See [Intents Reference](../../reference/strategy/rule_based/intents/intent.md)

## Enter Long Intent

The `EnterLongIntent` intent indicates for the rule based strategy to emit a long order for a provided symbol. The amount of shares to buy is calculated by a `PositionSizer`.

See [Enter Long Intent Reference](../../reference/strategy/rule_based/intents/enter_long_intent.md)

## Exit Long Intent

Similarly, the `ExitLongIntent` intent indicates for the rule based strategy to emit a sell order for a provided symbol. The amount of shares to sell is calculated by a `PositionSizer`.

See [Exit Long Intent Reference](../../reference/strategy/rule_based/intents/exit_long_intent.md)
