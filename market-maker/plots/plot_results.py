import pandas as pd
import matplotlib.pyplot as plt

# Load log
df = pd.read_csv("../logs/mm_log.csv")

# Convert timestamp if needed
# df["timestamp"] = pd.to_datetime(df["timestamp"])

# =========================
# 1. PnL: Adaptive vs Baseline
# =========================
plt.figure()
plt.plot(df["pnl"], label="Adaptive MM")
plt.plot(df["pnl_base"], label="Baseline MM", linestyle="--")
plt.xlabel("Time")
plt.ylabel("PnL")
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
plt.ylabel("Inventory")
plt.title("Inventory Over Time")
plt.grid()
plt.show()

# =========================
# 3. Imbalance vs Quoted Spread
# =========================
plt.figure()
plt.scatter(df["imbalance"], df["quoted_spread"], s=5)
plt.xlabel("Order Book Imbalance")
plt.ylabel("Quoted Spread")
plt.title("Spread Adaptation vs Imbalance")
plt.grid()
plt.show()

# =========================
# 4. Market Spread vs Quoted Spread
# =========================
market_spread = df["ask"] - df["bid"]

plt.figure()
plt.plot(market_spread, label="Market Spread")
plt.plot(df["quoted_spread"], label="Quoted Spread")
plt.xlabel("Time")
plt.ylabel("Spread")
plt.title("Market Spread vs Quoted Spread")
plt.legend()
plt.grid()
plt.show()
