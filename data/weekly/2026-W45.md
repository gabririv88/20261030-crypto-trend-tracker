# Weekly trend review 2026-W45

- Week ends: 2026-11-05 (UTC), report built 2026-11-06T19:35:34Z
- Live tracking since 2026-10-29: **7 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -2.7% |  | -2.8% | -7.5% | 100% |  |
| sma_50 | +0.2% | +2.9 pp | +0.2% | -0.4% | 0% | 1 |
| sma_100 | -4.0% | -1.3 pp | -4.1% | -6.7% | 20% | 26 |
| sma_blend | -1.7% | +1.0 pp | -1.7% | -3.2% | 21% | 57 |
| donchian_ens | -0.8% | +2.0 pp | -0.8% | -1.0% | 4% | 16 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **20%** (out of 20)
- Average 7-day move across coins: -2.8% (median -3.3%)
- BTC: 75,969 USD, 7-day -2.3%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 132 signals noticed within 12 h of the close; median adverse move +0.30%, 48% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 20 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Median execution gap is above 0.25%: real costs may be higher than assumed.
