# Conditions

A condition is any boolean when creating a strategy. The definition is intentionally very broad, as a condition can be literally anything, whether it be a change in price or an indicator crosses above another.

Conditions can be composed together. This means that the dunder `__and__`, `__or__`, and `__invert__` are overriden, so two conditions can be composed together using the key words `and`, `or`, and `not`. 

See [Conditions Reference](../../reference/strategy/rule_based/conditions/condition.md)

## Predicate

A predicate is simply a condition that is supplied a lambda function that returns a boolean. Upon being evaluated, that boolean is freshly generated. Essentially, a Predicate is the simplest possible `Condition`, and should be used in most use cases.

See [Predicate Reference](../../reference/strategy/rule_based/conditions/predicate.md)
