# Position Sizers

A position sizer decides how many units to either buy or sell upon an intent (`EnterLongIntent` or `ExitLongIntent`) being published. It will buy and sell the same amount of units, as pyramiding is uniformly unsupported throughout the codebase.

See [Position Sizer Reference](../../reference/strategy/rule_based/position_sizers/position_sizer.md)

## Allocation Position Sizer

An allocation position sizer trades a fixed portion of the portfolio upon buying and selling. For example, if 0.3 (30%) is specified, it will attempt in trading 30% of the portfolio value upon an enter long order, and -30% of the portfolio value upon an exit long order.

See [Allocation Position Sizer Reference](../../reference/strategy/rule_based/position_sizers/allocation_position_sizer.md)

## Fixed Position Sizer

A fixed position sizer trades a fixed amount of units upon buying and selling. For example, if 3 units is specified, it will attempt in trading 3 units upon an enter long order, and -3 units upon an exit long order.

See [Fixed Position Sizer Reference](../../reference/strategy/rule_based/position_sizers/fixed_position_sizer.md)

## Volatility Position Sizer

A volatility position sizer scales the amount of units to buy or sell inversely to volatility. Hardcoded position sizers assume a favorable velocity, but fail on highly volatile or too-little volatile periods. The volatility position sizer uses the same algorithm as TSMOM - if you want to use this, I implore you to go check it out.

See [Volatility Position Sizer Reference](../../reference/strategy/rule_based/position_sizers/volatility_position_sizer.md)
