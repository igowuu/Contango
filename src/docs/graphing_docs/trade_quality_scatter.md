# Chart 6: Trade Quality Scatter

**File:** `chart_06_trade_quality_scatter.py`
**Question it answers:** Why did it make money?

## What's On The Chart

- **X-axis:** `win_rate` — the fraction of trades that were profitable.
- **Y-axis:** `profit_factor` (default) or `expectancy` — reward relative to
  losses taken.
- **Bubble size:** `trade_count` — how many trades the experiment actually made.
- **Color:** `calmar_ratio` by default.

## How To Read It

1. **Note the bubble size before anything else.** A high-quality-looking dot
   (great win rate, great profit factor) with a *tiny* bubble is a warning, not
   a finding — a great record over 10-15 trades tells you very little about
   what the strategy will do over the next 100. Prioritize reading medium-to-large
   bubbles; treat small bubbles as statistically unreliable regardless of where
   they sit on the axes.
2. **Identify which "shape" of edge each surviving candidate has:**
   - **High win rate, modest profit factor (lower-right area):** a "grinder" —
     wins often, but wins are roughly similar in size to losses. Steady but
     unspectacular per-trade edge.
   - **Low-to-moderate win rate, high profit factor (upper-left area):** a
     "swinger" — loses more often than it wins, but wins are much larger than
     losses when they land. Classic trend-following signature.
   - **High on both axes (upper-right):** rare, and worth extra scrutiny — an
     unusually strong combination like this, especially on a small bubble, is
     more consistent with a fortunate backtest window than genuine skill.
3. **Compare mechanism across your shortlist.** Two candidates with similar
   total return can sit in completely different places on this chart — meaning
   they'd feel completely different to trade day-to-day (frequent small wins
   vs. rare big wins with a lot of losing trades in between).

## What Good Results Look Like

- A large-to-medium bubble sitting clearly in either the "grinder" or
  "swinger" region, with values that make sense together (e.g., a 35% win
  rate paired with a profit factor of 2.5+ is a coherent swinger profile; a
  35% win rate paired with a profit factor of 1.05 means it's barely breaking
  even and every metric upstream showing it as "good" deserves a second look).
- A trade count large enough that you'd trust the win rate and profit factor
  numbers as reasonably stable estimates rather than small-sample noise
  (there's no universal cutoff, but tens of trades is usually too few to trust;
  low hundreds starts to be meaningful, depending on strategy frequency).

## What Bad / Warning Signs Look Like

- **Excellent-looking dot, tiny bubble.** This is the single most important
  thing this chart catches. Revisit this candidate's position in every earlier
  chart with the knowledge that its whole track record rests on very few
  trades — a metric that looked like a standout in chart 1 may simply be small-sample
  variance.
- **Win rate near 50% with a profit factor near 1.0.** This combination is
  close to a coin flip with no real edge (before costs). If a candidate lands
  here despite looking good on Sharpe/Calmar upstream, check whether those
  ratios are being inflated by a short backtest window rather than genuine
  edge.
- **Profit factor very high but win rate very low (e.g., under ~20%) on a
  small bubble.** Extreme profit factors on few trades are usually one or two
  outsized winning trades doing all the work — closer to the "single lucky
  jump" pattern from chart 4 than a repeatable mechanism.

## Decision Rule

- Large bubble, coherent grinder or swinger profile → strong candidate for
  chart 7.
- Small bubble, regardless of how good the axes look → down-weight heavily, or
  exclude from the final radar even if it survived every earlier chart.
- Cross-reference: a candidate that showed a single dominant jump in chart 4
  should show a low win rate / high profit factor / small trade count profile
  here — if it doesn't, that's worth reconciling before trusting either chart's
  read.

## What This Chart Can't Tell You

It doesn't tell you whether the specific edge (grinder or swinger) is one
you're personally comfortable trading — that's a judgment call, not something
any chart resolves. It also doesn't factor in `average_holding_period`; two
candidates with similar profiles here could differ hugely in how long they tie
up capital per trade, which chart 7 folds back in as a normalized dimension.
