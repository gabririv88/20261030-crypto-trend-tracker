# Weekly trend review 2026-W45

- Week ends: 2026-11-08 (UTC), report built 2026-11-09T06:56:12Z
- Live tracking since 2026-10-29: **10 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -9.8% |  | -6.0% | -10.5% | 100% |  |
| sma_50 | -0.3% | +9.5 pp | +0.2% | -0.4% | 0% | 3 |
| sma_100 | -7.2% | +2.6 pp | -5.1% | -7.7% | 15% | 28 |
| sma_blend | -3.7% | +6.1 pp | -2.5% | -4.0% | 16% | 62 |
| donchian_ens | -1.0% | +8.8 pp | -0.9% | -1.1% | 1% | 19 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **15%** (out of 20)
- Average 7-day move across coins: -9.8% (median -8.8%)
- BTC: 74,754 USD, 7-day -4.4%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 165 signals noticed within 12 h of the close; median adverse move +0.24%, 47% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 18 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 18 runs in 7 days. Check the GitHub Actions tab.
