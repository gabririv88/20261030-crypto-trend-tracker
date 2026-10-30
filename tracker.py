#!/usr/bin/env python3
"""
Forward paper tracker for daily trend rules on Revolut X coins. READ-ONLY: it uses public Coinbase prices,
needs no account and no API key, and never places an order.

What it does on every run (safe to run any number of times per day, in any order):
  1. Decides which coins are tracked (first run, then once a month): coins from revolutx_coins.txt that are on
     Coinbase (USD pair), have >= 400 days of history and enough daily volume, minus stablecoins, wrapped coins and
     meme coins. Coins already tracked are never removed; new ones start on the day they are added.
  2. Downloads the missing daily candles (only closed UTC days are used).
  3. REPLAYS every model from the start date to the last closed day. The result depends only on the stored prices, so a
     missed run or a repeated run changes nothing: the next run simply catches up.
  4. Records, once per trade, the price actually visible when the script first saw the signal (execution lag check).
  5. Writes CSV files in data/ and the dashboard docs/index.html.

Models (long-only, decided at the daily close, executed at that close, cost 0.09% fee + 0.05% slippage per side):
  hold          buy at the start and keep            (benchmark)
  sma_50        100% invested while close > 50-day average, otherwise cash
  sma_100       same with 100 days
  sma_blend     average of the ten SMA signals (20..200 days): fractional position
  donchian_ens  average of eight Donchian breakout states (5..200 days): fractional position

Usage
  python tracker.py                 # real run (Coinbase public data)
  python tracker.py --demo          # offline run with synthetic prices (testing)
Needs: Python 3.9+ and numpy.
"""
import argparse, calendar, csv, json, math, os, sys, time, zlib
import urllib.error, urllib.parse, urllib.request
from pathlib import Path

try:
    import numpy as np
    from numpy.lib.stride_tricks import sliding_window_view as swv
except ImportError:
    sys.exit("This script needs numpy. Install it with:  python -m pip install numpy")

FEE, SLIP = 0.0009, 0.0005
COST = FEE + SLIP
CAP = 1000.0
DAY = 86400
API = "https://api.exchange.coinbase.com"
UA = {"User-Agent": "paper-tracker/1.0", "Accept": "application/json"}
MODELS = ["hold", "sma_50", "sma_100", "sma_blend", "donchian_ens"]
SMA_BLEND = (20, 30, 40, 50, 60, 75, 100, 125, 150, 200)
DONCH = (5, 10, 20, 30, 60, 90, 150, 200)
FETCH_DAYS = 1500

STABLES = set("USDT USDC DAI PYUSD EURC USDS USDE FDUSD TUSD GUSD PAX USDP BUSD FRAX LUSD GYEN EURT XSGD".split())
WRAPPED = set("WBTC WETH STETH WSTETH CBETH CBBTC RETH WEETH LSETH MSOL JITOSOL BNSOL".split())
MEMES = set("DOGE SHIB PEPE BONK WIF FLOKI TRUMP MEME BRETT POPCAT MOG TURBO NEIRO PNUT GOAT FARTCOIN SPX MEW DOGS "
            "HMSTR CATI BOME PEOPLE BABYDOGE WEN MOODENG GIGA TOSHI MOTHER ZEREBRO PENGU AI16Z FWOG BOBO LADYS "
            "PUMP ELON SAMO KISHU AKITA HOGE MONG SNEK DEGEN MOODENG PONKE RETARDIO BAN".split())


# ------------------------------------------------------------------ small helpers
def iso_day(t): return time.strftime("%Y-%m-%d", time.gmtime(t))
def iso_full(t): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t))
def day_ts(s): return calendar.timegm(time.strptime(s, "%Y-%m-%d"))
def last_closed_day(now): return (int(now) // DAY) * DAY - DAY
def clean(x, nd=6):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))): return None
    return float(f"{x:.{nd}g}")
def log(*a): print(*a, flush=True)


# ------------------------------------------------------------------ data sources
class Coinbase:
    def _get(self, path, params=None, tries=4):
        url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
        last = None
        for a in range(tries):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                    return json.loads(r.read())
            except urllib.error.HTTPError as e:
                last = f"HTTP {e.code}"
                if e.code in (429, 500, 502, 503, 504): time.sleep(2 * (a + 1)); continue
                raise RuntimeError(f"{path}: {last}")
            except (urllib.error.URLError, TimeoutError) as e:
                last = str(e); time.sleep(2 * (a + 1))
        raise RuntimeError(f"{path}: {last}")

    def products(self):
        return {p["base_currency"] for p in self._get("/products")
                if p.get("quote_currency") == "USD" and p.get("status") == "online" and not p.get("trading_disabled")}

    def candles(self, sym, since, now):
        out, cur_end = {}, int(now)
        while cur_end > since:
            cur_start = max(since, cur_end - 299 * DAY)
            rows = self._get(f"/products/{sym}-USD/candles",
                             {"granularity": DAY, "start": iso_full(cur_start), "end": iso_full(cur_end)})
            for r in rows:
                t = int(r[0])
                out[t] = (t, float(r[3]), float(r[2]), float(r[1]), float(r[4]), float(r[5]))  # t,o,h,l,c,v
            if not rows and (out or cur_end == int(now)): break
            cur_end = cur_start
            time.sleep(0.12)
        return sorted(out.values())

    def ticker(self, sym, now):
        return float(self._get(f"/products/{sym}-USD/ticker")["price"])


class Demo:
    """Synthetic prices so the whole pipeline can be tested offline."""
    SPECIAL = {"TINY": dict(vol=2e4), "NEWCOIN": dict(start_off=1500)}
    NAMES = "BTC ETH SOL XRP ADA LINK LTC DOT AVAX ATOM NEAR UNI AAVE TINY NEWCOIN USDT DOGE".split()
    T0 = calendar.timegm((2022, 6, 1, 0, 0, 0))
    N = 1800

    def __init__(self): self.cache = {}

    def products(self): return {s for s in self.NAMES}

    def _series(self, sym):
        if sym in self.cache: return self.cache[sym]
        rng = np.random.default_rng(zlib.crc32(sym.encode()))
        common = np.random.default_rng(99).normal(0, 0.02, self.N)
        drift = np.zeros(self.N); i = 0
        while i < self.N:
            L = int(rng.integers(40, 220)); drift[i:i + L] = rng.choice([-0.004, 0.0, 0.003, 0.006]); i += L
        ret = drift + 0.6 * common + rng.normal(0, 0.027, self.N)
        c = 100 * np.exp(np.cumsum(ret)) * (0.2 + rng.random() * 3)
        o = np.concatenate(([c[0]], c[:-1]))
        h = np.maximum(o, c) * (1 + np.abs(rng.normal(0, 0.012, self.N))); l = np.minimum(o, c) * (1 - np.abs(rng.normal(0, 0.012, self.N)))
        base_vol = self.SPECIAL.get(sym, {}).get("vol", 8e6 * (0.5 + rng.random() * 4))
        v = base_vol / c * np.exp(rng.normal(0, 0.3, self.N))
        s = self.SPECIAL.get(sym, {}).get("start_off", 0)
        rows = [(self.T0 + i * DAY, o[i], h[i], l[i], c[i], v[i]) for i in range(s, self.N)]
        self.cache[sym] = rows
        return rows

    def candles(self, sym, since, now):
        return [r for r in self._series(sym) if since <= r[0] <= now]

    def ticker(self, sym, now):
        rows = [r for r in self._series(sym) if r[0] + DAY <= now]
        return rows[-1][4] * 1.002


# ------------------------------------------------------------------ cache
def load_cache(p):
    if not p.exists(): return []
    with open(p, encoding="utf-8") as f:
        return [tuple(float(x) for x in r) for r in csv.reader(f) if r]


def save_cache(p, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for r in rows: w.writerow([int(r[0])] + [f"{x:.10g}" for x in r[1:]])


def closed_only(rows, now): return [r for r in rows if r[0] + DAY <= now]


def update_cache(src, sym, cache_dir, now):
    p = cache_dir / f"{sym}.csv"; rows = load_cache(p)
    since = int(rows[-1][0]) - 3 * DAY if rows else int(now) - FETCH_DAYS * DAY
    merged = {int(r[0]): r for r in rows}
    for r in closed_only(src.candles(sym, since, now), now): merged[int(r[0])] = r
    rows = [merged[k] for k in sorted(merged)]
    save_cache(p, rows)
    return rows


# ------------------------------------------------------------------ arrays and signals
def to_arrays(rows):
    t0 = int(rows[0][0]); n = int((rows[-1][0] - t0) // DAY) + 1
    a = np.full((n, 5), np.nan)
    for t, o, h, l, c, v in rows: a[int((t - t0) // DAY)] = [o, h, l, c, v]
    for i in range(1, n):
        if np.isnan(a[i, 3]): p = a[i - 1, 3]; a[i] = [p, p, p, p, 0.0]
    return dict(t0=t0, o=a[:, 0], h=a[:, 1], l=a[:, 2], c=a[:, 3], v=a[:, 4])


def rmean(x, n):
    out = np.full(len(x), np.nan)
    if len(x) >= n: cs = np.cumsum(np.insert(x, 0, 0.0)); out[n - 1:] = (cs[n:] - cs[:-n]) / n
    return out


def prior_ext(x, n, fn):
    out = np.full(len(x), np.nan)
    if len(x) > n: out[n:] = fn(swv(x, n), axis=1)[:len(x) - n]
    return out


def sig_sma(c, n):
    m = rmean(c, n)
    return np.where(np.isnan(m), 0.0, (c > m).astype(float))


def channel_state(h, l, c, n):
    up = prior_ext(h, n, np.max); lo = prior_ext(l, n, np.min)
    st, on = np.zeros(len(c)), False
    for i in range(len(c)):
        if np.isnan(up[i]): continue
        mid = (up[i] + lo[i]) / 2
        if not on and c[i] > up[i]: on = True
        elif on and c[i] < mid: on = False
        st[i] = 1.0 if on else 0.0
    return st


def weights(model, d):
    c = d["c"]
    if model == "hold": return np.ones(len(c))
    if model == "sma_50": return sig_sma(c, 50)
    if model == "sma_100": return sig_sma(c, 100)
    if model == "sma_blend": return np.mean([sig_sma(c, n) for n in SMA_BLEND], axis=0)
    if model == "donchian_ens": return np.mean([channel_state(d["h"], d["l"], c, n) for n in DONCH], axis=0)
    raise ValueError(model)


def replay(c, w, i0, cost=COST, cap=CAP):
    """Paper account: trade at the close of day i to reach target weight w[i]; trade only when the target changes."""
    n = len(c); eq = np.full(n, np.nan); cash, units, prev, trades = cap, 0.0, 0.0, []
    for i in range(i0, n):
        px = c[i]; val = cash + units * px; tw = float(w[i])
        if abs(tw - prev) > 1e-9:
            cur = units * px / val; tv = (tw - cur) * val; fee = abs(tv) * cost
            units += tv / px; cash -= tv + fee
            trades.append((i, prev, tw, px, fee)); prev = tw
        eq[i] = cash + units * px
    return eq, trades


# ------------------------------------------------------------------ portfolio and metrics
def place(arr, t0, i0, T0, n_cal):
    """Put a per-coin array (index 0 = day t0) onto the calendar starting at T0."""
    out = np.full(n_cal, np.nan)
    for j in range(max(i0, 0), len(arr)):
        k = (t0 + j * DAY - T0) // DAY
        if 0 <= k < n_cal: out[k] = arr[j]
    return out


def portfolio_index(eqs, cap=CAP):
    """Equal-weight portfolio index (start = 100): each day's return is the mean return of the coins active on both days."""
    if not eqs: return np.array([])
    M = np.array(eqs); n = M.shape[1]; idx = np.full(n, np.nan); prev = None
    for t in range(n):
        act = ~np.isnan(M[:, t])
        if not act.any():
            continue
        if prev is None:
            idx[t] = 100 * np.mean(M[act, t] / cap); prev = t; continue
        both = act & ~np.isnan(M[:, prev])
        r = np.mean(M[both, t] / M[both, prev] - 1) if both.any() else 0.0
        idx[t] = idx[prev] * (1 + r); prev = t
    return idx


def metrics(idx, expo, ntr):
    v = idx[~np.isnan(idx)]
    if len(v) < 2: return dict(days=0, ret=0.0, maxdd=0.0, sharpe=None, expo=expo, trades=ntr)
    peak = np.maximum.accumulate(np.maximum(v, 100.0)); dd = (v / peak - 1).min()
    r = v[1:] / v[:-1] - 1
    sharpe = float(r.mean() / r.std(ddof=1) * math.sqrt(365)) if len(r) >= 90 and r.std(ddof=1) > 0 else None
    return dict(days=len(v) - 1, ret=float(v[-1] / 100 - 1), maxdd=float(dd), sharpe=sharpe, expo=expo, trades=ntr)


# ------------------------------------------------------------------ universe
def read_listing(path):
    """Lines look like 'BTC, 13580000' (symbol, optional Revolut X 24h volume in USD). Returns (symbols, volumes)."""
    out, vols = [], {}
    if not Path(path).exists(): return out, vols
    for line in open(path, encoding="utf-8"):
        parts = line.split("#")[0].replace(",", " ").split()
        if not parts: continue
        s = parts[0].upper().replace("/", "-")
        for sfx in ("-USD", "-USDT", "-EUR"):
            if s.endswith(sfx): s = s[:-len(sfx)]
        if s not in out: out.append(s)
        if len(parts) > 1:
            try: vols[s] = float(parts[1])
            except ValueError: pass
    return out, vols


def select_universe(src, listing, vols, cfg, now, a, cache_dir, report_path):
    online = src.products(); rep = []; start = iso_day(last_closed_day(now))
    for sym in listing:
        if sym in cfg["coins"]: rep.append((sym, "tracked", "already tracked since " + cfg["coins"][sym])); continue
        if sym in STABLES: rep.append((sym, "excluded", "stablecoin")); continue
        if sym in WRAPPED: rep.append((sym, "excluded", "wrapped/staked copy of another coin")); continue
        if sym in MEMES: rep.append((sym, "excluded", "meme coin")); continue
        if sym in vols and vols[sym] < a.min_rx_vol:
            rep.append((sym, "excluded", f"Revolut X 24h volume ${vols[sym]/1e3:.0f}K < ${a.min_rx_vol/1e3:.0f}K")); continue
        if sym not in online: rep.append((sym, "excluded", "no online USD pair on Coinbase")); continue
        try:
            rows = closed_only(src.candles(sym, int(now) - FETCH_DAYS * DAY, now), now)
        except Exception as e:
            rep.append((sym, "error", str(e))); continue
        if len(rows) < a.min_days: rep.append((sym, "excluded", f"history {len(rows)} days < {a.min_days}")); continue
        if rows[-1][0] + DAY < last_closed_day(now) - 2 * DAY: rep.append((sym, "excluded", "no recent candles")); continue
        vol = float(np.mean([r[5] * r[4] for r in rows[-30:]]))
        if vol < a.min_vol: rep.append((sym, "excluded", f"30-day avg volume ${vol/1e6:.2f}M < ${a.min_vol/1e6:.1f}M")); continue
        save_cache(cache_dir / f"{sym}.csv", rows)
        cfg["coins"][sym] = start
        rep.append((sym, "added", f"start {start}, avg daily volume ${vol/1e6:.1f}M"))
    with open(report_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["symbol", "decision", "reason"]); w.writerows(rep)
    return rep



def evidence_label(days):
    if days < 30: return "setup phase: check the system works, ignore the returns"
    if days < 90: return "too short: results are mostly noise"
    if days < 365: return "early signal, not a verdict"
    return "first full review is possible"


def weekly_report(now, T_end, cfg, mets, portB, arrays, W, TR, fills, runs_path, errors, stale, failed):
    wk = time.strftime("%G-W%V", time.gmtime(T_end))
    days = mets["hold"]["days"]
    L = [f"# Weekly trend review {wk}", "",
         f"- Week ends: {iso_day(T_end)} (UTC), report built {iso_full(now)}",
         f"- Live tracking since {cfg['inception']}: **{days} days**, {len(arrays)} coins",
         f"- Evidence level: **{evidence_label(days)}**", ""]
    def wret(m):
        v = [x for x in portB[m] if not np.isnan(x)]
        return v[-1] / v[-8] - 1 if len(v) >= 8 else None
    hold7 = wret("hold")
    L += ["## Models", "", "| Model | Last 7 days | vs hold | Since start | Max drawdown | Invested now | Trades this week |", "|---|---|---|---|---|---|---|"]
    now_w = {}
    for m in MODELS:
        ws = [W[(s, m)][-1] for s, d in arrays.items() if d["t0"] + (len(d["c"]) - 1) * DAY == T_end]
        now_w[m] = float(np.mean(ws)) if ws else None
        w7 = wret(m); x = mets[m]
        ntw = sum(1 for t in TR if t[2] == m and t[0] >= T_end - 6 * DAY) if m != "hold" else 0
        rel = "" if m == "hold" or w7 is None or hold7 is None else f"{(w7 - hold7) * 100:+.1f} pp"
        L.append(f"| {m} | {'' if w7 is None else f'{w7*100:+.1f}%'} | {rel} | {x['ret']*100:+.1f}% | {x['maxdd']*100:.1f}% | "
                 f"{'' if now_w[m] is None else f'{now_w[m]*100:.0f}%'} | {ntw if m != 'hold' else ''} |")
    L += ["", "Last-7-day figures come from the same rules on the same prices; before the tracking start date they are a replay, not live results.", ""]
    # market trend
    L += ["## Market trend", ""]
    live = {s: d for s, d in arrays.items() if d["t0"] + (len(d["c"]) - 1) * DAY == T_end and len(d["c"]) > 210}
    if live:
        a50 = np.mean([W[(s, "sma_50")][-1] for s in live]); a100 = np.mean([W[(s, "sma_100")][-1] for s in live])
        ch = [d["c"][-1] / d["c"][-8] - 1 for d in live.values()]
        L.append(f"- Share of coins above their 50-day average: **{a50*100:.0f}%**; above their 100-day average: **{a100*100:.0f}%** (out of {len(live)})")
        L.append(f"- Average 7-day move across coins: {np.mean(ch)*100:+.1f}% (median {np.median(ch)*100:+.1f}%)")
        if "BTC" in live:
            d = live["BTC"]; c = d["c"]
            L.append(f"- BTC: {c[-1]:,.0f} USD, 7-day {((c[-1]/c[-8])-1)*100:+.1f}%, "
                     f"{'above' if W[('BTC','sma_50')][-1] else 'below'} its 50-day and {'above' if W[('BTC','sma_100')][-1] else 'below'} its 100-day average")
    else:
        L.append("- No coin has data for the last closed day yet.")
    L.append("")
    # execution
    fl = [f for f in fills.values() if float(f["lag_h"]) < 12]
    L += ["## Execution check (price seen vs close used)", ""]
    if fl:
        adv = np.array([float(f["adverse_pct"]) for f in fl])
        L.append(f"- {len(fl)} signals noticed within 12 h of the close; median adverse move {np.median(adv):+.2f}%, "
                 f"{np.mean(adv > 0.3)*100:.0f}% worse than 0.30% (the paper account assumes 0.05% slippage plus fees)")
    else:
        L.append("- No signal has been checked yet (a signal needs to be noticed within 12 hours of the daily close).")
    L.append("")
    # health
    nruns, nrun_ok = 0, 0
    if runs_path.exists():
        for r in csv.DictReader(open(runs_path, encoding="utf-8")):
            try: tt = calendar.timegm(time.strptime(r["run_utc"], "%Y-%m-%dT%H:%M:%SZ"))
            except Exception: continue
            if tt >= now - 7 * DAY: nruns += 1
    L += ["## System health", "", f"- Runs in the last 7 days: {nruns} (expected 28 once running for a full week)",
          f"- Download failures in this run: {failed}; coins without the last closed day: {len(stale)}"]
    for e in errors[:5]: L.append(f"- Note: {e}")
    L.append("")
    # flags
    flags = []
    if days >= 7 and nruns < 20: flags.append(f"Only {nruns} runs in 7 days. Check the GitHub Actions tab.")
    if stale: flags.append(f"{len(stale)} coin(s) missing the last closed day: {', '.join(stale[:8])}")
    if fl and np.median([float(f['adverse_pct']) for f in fl]) > 0.25: flags.append("Median execution gap is above 0.25%: real costs may be higher than assumed.")
    for m in MODELS[1:]:
        if days >= 30 and mets[m]["maxdd"] < mets["hold"]["maxdd"] - 0.02: flags.append(f"{m} has a deeper drawdown than buy and hold.")
    L += ["## Flags", ""] + ([f"- {f}" for f in flags] if flags else ["- none"]) + [""]
    return wk, "\n".join(L)


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--listing", default="revolutx_coins.txt")
    ap.add_argument("--data", default="data")
    ap.add_argument("--docs", default="docs")
    ap.add_argument("--min-vol", type=float, default=5e6, help="min 30-day average daily USD volume on Coinbase")
    ap.add_argument("--min-rx-vol", type=float, default=1e5, help="min Revolut X 24h volume (USD) from the listing file")
    ap.add_argument("--min-days", type=int, default=400)
    ap.add_argument("--hist-days", type=int, default=730, help="length of the labelled replay shown before the start date")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--now", default=None, help="testing only: pretend the current time is this UTC time, e.g. 2026-11-03T01:00:00")
    ap.add_argument("--no-live", action="store_true", help="skip the live-price check of new signals")
    a = ap.parse_args()
    for st in (sys.stdout, sys.stderr):
        try: st.reconfigure(encoding="utf-8", errors="replace")
        except Exception: pass

    now = calendar.timegm(time.strptime(a.now, "%Y-%m-%dT%H:%M:%S")) if a.now else time.time()
    data = Path(a.data); docs = Path(a.docs); cache_dir = data / "candles"
    data.mkdir(exist_ok=True); docs.mkdir(exist_ok=True)
    src = Demo() if a.demo else Coinbase()
    errors = []
    T_end = last_closed_day(now)

    cpath = data / "config.json"
    cfg = json.load(open(cpath, encoding="utf-8")) if cpath.exists() else {"inception": iso_day(T_end), "coins": {}, "universe_checked": ""}
    month = time.strftime("%Y-%m", time.gmtime(now))
    if a.demo and not Path(a.listing).exists():
        listing, vols = Demo.NAMES + ["GHOST"], {}
    else:
        listing, vols = read_listing(a.listing)
    if cfg["universe_checked"] != month or not cfg["coins"]:
        if not listing and not cfg["coins"]:
            sys.exit(f"No coin list found. Create {a.listing} with one coin symbol per line (the coins you can trade on Revolut X).")
        try:
            rep = select_universe(src, listing, vols, cfg, now, a, cache_dir, data / "universe_report.csv")
            cfg["universe_checked"] = month
            added = [r[0] for r in rep if r[1] == "added"]
            log(f"Universe check: {len(added)} added ({', '.join(added) or '-'}), {sum(1 for r in rep if r[1]=='excluded')} excluded, "
                f"{sum(1 for r in rep if r[1]=='error')} errors, {len(cfg['coins'])} tracked in total.")
        except Exception as e:
            errors.append(f"universe check failed: {e}"); log(errors[-1])
    json.dump(cfg, open(cpath, "w", encoding="utf-8"), indent=1, sort_keys=True)
    coins = sorted(cfg["coins"])
    if not coins: sys.exit("No coin passed the filters. See data/universe_report.csv.")

    # 2. candles
    arrays, stale, failed = {}, [], 0
    for sym in coins:
        try:
            rows = update_cache(src, sym, cache_dir, now)
        except Exception as e:
            failed += 1; errors.append(f"{sym}: download failed ({e}); using stored data"); rows = load_cache(cache_dir / f"{sym}.csv")
        if len(rows) < 2: errors.append(f"{sym}: no data"); continue
        arrays[sym] = to_arrays(rows)
        if arrays[sym]["t0"] + (len(arrays[sym]["c"]) - 1) * DAY < T_end: stale.append(sym)
    if stale: errors.append(f"{len(stale)} coin(s) have no candle for the last closed day yet: {', '.join(stale)}")
    log(f"Candles ready for {len(arrays)} coins; last closed day {iso_day(T_end)}; {failed} download failure(s).")
    if failed > len(coins) / 2: sys.exit("More than half of the downloads failed; stopping so the problem is visible.")

    # 3. replay
    inc = day_ts(cfg["inception"])
    fwd_days = (T_end - inc) // DAY
    span = max(a.hist_days, fwd_days + 365)
    TB = T_end - span * DAY; nB = span + 1
    nA = int((T_end - inc) // DAY) + 1
    W, EQB, EQA, TR = {}, {}, {}, []
    for sym, d in arrays.items():
        t0, n = d["t0"], len(d["c"])
        iB = max(0, (TB - t0) // DAY)
        iA = (day_ts(cfg["coins"][sym]) - t0) // DAY
        for m in MODELS:
            w = weights(m, d); W[(sym, m)] = w
            eqb, _ = replay(d["c"], w, iB); EQB[(sym, m)] = place(eqb, t0, iB, TB, nB)
            if 0 <= iA < n:
                eqa, trs = replay(d["c"], w, iA); EQA[(sym, m)] = place(eqa, t0, iA, inc, nA)
                for (i, wf, wt, px, fee) in trs: TR.append((t0 + i * DAY, sym, m, wf, wt, px, fee))
    TR.sort()
    dates_B = [iso_day(TB + k * DAY) for k in range(nB)]
    dates_A = [iso_day(inc + k * DAY) for k in range(nA)]
    portB = {m: portfolio_index([EQB[(s, m)] for s in arrays if (s, m) in EQB]) for m in MODELS}
    portA = {m: portfolio_index([EQA[(s, m)] for s in arrays if (s, m) in EQA]) for m in MODELS}
    mets = {}
    for m in MODELS:
        ws = [W[(s, m)][(day_ts(cfg["coins"][s]) - arrays[s]["t0"]) // DAY:] for s in arrays if (s, m) in EQA]
        expo = float(np.mean(np.concatenate(ws))) if ws else 0.0
        mets[m] = metrics(portA[m], expo, sum(1 for t in TR if t[2] == m))

    # 4. live check of new signals
    fills_path = data / "live_fills.csv"; fills = {}
    if fills_path.exists():
        for r in csv.DictReader(open(fills_path, encoding="utf-8")): fills[r["key"]] = r
    new_events = 0
    if not a.no_live:
        tick = {}
        for (t, sym, m, wf, wt, px, fee) in TR:
            key = f"{iso_day(t)}|{sym}|{m}"
            if m == "hold" or key in fills: continue
            try:
                if sym not in tick: tick[sym] = src.ticker(sym, now)
            except Exception as e:
                errors.append(f"{sym}: live price unavailable ({e})"); continue
            lag = (now - (t + DAY)) / 3600
            adverse = (tick[sym] - px) / px * (1 if wt > wf else -1)
            fills[key] = dict(key=key, seen_utc=iso_full(now), close_px=f"{px:.8g}", seen_px=f"{tick[sym]:.8g}", lag_h=f"{lag:.1f}", adverse_pct=f"{adverse*100:.3f}")
            new_events += 1
        with open(fills_path, "w", newline="", encoding="utf-8") as f:
            w_ = csv.DictWriter(f, fieldnames=["key", "seen_utc", "close_px", "seen_px", "lag_h", "adverse_pct"]); w_.writeheader(); w_.writerows(fills.values())

    # 5. outputs
    with open(data / "trades.csv", "w", newline="", encoding="utf-8") as f:
        w_ = csv.writer(f); w_.writerow(["signal_day", "coin", "model", "weight_from", "weight_to", "close_price", "fee_usd"])
        for (t, sym, m, wf, wt, px, fee) in TR: w_.writerow([iso_day(t), sym, m, f"{wf:.3f}", f"{wt:.3f}", f"{px:.8g}", f"{fee:.4f}"])
    with open(data / "portfolio_forward.csv", "w", newline="", encoding="utf-8") as f:
        w_ = csv.writer(f); w_.writerow(["date"] + MODELS)
        for k, dstr in enumerate(dates_A): w_.writerow([dstr] + [f"{portA[m][k]:.4f}" if not np.isnan(portA[m][k]) else "" for m in MODELS])
    with open(data / "runs.csv", "a", newline="", encoding="utf-8") as f:
        w_ = csv.writer(f)
        if f.tell() == 0: w_.writerow(["run_utc", "last_closed_day", "coins", "download_failures", "new_signals", "notes"])
        w_.writerow([iso_full(now), iso_day(T_end), len(arrays), failed, new_events, "; ".join(errors)[:300]])

    last_trades = []
    for (t, sym, m, wf, wt, px, fee) in reversed(TR):
        if m == "hold": continue
        fl = fills.get(f"{iso_day(t)}|{sym}|{m}")
        last_trades.append([iso_day(t), sym, m, clean(wf, 3), clean(wt, 3), clean(px),
                            clean(float(fl["seen_px"])) if fl else None, clean(float(fl["lag_h"]), 3) if fl else None,
                            clean(float(fl["adverse_pct"]), 3) if fl else None])
        if len(last_trades) >= 150: break

    coin_out = {}
    for sym, d in arrays.items():
        t0 = d["t0"]; iB = max(0, (TB - t0) // DAY)
        coin_out[sym] = dict(start=cfg["coins"][sym],
                             price=[clean(x) for x in place(d["c"], t0, 0, TB, nB)],
                             eq={m: [clean(x, 5) for x in EQB[(sym, m)]] for m in MODELS},
                             w={m: [clean(x, 3) for x in place(W[(sym, m)], t0, iB, TB, nB)] for m in MODELS})
    payload = dict(demo=bool(a.demo), generated_utc=iso_full(now), last_closed_day=iso_day(T_end), inception=cfg["inception"],
                   models=MODELS, dates_B=dates_B, dates_A=dates_A, cost_pct=COST * 100,
                   portB={m: [clean(x, 6) for x in portB[m]] for m in MODELS},
                   portA={m: [clean(x, 6) for x in portA[m]] for m in MODELS},
                   metrics=mets, coins=coin_out, trades=last_trades, errors=errors[:20],
                   n_coins=len(arrays))
    wk, md = weekly_report(now, T_end, cfg, mets, portB, arrays, W, TR, fills, data / "runs.csv", errors, stale, failed)
    (data / "weekly").mkdir(exist_ok=True)
    (data / "weekly" / f"{wk}.md").write_text(md, encoding="utf-8"); (data / "weekly" / "latest.md").write_text(md, encoding="utf-8")
    tpl_path = Path(__file__).parent / "dashboard_template.html"
    tpl = tpl_path.read_text(encoding="utf-8")
    html = tpl.replace("__DATA_JSON__", json.dumps(payload, separators=(",", ":")))
    if "<!doctype" not in html[:200].lower():
        html = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
                '<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,sans-serif}[hidden]{display:none!important}</style></head><body>' + html + '</body></html>')
    (docs / "index.html").write_text(html, encoding="utf-8")
    log(f"Done: {len(arrays)} coins, {len(TR)} paper trades since {cfg['inception']}, {new_events} new signal(s) checked against live prices.")
    for m in MODELS:
        x = mets[m]; log(f"  {m:<13} return {x['ret']*100:+6.1f}%  maxDD {x['maxdd']*100:6.1f}%  invested {x['expo']*100:4.0f}%  trades {x['trades']}")
    if errors: log("Notes:", *errors, sep="\n  ")


if __name__ == "__main__":
    main()
