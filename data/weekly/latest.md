# Weekly trend review 2026-W45

- Week ends: 2026-11-04 (UTC), report built 2026-11-05T07:04:24Z
- Live tracking since 2026-10-29: **6 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -4.3% |  | +5.0% | -4.3% | 100% |  |
| sma_50 | -1.5% | +2.8 pp | +0.6% | -0.2% | 5% | 1 |
| sma_100 | -6.7% | -2.4 pp | +1.3% | -3.5% | 70% | 26 |
| sma_blend | -3.2% | +1.1 pp | +1.3% | -1.8% | 39% | 56 |
| donchian_ens | -1.5% | +2.8 pp | +0.0% | -0.5% | 10% | 14 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **5%**; above their 100-day average: **70%** (out of 20)
- Average 7-day move across coins: -4.3% (median -3.1%)
- BTC: 80,428 USD, 7-day -1.0%, below its 50-day and above its 100-day average

## Execution check (price seen vs close used)

- 97 signals noticed within 12 h of the close; median adverse move +0.39%, 54% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 21 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Median execution gap is above 0.25%: real costs may be higher than assumed.
