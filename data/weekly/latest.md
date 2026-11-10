# Weekly trend review 2026-W46

- Week ends: 2026-11-09 (UTC), report built 2026-11-10T07:32:51Z
- Live tracking since 2026-10-29: **11 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -4.0% |  | -3.7% | -10.5% | 100% |  |
| sma_50 | -0.1% | +3.9 pp | +0.2% | -0.4% | 0% | 3 |
| sma_100 | -4.2% | -0.2 pp | -5.0% | -7.7% | 25% | 25 |
| sma_blend | -1.9% | +2.1 pp | -2.1% | -4.0% | 20% | 57 |
| donchian_ens | -0.7% | +3.3 pp | -0.9% | -1.1% | 1% | 16 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **25%** (out of 20)
- Average 7-day move across coins: -4.0% (median -4.2%)
- BTC: 75,259 USD, 7-day -1.8%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 172 signals noticed within 12 h of the close; median adverse move +0.22%, 47% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 17 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 17 runs in 7 days. Check the GitHub Actions tab.
