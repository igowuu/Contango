# Chart 7: Final Cross-Strategy Comparison Radar

**File:** `chart_07_final_comparison_radar.py`
**Question it answers:** Given everything, which one wins?

## What's On The Chart

A radar (spider) chart with one axis per metric (default: `sharpe_ratio`,
`calmar_ratio`, `win_rate`, `profit_factor`, `average_holding_period`, plus
`max_drawdown` always included) and one filled polygon per experiment in your
final shortlist (3-5 recommended). Every axis is min-max normalized to 0-1
**across just this shortlist** — so a value of 1.0 on an axis means "the best
of this final group on this metric," not some fixed universal benchmark.
`max_drawdown` is inverted before normalizing, so on every axis, further from
the center is always better — there's no axis where you have to remember "wait,
lower is better here."

## How To Read It

1. **Look at overall polygon area first.** A larger filled area generally
   means a candidate is doing well across more dimensions simultaneously —
   but don't stop here (see below).
2. **Then look at shape, not just size.** A large but lopsided polygon (very
   strong on 1-2 axes, weak on the rest) tells a different story than a
   moderately sized but balanced polygon (decent on everything). Which one you
   prefer depends on what you actually value — a balanced profile is generally
   safer/more robust; a lopsided one is a specialist that might be worth
   pairing with a different specialist strategy rather than run alone.
3. **Check for a candidate that's weak specifically on `max_drawdown`.** Since
   this axis is inverted and included by default, a polygon that pinches in
   sharply on that one axis while being large everywhere else is a candidate
   with good average behavior but a rough worst-case — worth weighing against
   how much you can tolerate what chart 5 showed for that specific candidate.
4. **Remember every number here is relative to the shortlist, not absolute.**
   A candidate scoring 1.0 on `sharpe_ratio` just means it has the best Sharpe
   *among these 3-5 finalists* — go back to the actual metric values (not the
   normalized chart) if you need to know whether that Sharpe is good in an
   absolute sense.

## What Good Results Look Like

- One candidate with a clearly larger, reasonably balanced polygon relative to
  the others — a fairly clean winner.
- If two candidates are close in overall area, look at which specific axes
  each one wins — this often reframes the decision from "which is better" to
  "which trade-off do I prefer" (e.g., one wins on Sharpe/Calmar, the other
  wins on drawdown control and win rate).

## What Bad / Warning Signs Look Like

- **No candidate has a clearly larger polygon — they're all roughly the same
  size with different shapes.** This isn't a flaw in the chart; it's an honest
  signal that your shortlist doesn't have a dominant winner, and the choice
  genuinely comes down to which trade-off (return vs. drawdown vs. consistency)
  you personally prioritize. Don't force a "winner" narrative onto this result.
- **A candidate that looked strong throughout the earlier funnel scores
  surprisingly low here.** This can happen because normalization is relative
  to just the finalists — if your shortlist is unusually strong, a genuinely
  good candidate can look mediocre next to other genuinely good candidates.
  Don't read a low relative score here as contradicting everything upstream;
  check the raw metric values before concluding anything changed.

## Decision Rule

- Clear largest, reasonably balanced polygon → that's your strategy/parameter
  choice.
- Close contest between 2+ shapes → make the trade-off explicit (write down,
  in plain language, what you're gaining and giving up by picking one over the
  other) rather than picking based on polygon area alone.

## What This Chart Can't Tell You

It's a summary of everything upstream, not a replacement for it — it doesn't
show *why* a candidate scores the way it does (that's charts 1-6), and because
every axis is normalized only within the shortlist, it can't tell you whether
even your best finalist is good in an absolute sense, or just the best of a
weak set. Sanity-check the winner's raw metrics (and its chart 4/5 shapes)
before finalizing, rather than trusting the radar shape alone.
