# Weekly trend review 2026-W45

- Week ends: 2026-11-07 (UTC), report built 2026-11-08T22:18:35Z
- Live tracking since 2026-10-29: **9 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -6.4% |  | -2.0% | -7.5% | 100% |  |
| sma_50 | -0.2% | +6.2 pp | +0.2% | -0.4% | 0% | 3 |
| sma_100 | -6.3% | +0.2 pp | -3.6% | -6.7% | 30% | 26 |
| sma_blend | -2.9% | +3.6 pp | -1.4% | -3.2% | 25% | 56 |
| donchian_ens | -1.0% | +5.5 pp | -0.8% | -1.0% | 4% | 16 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **30%** (out of 20)
- Average 7-day move across coins: -6.4% (median -6.1%)
- BTC: 75,754 USD, 7-day -2.2%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 149 signals noticed within 12 h of the close; median adverse move +0.24%, 46% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 18 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 18 runs in 7 days. Check the GitHub Actions tab.
