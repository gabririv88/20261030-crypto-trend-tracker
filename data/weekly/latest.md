# Weekly trend review 2026-W48

- Week ends: 2026-11-27 (UTC), report built 2026-11-28T08:10:02Z
- Live tracking since 2026-10-29: **29 days**, 20 coins
- Evidence level: **setup phase: check the system works, ignore the returns**

## Models

| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |
|---|---|---|---|---|---|---|
| hold | +5.2% |  | -21.9% | -29.3% | 100% |  |
| sma_50 | +0.3% | -4.8 pp | +0.5% | -0.6% | 5% | 1 |
| sma_100 | -0.1% | -5.2 pp | -8.0% | -10.7% | 5% | 5 |
| sma_blend | +0.8% | -4.4 pp | -4.3% | -6.5% | 8% | 8 |
| donchian_ens | +0.2% | -4.9 pp | -0.7% | -1.2% | 2% | 4 |

Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.

## Market trend

- Share of coins above their 50-day average: **5%**; above their 100-day average: **5%** (out of 20)
- Average 7-day move across coins: +5.0% (median +4.1%)
- BTC: 59,858 USD, 7-day +1.8%, below its 50-day and below its 100-day average

## Execution check (price seen vs close used)

- 236 signals noticed within 12 h of the close; median adverse move +0.19%, 46% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)

## System health

- Runs in the last 7 days: 14 (expected 28 once running for a full week)
- Download failures in this run: 0; coins without the last closed day: 0

## Flags

- Only 14 runs in 7 days. Check the GitHub Actions tab.
