# Weekly trend review 2026-W47

- Week ends: 2026-11-19 (UTC), report built 2026-11-20T07:32:25Z
- Live tracking since 2026-10-29: **21 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -12.3% |  | -20.9% | -25.4% | 100% |  |
| sma_50 | +0.0% | +12.3 pp | +0.2% | -0.4% | 0% | 0 |
| sma_100 | -0.4% | +11.9 pp | -7.6% | -10.3% | 5% | 0 |
| sma_blend | -1.0% | +11.3 pp | -4.7% | -6.3% | 6% | 17 |
| donchian_ens | +0.0% | +12.3 pp | -0.9% | -1.2% | 1% | 1 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **5%** (out of 20)
- Average 7-day move across coins: -12.1% (median -12.9%)
- BTC: 61,913 USD, 7-day -13.3%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 215 signals noticed within 12 h of the close; median adverse move +0.24%, 47% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 15 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 15 runs in 7 days. Check the GitHub Actions tab.
