import time
import csv
from nubra_python_sdk.start_sdk import InitNubraSdk, NubraEnv
from nubra_python_sdk.marketdata.market_data import MarketData

from config import *
from strategy import compute_quotes
from simulator import Simulator

# SDK init
nubra = InitNubraSdk(NubraEnv.UAT, env_creds=True)
md = MarketData(nubra)

sim = Simulator()

cfg = {
    "BASE_SPREAD_TICKS": BASE_SPREAD_TICKS,
    "ALPHA": ALPHA,
    "K_INVENTORY": K_INVENTORY,
    "TICK_SIZE": TICK_SIZE,
    "Q_MAX": Q_MAX
}

# CSV logging
f = open("logs/mm_log.csv", "w", newline="")
writer = csv.writer(f)
writer.writerow([
    "timestamp", "bid", "ask",
    "imbalance", "quoted_spread",
    "bid_q", "ask_q",
    "inventory", "pnl", "pnl_base"
])

print("Market maker running... Ctrl+C to stop")

try:
    while True:
        try:
            quote = md.quote(ref_id=REF_ID, levels=1)
        except Exception as e:
            print(f"Market data error, skipping tick: {e}")
            time.sleep(0.5)
            continue

        ob = quote.orderBook

        if not ob.bid or not ob.ask:
            continue

        bid = ob.bid[0].price
        ask = ob.ask[0].price
        v_bid = ob.bid[0].quantity
        v_ask = ob.ask[0].quantity

        market_spread = ask - bid
        vol_factor = min(market_spread / (2 * TICK_SIZE), 3)

        cfg_adj = cfg.copy()
        cfg_adj["ALPHA"] = cfg["ALPHA"] * vol_factor
        cfg_adj["Q_MAX"] = Q_MAX

        cfg_adj["INV_TIME"] = sim.inventory_time

        bid_q, ask_q = compute_quotes(
            bid, ask, v_bid, v_ask, sim.inventory, cfg_adj
        )

        sim.step(bid, ask, bid_q, ask_q)
        mid = (bid + ask) / 2
        imbalance = (v_bid - v_ask) / max(v_bid + v_ask, 1)
        quoted_spread = ask_q - bid_q

        writer.writerow([
            ob.timestamp,
            bid, ask,
            imbalance, quoted_spread,
            bid_q, ask_q,
            sim.inventory,
            sim.pnl(mid),
            sim.pnl_base(mid)
        ])

        print(
            f"Inv={sim.inventory} | "
            f"PnL={sim.pnl(mid):.2f} | "
            f"Base={sim.pnl_base(mid):.2f}"
        )

        time.sleep(SLEEP_SEC)

except KeyboardInterrupt:
    print("Stopped.")
    f.close()