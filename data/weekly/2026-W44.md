# Weekly trend review 2026-W44

- Week ends: 2026-11-01 (UTC), report built 2026-11-02T01:35:23Z
- Live tracking since 2026-10-29: **3 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -3.3% |  | +4.2% | -0.6% | 100% |  |
| sma_50 | -1.3% | +1.9 pp | +0.5% | -0.0% | 5% | 1 |
| sma_100 | -4.1% | -0.9 pp | +2.2% | -0.6% | 65% | 15 |
| sma_blend | -2.3% | +0.9 pp | +1.3% | -0.3% | 35% | 32 |
| donchian_ens | -1.2% | +2.1 pp | +0.2% | -0.1% | 8% | 5 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **5%**; above their 100-day average: **65%** (out of 20)
- Average 7-day move across coins: -3.3% (median -2.4%)
- BTC: 78,231 USD, 7-day -2.3%, below its 50-day and above its 100-day average

## Execution check (price seen vs close used)

- 53 signals noticed within 12 h of the close; median adverse move +1.46%, 72% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 13 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Median execution gap is above 0.25%: real costs may be higher than assumed.
