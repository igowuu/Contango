# Chart 2a: Parameter Importance Ranking

**File:** `chart_02a_parameter_importance.py`
**Question it answers:** Which knobs actually matter?

## What's On The Chart

A horizontal bar chart, one bar per swept parameter (`fast_ema_period`,
`slow_ema_period`, `rsi_period`, `lower_rsi_threshold`, `upper_rsi_threshold` in
the EMA/RSI example — `allocation` is excluded automatically since it wasn't
actually varied). Bar length = an eta-squared style importance score between 0
and 1: the share of total variance in your target metric (default
`calmar_ratio`) that's explained by grouping experiments on that parameter's
value alone.

## How To Read It

1. **Read top to bottom** — it's sorted descending, so the top bar is the
   single most influential parameter on your outcome metric.
2. **Look at the gap sizes, not just the order.** A ranking where the top bar
   is 0.35 and the rest trail off to 0.02 tells a very different story than one
   where all five bars sit between 0.15 and 0.22. The former says "one
   parameter dominates"; the latter says "the outcome depends on a genuine
   interaction across several parameters," which changes how you should read
   chart 2b and which parameters you pick for chart 2c.
3. **Sanity-check against domain knowledge.** If `rsi_period` ranks near zero
   for an RSI-based strategy, that's either a real (interesting) finding or a
   sign something's off in how the strategy consumes that parameter — worth a
   second look before trusting it blindly.

## What Good Results Look Like

- A clear top 2-3 parameters with meaningfully larger bars than the rest. This
  gives you exactly what you need for chart 2c: two axes plus a facet
  parameter, chosen with justification rather than guesswork.
- Scores that make intuitive sense given what the parameter actually does
  (e.g., for a trend-following EMA strategy, the EMA periods dominating over
  RSI thresholds would be unsurprising).

## What Bad / Warning Signs Look Like

- **All bars near zero.** No single parameter explains much variance in
  isolation. This usually means either (a) the metric is dominated by
  interaction effects between parameters rather than any one parameter alone —
  in which case chart 2b becomes your primary tool, not this bar chart — or
  (b) there just isn't a strong parameter-driven pattern at all, which echoes
  a "no cluster" result from chart 1 and is worth cross-checking against it.
- **All bars roughly equal and moderately high.** Every parameter matters
  about the same amount. This isn't necessarily bad, but it does mean chart 2c
  (which only facets on 3 parameters at a time) will only be showing you part
  of the picture — you may need to run 2c multiple times with different
  parameter triads to get a full sense of robustness.
- **One parameter overwhelmingly dominates (score near 1.0) and the rest are
  near zero.** This can be a real, simple relationship — but it's also
  consistent with that one parameter being confounded with something else in
  how the strategy or backtest is structured (e.g., a parameter that
  indirectly controls how many trades get taken at all, which mechanically
  moves every downstream metric). Worth a sanity check against chart 6 (trade
  count) before treating it as a clean finding.

## Decision Rule

- Take the **top 2** parameters as your x/y axes for chart 2c.
- Take the **3rd-ranked** parameter as your facet parameter for chart 2c.
- If scores are near-uniform across all parameters, treat chart 2b (parallel
  coordinates) as your primary tool instead — 2c will need to be re-run with
  different parameter combinations to get full coverage, since it can't
  represent all parameters in a single grid.

## What This Chart Can't Tell You

It tells you which parameters matter *in isolation*, not how they interact.
A parameter can score low here while still being part of a strong 2-way
interaction (e.g., `lower_rsi_threshold` might only matter when
`rsi_period` is short) — that's exactly what chart 2b is for.
