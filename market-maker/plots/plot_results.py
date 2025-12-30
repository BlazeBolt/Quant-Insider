import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../logs/mm_log.csv")

# =========================
# 1. PnL: Adaptive vs Baseline
# =========================
plt.figure()
plt.plot(df["pnl"], label="Adaptive MM")
plt.plot(df["pnl_base"], label="Baseline MM", linestyle="--")
plt.xlabel("Time")
plt.ylabel("PnL (₹)")
plt.title("PnL Comparison: Adaptive vs Baseline")
plt.legend()
plt.grid()
plt.show()

# =========================
# 2. Inventory Over Time
# =========================
plt.figure()
plt.plot(df["inventory"])
plt.xlabel("Time")
plt.ylabel("Inventory (lots)")
plt.title("Inventory Over Time")
plt.grid()
plt.show()

# =========================
# 3. Imbalance vs Quoted Spread
# =========================
quoted_spread = df["ask_q"] - df["bid_q"]

plt.figure()
plt.scatter(df["imbalance"], quoted_spread, s=6, alpha=0.6)
plt.xlabel("Order Book Imbalance")
plt.ylabel("Quoted Spread (paise)")
plt.title("Spread Adaptation vs Imbalance")
plt.grid()
plt.show()

# =========================
# 4. Market Spread vs Quoted Spread
# =========================
market_spread = df["ask"] - df["bid"]

plt.figure()
plt.plot(market_spread, label="Market Spread")
plt.plot(quoted_spread, label="Quoted Spread")
plt.xlabel("Time")
plt.ylabel("Spread (paise)")
plt.title("Market Spread vs Quoted Spread")
plt.legend()
plt.grid()
plt.show()
