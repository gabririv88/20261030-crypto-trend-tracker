# Weekly trend review 2026-W46

- Week ends: 2026-11-13 (UTC), report built 2026-11-14T06:47:29Z
- Live tracking since 2026-10-29: **15 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -11.1% |  | -12.5% | -16.7% | 100% |  |
| sma_50 | +0.0% | +11.1 pp | +0.2% | -0.4% | 0% | 1 |
| sma_100 | -3.6% | +7.5 pp | -7.3% | -9.9% | 5% | 11 |
| sma_blend | -2.5% | +8.6 pp | -3.9% | -5.4% | 8% | 43 |
| donchian_ens | -0.2% | +10.9 pp | -0.9% | -1.2% | 0% | 4 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **5%** (out of 20)
- Average 7-day move across coins: -11.1% (median -9.1%)
- BTC: 68,237 USD, 7-day -9.9%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 200 signals noticed within 12 h of the close; median adverse move +0.30%, 50% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 16 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 16 runs in 7 days. Check the GitHub Actions tab.
- Median execution gap is above 0.25%: real costs may be higher than assumed.
