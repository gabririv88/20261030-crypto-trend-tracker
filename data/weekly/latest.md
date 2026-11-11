# Weekly trend review 2026-W46

- Week ends: 2026-11-10 (UTC), report built 2026-11-11T06:50:04Z
- Live tracking since 2026-10-29: **12 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -8.5% |  | -7.0% | -11.4% | 100% |  |
| sma_50 | -0.0% | +8.5 pp | +0.2% | -0.4% | 0% | 3 |
| sma_100 | -6.2% | +2.3 pp | -6.2% | -8.8% | 15% | 25 |
| sma_blend | -3.1% | +5.4 pp | -3.0% | -4.4% | 14% | 62 |
| donchian_ens | -0.7% | +7.8 pp | -0.9% | -1.1% | 1% | 16 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **15%** (out of 20)
- Average 7-day move across coins: -8.6% (median -7.8%)
- BTC: 73,698 USD, 7-day -4.7%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 183 signals noticed within 12 h of the close; median adverse move +0.24%, 47% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 16 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 16 runs in 7 days. Check the GitHub Actions tab.
