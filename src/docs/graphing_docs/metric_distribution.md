# Chart 3: Metric Distribution (Box / Violin Plot)

**File:** `chart_03_metric_distribution.py`
**Question it answers:** How consistent is this, not just how good on average?

## What's On The Chart

One box (or violin) per group — typically grouped by your most important
parameter from chart 2a — showing the distribution of a metric (default
`total_return`) across the experiments in that group. Each box shows the
median (center line), interquartile range (box body), and whiskers/outliers.
With `points="all"` (the default in the provided code), every individual
experiment is also overlaid as a dot so you can see the raw data, not just the
summary shape.

## How To Read It

1. **Compare medians across groups first** — this is the same information
   chart 1/2a already gave you in a different form, so don't dwell here.
2. **Now look at box width and whisker length — this is the new information.**
   A narrow box with short whiskers means most experiments in that group
   landed close to the median. A wide box or long whiskers means results in
   that group varied a lot — some experiments did great, others did poorly,
   under what's nominally "the same" parameter setting (varying only in the
   other parameters, or in market regime slices if you're grouping by time).
3. **Check the individual points, not just the box.** A box can look
   reasonably tight while still containing a couple of severe outliers pulling
   the visual median. The overlaid points let you see whether a "good" group
   is uniformly good or good-with-exceptions.

## What Good Results Look Like

- The group(s) that looked best in charts 1/2a also show the **tightest**
  boxes here — good on average *and* consistent.
- Whisker length that's small relative to the box's distance from zero (e.g.,
  a group with median return of 15% and whiskers only spanning 10-20% is far
  more trustworthy than one with median 15% and whiskers spanning -10% to 40%).

## What Bad / Warning Signs Look Like

- **The best-median group also has the widest box.** This is the "great
  average, terrible reliability" trap this chart exists to catch. It means the
  good average you saw in earlier charts is being pulled up by a few very good
  runs while plenty of others in the same group did poorly (or lost money) —
  not a strategy behavior you can count on repeating.
- **Whiskers or outlier points crossing into negative territory** for a group
  whose median return is positive. Even a "winning" parameter group having
  individual experiments that lost money is worth noting, especially if you
  plan to trade a single parameter setting live rather than an ensemble.
- **Similar box widths across all groups.** If every group — good and bad
  median alike — shows similarly wide spread, that's a sign the parameter
  you're grouping by isn't actually controlling consistency, only average
  level. Worth grouping by a different parameter (perhaps the 2nd-ranked one
  from chart 2a) to see if that tells a cleaner story.

## Decision Rule

- Groups with both a good median *and* a tight box move forward to charts 4-5.
- A group with a good median but wide box should be treated with suspicion —
  worth checking whether its "hits" and "misses" correspond to something
  identifiable (e.g., particular time periods, if you have that available)
  before trusting it.

## What This Chart Can't Tell You

It shows *that* results vary within a group, but not *when* or *why*. A wide
box could mean genuine day-to-day inconsistency, or it could mean the strategy
did great for the first half of the backtest window and poorly for the second
(a regime shift) — those have very different implications, and only the
equity curve (chart 4) and underwater plot (chart 5) can distinguish them.
