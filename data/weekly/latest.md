# Weekly trend review 2026-W46

- Week ends: 2026-11-15 (UTC), report built 2026-11-16T22:22:44Z
- Live tracking since 2026-10-29: **17 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -12.1% |  | -17.4% | -25.4% | 100% |  |
| sma_50 | +0.0% | +12.1 pp | +0.2% | -0.4% | 0% | 0 |
| sma_100 | -2.3% | +9.8 pp | -7.4% | -10.3% | 5% | 6 |
| sma_blend | -2.2% | +9.9 pp | -4.6% | -6.3% | 5% | 38 |
| donchian_ens | -0.1% | +12.1 pp | -0.9% | -1.2% | 0% | 1 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **5%** (out of 20)
- Average 7-day move across coins: -12.1% (median -11.2%)
- BTC: 65,315 USD, 7-day -12.6%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 210 signals noticed within 12 h of the close; median adverse move +0.24%, 47% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 16 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 16 runs in 7 days. Check the GitHub Actions tab.
