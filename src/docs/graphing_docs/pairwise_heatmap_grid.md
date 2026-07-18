# Chart 2c: Pairwise Heatmap Grid (Small Multiples)

**File:** `chart_02c_pairwise_heatmap_grid.py`
**Question it answers:** Is the interaction real, or a coincidence of one fixed combination?

This is the single most important chart in the flow for parameterized
backtests specifically. If you only had time for one chart, this would be it.

## What's On The Chart

A grid of small 2D heatmaps. Each panel is a heatmap of `param_x` (columns)
vs. `param_y` (rows), colored by the target metric (default `calmar_ratio`,
red-to-green). There is one panel per unique value of a third parameter
(`facet_param`) — so you're looking at the same 2D relationship repeated
across different "slices" of a third dimension.

## How To Read It

1. **Find the warm (green) region in the first panel.** Note roughly where it
   sits — which `param_x` / `param_y` values it covers.
2. **Check every other panel for the same warm region.** This is the entire
   point of the chart: does that same region of green cells show up (even if
   slightly shifted or slightly less intense) in most or all of the other
   panels? Or does it only appear in one panel and vanish in the rest?
3. **Look at the shape of the warm region within a single panel too.** A
   smooth blob of green cells that fades gradually into yellow/red at the
   edges is very different from a single isolated bright-green cell surrounded
   on all sides by red. The former is a real, gradual relationship between the
   parameters and the outcome. The latter is much more consistent with noise —
   a real underlying relationship should vary smoothly as you nudge a
   parameter slightly, not swing from great to terrible between adjacent
   values.

## What Good (Robust) Results Look Like

- The same warm region appears across most or all panels, even if its exact
  boundaries shift a little panel to panel.
- Within any single panel, the warm region is a contiguous blob of
  medium-to-high cells, not an isolated pixel.
- The edges of the warm region fade gradually (green → yellow → red) rather
  than switching abruptly.

## What Bad (Fragile / Overfit) Results Look Like

- **A hot cell that only appears in one panel** and is cold/red in every
  other panel. This is the textbook signature of overfitting a parameterized
  strategy: the "great" result depended on one very specific combination of
  three-plus parameter values simultaneously, and any deviation collapses
  performance. **Discard this candidate even if chart 1 flagged it as a
  standout point** — that standout point is very likely this exact cell.
- **A checkerboard pattern** (alternating hot/cold cells with no spatial
  structure) within a panel. This suggests the relationship between these
  parameters and the outcome is essentially noise — real market-driven edges
  tend to vary smoothly with parameter values, not flip unpredictably between
  neighbors.
- **No warm region anywhere, in any panel.** Combined with earlier charts
  showing a cluster, this specific combination of parameters isn't where the
  edge lives — worth revisiting chart 2a/2b to see if you picked the wrong
  three parameters for this grid, before concluding there's no edge at all.

## Decision Rule

- **Warm region persists across panels →** this is your confirmed robust
  parameter region. Take the experiments inside it forward to chart 3.
- **Warm region only appears in 1 panel →** discard. Do not carry this region
  forward, regardless of how good its single best point looked in chart 1.
- **No warm region in any panel, despite chart 1/2b suggesting a real
  pattern →** re-run this chart with a different parameter triad (chart 2a's
  4th/5th ranked parameters, or a pairing chart 2b's line-following suggested)
  before concluding there's no robust region at all.

## A Practical Note on Facets

This grid only shows 3 parameters at once (2 axes + 1 facet). If chart 2a
showed several parameters with meaningfully high importance (not just a clear
top 3), it's worth re-running this chart with different parameter triads to
confirm robustness isn't an artifact of which third parameter you happened to
facet on. Don't treat a single run of this chart as exhaustive if you have 4+
important parameters.

## What This Chart Can't Tell You

Robustness across nearby *parameter* values doesn't guarantee reliability
across *time* — a genuinely robust parameter region can still have been
consistently good in one favorable regime and would fail in a different market
condition. That's what chart 3 (distribution) starts to probe, and what
charts 4-5 (equity curve, underwater) let you inspect directly.
