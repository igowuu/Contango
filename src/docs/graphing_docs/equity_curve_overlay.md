# Chart 4: Equity Curve Overlay

**File:** `chart_04_equity_curve_overlay.py`
**Question it answers:** What does the ride actually look like?

## What's On The Chart

One line per shortlisted experiment (default: top 8 by `calmar_ratio`),
plotting account value (`equity_curve`, cash + units) over time. This is the
first chart in the flow that shows genuine time-series behavior rather than a
single summary number per experiment.

## How To Read It

1. **Look at the overall shape of each line first, not the endpoint.** Two
   lines can end at the same final value via completely different paths — one
   a steady staircase upward, the other flat for 80% of the backtest then one
   enormous jump. Chart 1-3 cannot distinguish these; this chart is built
   specifically to.
2. **Check whether the line's slope is roughly consistent** across the whole
   time window, or concentrated in a short burst.
3. **Compare shapes across your shortlist.** If several candidates share a
   similar "shape" (e.g., all flat through the same specific week, then all
   jump together), that's informative — it likely means they're all reacting
   to the same underlying market event, which tells you something about how
   correlated your "shortlist" actually is (they may not be as diversified a
   set of choices as their different parameter values suggest).

## What Good Results Look Like

- A smooth, mostly-monotonic upward slope with no single day/week dominating
  the total return. If you covered up any one week of the chart, the overall
  shape should still look like "steadily up."
- Multiple shortlisted candidates showing broadly similar, steady shapes —
  suggests the edge is coming from the strategy's actual logic operating
  consistently, not from a lucky market event a specific parameter set happened
  to catch.

## What Bad / Warning Signs Look Like

- **A single vertical jump** responsible for most of the total gain, with a
  flat or choppy line everywhere else. This is the "one lucky trade" pattern —
  the summary metrics from earlier charts (total return, Sharpe, Calmar) don't
  distinguish this from genuine consistent skill, but visually it's obvious.
  Treat any candidate showing this pattern with real skepticism, regardless of
  how good its numbers looked upstream.
- **A long flat (or declining) stretch followed by a late recovery.** Even if
  the line ends high, ask whether you'd have had the conviction to keep the
  strategy running through that flat/declining stretch in real time, not knowing
  the recovery was coming. This connects directly to chart 5, which quantifies
  exactly this pattern.
- **Wildly different shapes across your shortlist** despite similar final
  metrics. This can mean your shortlist candidates are picking up genuinely
  different, uncorrelated sources of return (potentially good — worth
  understanding why) or that some of them are noise-driven outliers that
  happen to land on similar final numbers by coincidence (worth investigating
  via chart 6, trade quality).

## Decision Rule

- Smooth, consistent shapes → carry forward to chart 5 and 6 with confidence.
- Any candidate dominated by a single jump → flag for likely exclusion from
  the final radar (chart 7), even if its summary stats are excellent.

## What This Chart Can't Tell You

It shows account value, which by construction can mask how *bad* a decline
felt relative to the peak that came before it — a decline from $150k to $130k
looks small on an equity curve dominated by a later run to $300k, but is a
~13% drawdown that would have been painful to hold through in real time. Chart
5 exists specifically to make that visible.
