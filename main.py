"""Selective trend hold: broad downside protection, no routine rebalancing."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
from makefun_bars import run

# Require enough history to avoid reacting to the opening minutes.
WARMUP = 150
TREND = 55
ENTRY_BPS = 15
STOP_BPS = 250
COOLDOWN = 60
BREAK_WINDOW = 120
BREAK_BPS = 150
SIZE_BPS = 9800


class Strategy:
    def __init__(self):
        self.closes = []
        self.high = 0
        self.cool_until = 0
        self.armed = True
        self.was_up = False

    def on_batch(self, state, batch):
        symbol = "CBBTC"
        for fill in batch["fills"]:
            if fill["symbol"] == symbol and fill["status"] == "filled":
                if fill["side"] == "buy":
                    self.high = int(fill["price"])
                else:
                    self.high = 0
                    self.cool_until = state.seq + COOLDOWN
                    self.armed = False
        bar = next((b for b in batch["bars"] if b["symbol"] == symbol), None)
        if bar is None:
            return []
        price = int(bar["c"])
        self.closes.append(price)
        n = len(self.closes)
        window = min(TREND, n - 1)
        up = (window > 0 and price * window > sum(self.closes[-window:])
              and price * 10000 > self.closes[-window - 1] * (10000 + ENTRY_BPS))
        # A new rising regime is required after each confirmed exit.
        if not up:
            self.armed = True
        fresh = up and not self.was_up
        self.was_up = up
        # The published race is 1,440 minutes; use bar time, including gaps.
        last_time = state.hello["first_close_ms"] + (state.warmup_bars + 1439) * 60000
        if state.warming_up or state.t >= last_time or n < WARMUP:
            return []
        held = state.positions.get(symbol)
        if held and held.qty:
            self.high = max(self.high, price)
            hard_break = (n > BREAK_WINDOW and price * 10000 <
                          self.closes[-BREAK_WINDOW - 1] * (10000 - BREAK_BPS))
            if price * 10000 < self.high * (10000 - STOP_BPS) or hard_break:
                return [{"side": "sell", "symbol": symbol, "qty": held.qty,
                         "max_slippage_bps": 500}]
        elif up and self.armed and state.seq >= self.cool_until and (self.cool_until == 0 or fresh):
            amount = min(state.cash * SIZE_BPS // 10000, state.weight_room(symbol))
            if amount >= int(state.hello["fees"]["min_notional_quote_units"]):
                return [{"side": "buy", "symbol": symbol,
                         "notional_quote_units": amount, "max_slippage_bps": 500}]
        return []


if __name__ == "__main__":
    run(Strategy().on_batch)
