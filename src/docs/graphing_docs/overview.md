# Backtest Analysis Flow — Overview

This describes the order to look at the 9 charts in, and why that order matters:
each step operates on a **narrower, more scrutinized set of experiments** than the
one before it. You are not looking at 9 independent charts — you are running a
funnel. Skipping steps or reordering them will cause you to draw conclusions
(usually "this is a great strategy") that later steps would have disproven.

## The Funnel, At a Glance

| # | Chart | Question It Answers | Input Set | Output |
|---|---|---|---|---|
| 1 | Risk/Return Overview Scatter | Is anything here even worth looking at? | All experiments | Rough cluster of candidates |
| 2a | Parameter Importance Ranking | Which knobs actually matter? | All experiments | Ranked parameter list |
| 2b | Parallel Coordinates | What do full winning combinations look like? | All experiments | Candidate parameter region(s) |
| 2c | Pairwise Heatmap Grid | Is that region stable or a fluke? | All experiments | Confirmed robust region, or discard |
| 3 | Metric Distribution | How consistent is this, not just how good on average? | Experiments in the robust region | Reliability check |
| 4 | Equity Curve Overlay | What does the ride actually look like? | Shortlist (top ~8) | Visual pattern (steady vs. lucky spike) |
| 5 | Underwater Plot | How much pain, and for how long? | Same shortlist | Tolerability check |
| 6 | Trade Quality Scatter | Why did it make money? | Shortlist or full set | Mechanism (grinder vs. swinger) |
| 7 | Final Comparison Radar | Given everything, which one wins? | Final shortlist (3-5) | The decision |

## The Core Discipline: Elimination, Not Accumulation

Every chart before #7 exists to **remove** candidates, not just to admire the
survivors. A healthy pass through this flow should shrink your candidate set at
almost every step:

- Start: hundreds or thousands of parameter combinations.
- After #1: a visually plausible cluster (could be dozens to hundreds).
- After #2a-2c: a confirmed robust parameter region (could be a handful of
  combinations, or **zero** — that's a valid and useful outcome).
- After #3: candidates that survive both "good on average" and "reliable."
- After #4-5: candidates whose actual behavior over time is something you'd be
  willing to trade live.
- After #6: candidates whose *mechanism* you understand and trust.
- #7: the final decision among 3-5 survivors.

If your candidate set isn't shrinking as you move through the funnel, that's a
signal you're being too lenient at each step — go back and tighten your
thresholds rather than carrying a large set all the way to the end.

## Stopping Early Is a Valid Outcome

If chart 1 shows no cluster at all — points scattered with no visible upper-right
concentration — stop. Don't proceed to chart 2. A strategy family with no visible
risk/return edge at the broadest level will not be rescued by parameter tuning;
tuning noise just finds you a lucky-looking corner of the noise (this is exactly
what chart 2c is designed to catch if you proceed anyway).

Similarly, if chart 2c shows no region where the "warm zone" survives across
facets — every hot cell is an isolated pixel — stop there. You do not have a
robust strategy; you have an overfit one. Go back to strategy design, not
parameter re-tuning.

## Per-Chart Documentation

Each chart has its own doc with explicit reading instructions, worked examples of
what good/bad/ambiguous results look like, and a decision rule for what to do
next:

- `01_risk_return_overview.md`
- `02a_parameter_importance.md`
- `02b_parallel_coordinates.md`
- `02c_pairwise_heatmap_grid.md`
- `03_metric_distribution.md`
- `04_equity_curve_overlay.md`
- `05_underwater_drawdown.md`
- `06_trade_quality_scatter.md`
- `07_final_comparison_radar.md`
