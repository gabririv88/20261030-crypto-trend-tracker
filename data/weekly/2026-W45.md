# Weekly trend review 2026-W45

- Week ends: 2026-11-02 (UTC), report built 2026-11-03T01:05:44Z
- Live tracking since 2026-10-29: **4 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -7.6% |  | +0.2% | -4.3% | 100% |  |
| sma_50 | -1.8% | +5.8 pp | +0.3% | -0.2% | 5% | 1 |
| sma_100 | -7.6% | +0.1 pp | -0.8% | -3.5% | 40% | 20 |
| sma_blend | -4.2% | +3.4 pp | -0.2% | -1.8% | 30% | 42 |
| donchian_ens | -1.5% | +6.1 pp | -0.2% | -0.5% | 5% | 8 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **5%**; above their 100-day average: **40%** (out of 20)
- Average 7-day move across coins: -7.7% (median -6.6%)
- BTC: 76,674 USD, 7-day -4.2%, below its 50-day and above its 100-day average

## Execution check (price seen vs close used)

- 71 signals noticed within 12 h of the close; median adverse move +0.40%, 55% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 16 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Median execution gap is above 0.25%: real costs may be higher than assumed.
