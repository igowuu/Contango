# Action

An actions is something that executes a single behavior through the `execute` method, which recieves a context type.

See [Action Reference](../../reference/strategy/rule_based/actions/action.md)

# Emit

Emit is a simple action that emits a singular `Intent` type upon being executed. No context is used, although it is still passed into the `execute` method. For example, an Emit action may simply emit an `EnterLongIntent` intent type, and that would be it's sole purpose.

See [Emit Reference](../../reference/strategy/rule_based/actions/emit.md)
