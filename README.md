# Trend Tracker: setup guide

A paper-trading tracker for daily trend rules on the coins you can trade on Revolut X. It places no orders, needs no Revolut account or API key, and uses public Coinbase prices. GitHub runs it for free four times a day and publishes a dashboard page you can open from your phone.

You do everything in the GitHub website. You don't need to install anything.

## The files

| File | What it is |
|---|---|
| `tracker.py` | The whole tracker |
| `dashboard_template.html` | The page layout of the dashboard |
| `revolutx_coins.txt` | Your Revolut X coin list, with 24h volumes from 2026-10-30 |
| `tracker.yml` | The GitHub schedule. It goes in the folder `.github/workflows/` |
| `README.md` | This guide |

## Step 1: GitHub account
1. Create an account at github.com, if you don't have one.
2. Turn on two-factor authentication: Settings, then Password and authentication.
3. Keep your email private: Settings, then Emails, then tick "Keep my email addresses private" and "Block command line pushes that expose my email". Without this, the bot's commits are fine, but yours would show your real email on a public repository.

## Step 2: Create the repository
1. Click **+** (top right), then **New repository**.
2. Name: `crypto-trend-tracker` (any name works).
3. Choose **Public**. This is free and the dashboard page works with it. Anyone can see your strategies and results, but nothing secret is stored, because the tracker uses no keys.
4. Do not tick any "Add a file" options. Click **Create repository**.

## Step 3: Upload the files
1. On the empty repository page, click **uploading an existing file**.
2. Drag in `tracker.py`, `dashboard_template.html`, `revolutx_coins.txt` and `README.md`.
3. Click **Commit changes**.

## Step 4: Add the schedule file
1. Click **Add file**, then **Create new file**.
2. In the name box, type exactly `.github/workflows/tracker.yml`. Each `/` creates a folder.
3. Paste the full content of `tracker.yml` into the editor.
4. Click **Commit changes**.

## Step 5: Turn on the dashboard page
1. Go to **Settings**, then **Pages**.
2. Under **Build and deployment**, set **Source** to **GitHub Actions**.

## Step 6: Allow the tracker to save its data
1. Go to **Settings**, then **Actions**, then **General**.
2. Scroll to **Workflow permissions**, choose **Read and write permissions**, and click **Save**.

## Step 7: First run
1. Open the **Actions** tab. If asked, click the green button to enable workflows.
2. Click **tracker** on the left, then **Run workflow**, then the green **Run workflow** button.
3. Wait 3 to 6 minutes. The first run downloads about four years of daily prices for each coin that passes the filters.
4. A green tick means it worked. A red cross means something failed: click the run, open the failing step, and send me the error text.

Then open **Settings**, then **Pages**. The address of your dashboard is shown there (`https://YOUR-NAME.github.io/crypto-trend-tracker/`). Open it and bookmark it on your phone.

## What happens next
- GitHub runs the tracker at **00:30, 06:30, 12:30 and 18:30 UTC** (01:30, 07:30, 13:30 and 19:30 in Warsaw in winter; one hour later in the clock in summer). The first run after the daily close does the actual work. The other three are retries: if a run fails or GitHub skips it, the next one catches up on everything missed, and nothing is traded twice.
- GitHub's scheduler can start runs late. The dashboard shows the time of the last update and turns red if it is more than 26 hours old.
- GitHub emails you when a scheduled run fails. Check your notification settings (Settings, then Notifications, then Actions).
- GitHub switches off scheduled runs in a public repository after 60 days with no activity. The tracker saves data on each run, which should count as activity, but I could not verify that from here. **Check the Actions tab once a month.** If runs stop, open the tracker workflow and click **Enable workflow**.

## Which coins are tracked
On the first run, and on the first run of every month, the tracker checks each coin in `revolutx_coins.txt` and keeps those that pass all of these:
- Not a stablecoin, a wrapped or staked copy of another coin, or a meme coin (excluded by name).
- At least $100,000 of 24h volume on Revolut X, taken from the file.
- A USD pair on Coinbase, with at least 400 days of price history.
- At least $5 million of average daily volume on Coinbase over the last 30 days.

The result of every decision, with the reason, is in `data/universe_report.csv`. A coin already tracked is never removed. A new coin starts with its own start date, so results are never rewritten.

To add coins, edit `revolutx_coins.txt` (one line per coin: `SYMBOL, volume`). It is picked up at the next monthly check. To force it now: open `data/config.json`, set `"universe_checked": ""`, commit, and run the workflow.

## The models
Every coin and every model starts with a virtual $1,000. Decisions use the daily close (00:00 UTC), and trades happen at that close.

| Model | Rule |
|---|---|
| Buy & hold | Buy at the start and keep (the benchmark) |
| SMA 50 | Fully invested while the price is above its 50-day average, otherwise cash |
| SMA 100 | The same with 100 days |
| SMA blend | The average of ten SMA signals (20 to 200 days): a partial position |
| Donchian blend | The average of eight breakout signals (5 to 200 days): a partial position |

Every trade pays 0.14% (0.09% Revolut X taker fee plus 0.05% assumed slippage). The partial-position models trade often in small steps, which is realistic but makes the trade log long.

## Reading the results
- **Dashboard**: scoreboard, portfolio and drawdown charts, today's positions, a one-coin view and the latest signals. The "Replay + live tracking" view shows the models on past prices before tracking started. It uses today's coin list, so treat it as a demonstration of behaviour, not as earnings.
- **Files in `data/`**: `portfolio_forward.csv` (daily value of each model), `trades.csv` (every paper trade), `live_fills.csv` (the price seen when each signal was first noticed, against the close used), `runs.csv` (a log of every run), `universe_report.csv`.
- **Weekly review**: every run writes `data/weekly/latest.md` and `data/weekly/<year>-W<week>.md`: model results for the last 7 days and since the start, the market trend (share of coins above their 50 and 100-day averages), the execution check, system health and automatic warning flags. The file for a week is final after that week's Sunday close.

## Rules for the experiment
1. Don't change the models after the start. If you want to test a new idea, make a second repository, so the original stays a clean test.
2. Less than 90 days of data says almost nothing. Judge after at least a year, on drawdown and risk-adjusted return versus buy and hold, not on one good month.
3. Watch `live_fills.csv`. If the "adverse" column is often well above 0.3%, the real costs are higher than the assumed 0.05% slippage, and the results are too optimistic.
4. The tracker never needs a key. Never put a Revolut X API key, a password or a seed phrase into this repository.

## Testing offline (optional)
With Python and numpy installed: `python tracker.py --demo --data demo_data --docs demo_docs` builds a dashboard from synthetic prices in the folder `demo_docs`. Open `demo_docs/index.html` in a browser. Delete both folders afterwards.
