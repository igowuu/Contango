# Chart 2b: Parallel Coordinates Plot

**File:** `chart_02b_parallel_coordinates.py`
**Question it answers:** What do the full parameter combinations that work actually look like?

## What's On The Chart

One vertical axis per swept parameter, plus one final axis for the target
metric (default `calmar_ratio`). Each experiment is drawn as a single line
crossing all axes left to right, colored by its value on the target metric
(red = poor, green = good, by default using a red-yellow-green scale).

## How To Read It

This is the hardest chart in the set to read well — go slowly.

1. **Ignore individual lines at first. Look for color bands.** Scan each axis
   top to bottom and notice whether green lines tend to pass through a narrow
   band of that axis, or whether they're spread across the entire range of
   that axis.
2. **A narrow green band on an axis = that parameter value range matters.**
   If nearly all green lines pass through `slow_ema_period` values between 180
   and 220, that's a strong, visually obvious signal — and should roughly
   agree with what chart 2a's importance ranking told you about that
   parameter.
3. **Follow a few individual green lines across all axes.** This is where
   parallel coordinates earns its place in the flow: you can see whether the
   *same* lines that are narrow on axis 1 are also narrow on axis 3, meaning
   those two parameters move together for good outcomes (an interaction), or
   whether a line that's great on axis 1 wanders freely on axis 3 (no
   interaction — axis 3 doesn't matter much once axis 1 is right).
4. **Compare against chart 2a.** If 2a said one parameter dominates, you
   should see that parameter's axis show the tightest green band here. If 2b
   shows a tight band on an axis that 2a ranked low, that's worth
   investigating — it likely means that parameter's effect is *conditional*
   (an interaction effect) rather than a strong effect on its own, which is
   exactly the kind of thing eta-squared on a single parameter can miss.

## What Good Results Look Like

- Green lines visibly cluster through a narrow band on at least 2-3 axes, and
  that cluster is consistent across the group (not just one or two lines).
- The narrow bands roughly agree with the top parameters from chart 2a.
- Red lines are diffusely spread everywhere — i.e., there's no equally
  strong "band" that predicts bad outcomes, which would suggest the good
  region is a real signal rather than everything being noisy in both directions.

## What Bad / Warning Signs Look Like

- **Green lines scattered across the full range on every axis, no narrow
  bands anywhere.** No coherent parameter story — the good results you saw in
  chart 1 don't correspond to any identifiable parameter region, meaning
  they're more consistent with noise than with a real, describable edge.
- **A single green line that's an outlier on most axes**, not part of any
  band with other green lines. Same interpretation as the "isolated great
  point" warning from chart 1 — likely a lucky specific combination rather
  than a real region.
- **Too many lines to read (hundreds+).** If your `param_space` produces
  hundreds or thousands of combinations, the plot becomes an unreadable mess
  of overlapping strands. Use the `sample_size` parameter on
  `build_parallel_coordinates` to randomly subsample down to something
  readable (a few hundred lines max) — you're looking for a pattern, and a
  representative sample shows the same pattern as the full set.

## Decision Rule

- Bands you find here become your hypothesis for chart 2c's facet structure —
  if 2b suggests an interaction between two parameters that chart 2a didn't
  rank as the top two, override the auto-selected axes in chart 2c and pass
  those two explicitly instead.
- No bands anywhere → treat this as agreement with a "no cluster" result from
  chart 1, and lean toward stopping rather than proceeding to chart 2c.

## What This Chart Can't Tell You

It shows you *that* an interaction or region exists, and roughly where — but
it can't tell you if that region is robust (a few nearby parameter values also
performing well) or fragile (a knife-edge that only works at exact values).
That's chart 2c's job specifically.
