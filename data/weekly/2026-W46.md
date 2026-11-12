# Weekly trend review 2026-W46

- Week ends: 2026-11-11 (UTC), report built 2026-11-12T20:11:06Z
- Live tracking since 2026-10-29: **13 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | -12.4% |  | -8.0% | -12.4% | 100% |  |
| sma_50 | -0.3% | +12.0 pp | +0.2% | -0.4% | 0% | 3 |
| sma_100 | -8.0% | +4.4 pp | -6.8% | -9.4% | 10% | 22 |
| sma_blend | -4.5% | +7.9 pp | -3.3% | -4.8% | 12% | 57 |
| donchian_ens | -0.9% | +11.5 pp | -0.9% | -1.1% | 1% | 10 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **0%**; above their 100-day average: **10%** (out of 20)
- Average 7-day move across coins: -12.4% (median -11.9%)
- BTC: 73,928 USD, 7-day -8.1%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 189 signals noticed within 12 h of the close; median adverse move +0.30%, 48% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 16 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 16 runs in 7 days. Check the GitHub Actions tab.
- Median execution gap is above 0.25%: real costs may be higher than assumed.
