# Weekly trend review 2026-W45

- Week ends: 2026-11-03 (UTC), report built 2026-11-04T06:45:01Z
- Live tracking since 2026-10-29: **5 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -6.9% |  | +1.6% | -4.3% | 100% |  |
| sma_50 | -2.0% | +5.0 pp | +0.3% | -0.2% | 5% | 1 |
| sma_100 | -7.4% | -0.5 pp | -0.0% | -3.5% | 50% | 22 |
| sma_blend | -4.1% | +2.8 pp | +0.2% | -1.8% | 32% | 46 |
| donchian_ens | -1.7% | +5.3 pp | -0.2% | -0.5% | 5% | 8 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **5%**; above their 100-day average: **50%** (out of 20)
- Average 7-day move across coins: -7.0% (median -5.0%)
- BTC: 77,337 USD, 7-day -4.3%, below its 50-day and above its 100-day average

## Execution check (price seen vs close used)

- 77 signals noticed within 12 h of the close; median adverse move +0.40%, 55% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 19 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Median execution gap is above 0.25%: real costs may be higher than assumed.
