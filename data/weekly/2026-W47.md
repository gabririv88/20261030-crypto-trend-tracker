# Weekly trend review 2026-W47

- Week ends: 2026-11-16 (UTC), report built 2026-11-17T21:08:09Z
- Live tracking since 2026-10-29: **18 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -15.7% |  | -18.8% | -25.4% | 100% |  |
| sma_50 | +0.0% | +15.7 pp | +0.2% | -0.4% | 0% | 0 |
| sma_100 | -2.7% | +13.1 pp | -7.5% | -10.3% | 5% | 4 |
| sma_blend | -2.7% | +13.0 pp | -4.7% | -6.3% | 5% | 33 |
| donchian_ens | -0.1% | +15.6 pp | -0.9% | -1.2% | 0% | 1 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **5%** (out of 20)
- Average 7-day move across coins: -15.7% (median -14.5%)
- BTC: 64,817 USD, 7-day -13.9%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 210 signals noticed within 12 h of the close; median adverse move +0.24%, 47% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 15 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 15 runs in 7 days. Check the GitHub Actions tab.
