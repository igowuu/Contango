# Chart 5: Underwater Plot (Drawdown Over Time)

**File:** `chart_05_underwater_drawdown.py`
**Question it answers:** How much pain, and for how long?

## What's On The Chart

For the same shortlist as chart 4, one line per experiment showing percent
decline from the running peak account value at every point in time (0% means
"at a new all-time high right now"; a line dipping to -20% means the account
is currently 20% below its best-ever value). The area under each line is
filled, making the depth and duration of underwater periods immediately
visible.

## How To Read It

1. **Depth first: how far below zero does each line go?** This is your
   `max_drawdown` number, but now you can see exactly *when* it happened and
   what the shape of the decline into it looked like (sudden cliff vs. slow
   grind down).
2. **Duration second: how long does each dip last before returning to 0%
   (a new peak)?** A -15% dip that recovers in two weeks is a very different
   experience from a -15% dip that takes four months to recover from, even
   though `max_drawdown` alone reports the same number for both.
3. **Count the dips, not just the deepest one.** A strategy with one clean
   -20% drawdown across the whole backtest is arguably easier to reason about
   than one with five separate -12% drawdowns scattered throughout — the
   latter means you'd be white-knuckling through recoveries repeatedly, not
   just once.

## What Good Results Look Like

- Shallow dips (small distance below zero) that recover quickly (line returns
  to 0% soon after each dip).
- Time spent underwater is a small fraction of total backtest time — the line
  spends most of its time at or near 0%, with occasional brief dips.

## What Bad / Warning Signs Look Like

- **Deep, slow-recovering dips.** A long, gradual decline followed by a long,
  gradual recovery back to 0% represents an extended period where the account
  was below its best value — ask honestly whether that's a period you (or
  whoever is trading this) would tolerate holding through in real time, not
  knowing in advance that recovery was coming.
- **A drawdown that never fully recovers by the end of the backtest window.**
  The line ends below 0% — meaning the strategy was still underwater relative
  to an earlier peak when the backtest period ended. This is a meaningfully
  worse signal than a drawdown that recovered, since you have no evidence from
  this backtest that it *would* recover.
- **Frequent, overlapping dips with little time spent at 0%.** Even if no
  single dip is severe, a strategy that's almost always somewhat underwater is
  a very different (and often more psychologically taxing) experience than one
  with brief clean dips and long stretches at new highs — despite potentially
  having a similar `average_drawdown` number.

## Decision Rule

- Shallow, quick-recovering dips → strong candidate, carry to chart 6.
- Any candidate with a deep, still-unrecovered drawdown at the end of the
  backtest window → treat as high-risk regardless of its other metrics; if
  kept in the running, flag this explicitly going into chart 7.
- Compare dip *timing* across your shortlist: if all candidates show their
  worst drawdown during the same date range, that's a shared vulnerability to
  one market event — worth knowing before assuming your shortlist gives you
  diversified options.

## What This Chart Can't Tell You

It tells you about the pain of holding the strategy, but not *why* the
drawdowns happened — whether from a string of small losing trades, one huge
losing trade, or simply being on the wrong side of a broad market move. That
mechanism-level understanding is what chart 6 is for.
