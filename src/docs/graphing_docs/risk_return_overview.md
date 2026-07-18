# Chart 1: Risk/Return Overview Scatter

**File:** `chart_01_risk_return_overview.py`
**Question it answers:** Is anything here even worth looking at?

## What's On The Chart

- **X-axis:** `annual_return` — the CAGR of the strategy over the backtest period.
- **Y-axis:** `sharpe_ratio` — return per unit of volatility (risk-adjusted).
- **Bubble size:** severity of `max_drawdown` (larger bubble = worse worst-case loss).
- **Color:** `calmar_ratio` by default (or a chosen parameter, if you passed `color_by`).

Every dot is one full backtest experiment (one parameter combination).

## How To Read It

Look at the chart in this order:

1. **Is there a cluster in the upper-right?** Upper-right means high return *and*
   high Sharpe simultaneously — this is the region of experiments that made
   money efficiently, not just experiments that made money.
2. **Within that cluster, which bubbles are small?** Small bubble = mild worst
   drawdown. A dot in the upper-right with a huge bubble is a strategy that made
   good risk-adjusted returns on average but had at least one catastrophic
   period — worth flagging, not necessarily disqualifying yet (chart 5 will
   tell you more about that specific drawdown).
3. **Is the cluster made of one color or many?** If you colored by a parameter,
   a cluster dominated by a single color tells you that parameter value is
   doing a lot of the work — a preview of what chart 2a will quantify properly.

## What Good Results Look Like

- A visible, non-trivial group of points in the upper-right quadrant, distinct
  from the rest of the scatter — not just the single best point, but a *region*.
  A lone great point surrounded by mediocre ones is a warning sign (see below),
  not a good sign.
- Small-to-medium bubbles within that cluster.
- The cluster should represent a meaningful fraction of total experiments —
  even 5-10% is fine, but if only 1-2 out of hundreds land there, that's a
  fragility signal, not a robustness signal.

## What Bad / Warning Signs Look Like

- **No visible clustering at all** — points scattered roughly evenly across the
  whole plot area, upper-right no denser than anywhere else. This means the
  parameter space you swept doesn't contain a real edge. **Stop here.** Don't
  proceed to chart 2 hoping tuning will find one; you'll just be tuning to noise.
- **A single isolated great point** far from any neighbors, with everything
  else mediocre or bad. This is very likely a lucky combination, not a real
  edge — chart 2c (pairwise heatmap) will almost certainly show this as an
  isolated hot pixel with cold neighbors. Treat this point as *interesting but
  unconfirmed*, not as a winner.
- **Large bubbles concentrated in the upper-right.** High return, high Sharpe,
  but also high worst-case loss — this is a strategy that "worked" but took a
  large risk to get there. Sharpe already penalizes volatility somewhat, but
  it doesn't fully capture tail risk, which is exactly what the bubble size is
  for. Don't let a good Sharpe number talk you out of noticing a big bubble.

## Decision Rule

- **Clear cluster, small bubbles →** proceed to chart 2a with this strategy family.
- **No cluster →** stop. Reconsider the strategy logic itself, not the parameters.
- **Single isolated great point, no surrounding cluster →** proceed cautiously;
  treat this point as a hypothesis to be stress-tested (and likely rejected) by
  chart 2c, not as a finding.

## What This Chart Can't Tell You

It can't tell you *why* the good cluster is good (that's chart 6), whether it's
consistent over time (chart 3) or robust to nearby parameter values (chart 2c),
or what the actual ride looked like (charts 4-5). It is purely a triage step —
resist the temptation to make a final decision from this chart alone.
