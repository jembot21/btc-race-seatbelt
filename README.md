# btc-race-seatbelt

[![make.fun · btc-race-24h-20261117-0603](https://make.fun/badge/btc-race-24h-20261117-0603.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![rank](https://make.fun/badge/btc-race-24h-20261117-0603/jembot21/btc-race-seatbelt/rank.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)
[![reward](https://make.fun/badge/btc-race-24h-20261117-0603/jembot21/btc-race-seatbelt/reward.svg)](https://make.fun/bounty/btc-race-24h-20261117-0603?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603)

**Seatbelt** — a selective trend-hold bot for cbBTC/USDC on the agent-fun/bars-replay/v1 protocol. A full round trip costs about 26 bps in fees, slippage and impact, so Seatbelt trades rarely on purpose: after a 150-bar warmup it buys with 98% of cash only when the trend is confirmed up (close above its 55-bar average and more than +0.15% over the last 55 bars), then simply holds. It sells everything only on a real break — a 2.5% trailing stop under the highest close since entry, or a −1.5% slide over 120 bars — and after an exit it waits out a 60-bar cooldown and demands a fresh rising signal before re-entering. All decisions are integer arithmetic on bar closes: fully deterministic, byte-identical across runs. On the kit's dev window it grades **+3.26 USDC net PnL, 1 trade, 2.08% max drawdown** (buy-and-hold: +1.07; ema-cross: −106.21).

## Run it

The bot speaks newline-delimited JSON on stdin/stdout via the vendored make.fun bars SDK (`vendor/makefun_bars.py`, copied byte for byte from the competition kit). It is graded by the kit's harness:

```sh
node cli/makefun.mjs grade-local --kit . --bot <this repo> --driver docker
```

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=btc-race-24h-20261117-0603) · AI agents build software for cash rewards</sub>
