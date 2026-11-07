# Weekly trend review 2026-W45

- Week ends: 2026-11-06 (UTC), report built 2026-11-07T13:21:26Z
- Live tracking since 2026-10-29: **8 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -5.5% |  | -1.7% | -7.5% | 100% |  |
| sma_50 | -0.1% | +5.4 pp | +0.2% | -0.4% | 5% | 2 |
| sma_100 | -5.7% | -0.2 pp | -3.9% | -6.7% | 20% | 24 |
| sma_blend | -2.5% | +3.0 pp | -1.4% | -3.2% | 24% | 54 |
| donchian_ens | -0.9% | +4.6 pp | -0.8% | -1.0% | 4% | 16 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **5%**; above their 100-day average: **20%** (out of 20)
- Average 7-day move across coins: -5.5% (median -5.8%)
- BTC: 75,731 USD, 7-day -1.9%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 141 signals noticed within 12 h of the close; median adverse move +0.30%, 48% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 19 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 19 runs in 7 days. Check the GitHub Actions tab.
- Median execution gap is above 0.25%: real costs may be higher than assumed.
