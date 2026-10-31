# Weekly trend review 2026-W44

- Week ends: 2026-10-30 (UTC), report built 2026-10-31T01:27:23Z
- Live tracking since 2026-10-29: **1 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -5.2% |  | +4.1% | -0.1% | 100% |  |
| sma_50 | -1.5% | +3.7 pp | +0.2% | -0.0% | 5% | 1 |
| sma_100 | -6.0% | -0.8 pp | +1.9% | -0.1% | 70% | 14 |
| sma_blend | -3.4% | +1.8 pp | +1.1% | -0.0% | 36% | 25 |
| donchian_ens | -1.6% | +3.5 pp | +0.1% | -0.0% | 8% | 5 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **5%**; above their 100-day average: **70%** (out of 20)
- Average 7-day move across coins: -5.2% (median -5.8%)
- BTC: 77,180 USD, 7-day -4.8%, below its 50-day and above its 100-day average

## Execution check (price seen vs close used)

- 45 signals noticed within 12 h of the close; median adverse move +1.76%, 76% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 5 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Median execution gap is above 0.25%: real costs may be higher than assumed.
