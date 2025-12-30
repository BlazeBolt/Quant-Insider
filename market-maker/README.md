# Market Making Strategy — NIFTY Options (UAT Live)

## Overview

This repository contains my submission for the **Quant Insider Market Making Challenge (UAT Live Edition)**.

The objective was to design and run a **simulated market-making strategy** on **live UAT order book data** for **NIFTY options (expiry: 6 Jan 2026)** and benchmark it against a naive constant-spread baseline.

The strategy dynamically adapts its quotes based on:

* **Order book imbalance**
* **Inventory risk**

Performance is evaluated using:

* PnL comparison vs baseline
* Inventory stability
* Responsiveness to market conditions
* Clarity of logic and analysis

---

## Instrument Selection

* Underlying: **NIFTY**
* Expiry: **6 January 2026**
* Instrument type: **Options**
* Selected contract: **Near-ATM Call Option**

The ATM option was selected by:

1. Fetching all NIFTY options expiring on 6 Jan 2026
2. Computing the approximate ATM strike using live NIFTY index price
3. Choosing the closest strike available in the instrument list

This ensures:

* High liquidity
* Meaningful bid–ask dynamics
* Realistic market-making behavior

---

## Strategy Design

### 1. Market Data Inputs (L1)

At each timestep, the strategy reads:

* Best bid price (`b_t`)
* Best ask price (`a_t`)
* Volume at best bid (`V_bid`)
* Volume at best ask (`V_ask`)

From these, we compute:

* **Mid price**
* **Order book imbalance**

---

### 2. Order Book Imbalance Signal

Imbalance is defined as:

[
I_t = \frac{V_{bid} - V_{ask}}{V_{bid} + V_{ask}} \in [-1, 1]
]

Interpretation:

* Positive imbalance → stronger buying pressure
* Negative imbalance → stronger selling pressure
* Higher absolute value → higher adverse selection risk

---

### 3. Adaptive Spread Logic

A base spread is defined using tick size:

[
s_0 = 2 \times \text{tick size}
]

The quoted spread adapts based on imbalance:

[
s_t = s_0 \times (1 + \alpha |I_t|)
]

Where:

* `α` controls how aggressively the spread widens under imbalance

This allows the strategy to:

* Tighten spreads during balanced, liquid conditions
* Widen spreads during one-sided markets

---

### 4. Inventory-Based Skew (Risk Control)

To control inventory risk, quotes are skewed based on current position:

[
\hat{b}_t = m_t - \frac{s_t}{2} - k Q_t
]
[
\hat{a}_t = m_t + \frac{s_t}{2} - k Q_t
]

Where:

* `Q_t` is current inventory
* `k` controls the strength of inventory pressure

Behavior:

* Long inventory → bid becomes less aggressive, ask more aggressive
* Short inventory → bid more aggressive, ask less aggressive

Inventory is capped to prevent runaway exposure.

---

### 5. Fill Simulation (L1 Deterministic)

To focus on strategy logic rather than exchange microstructure, fills are simulated using deterministic L1 rules:

* Buy fill if quoted bid ≥ market ask
* Sell fill if quoted ask ≤ market bid

State updates:

* Inventory
* Cash
* Mark-to-market PnL

---

## Baseline Strategy (Benchmark)

A naive constant-spread market maker is implemented as a benchmark:

* Fixed spread = base spread
* No imbalance awareness
* No inventory skew

Both strategies run **on the same market data**, allowing a fair comparison.

---

## Results Summary

### Inventory Behavior

* Inventory remained bounded throughout the session
* No runaway drift
* Inventory skew effectively pulled positions back toward zero

### PnL Behavior

* Adaptive strategy showed **higher variance but better opportunity capture**
* Baseline strategy remained flat, missing microstructure signals
* Losses during trending periods highlighted adverse selection risk, which is expected in live conditions

### Spread Responsiveness

* Quoted spreads widened during high imbalance
* Spreads tightened during balanced conditions
* Behavior matched the intended design

---

## Plots Included

The repository includes:

1. **PnL comparison** (Adaptive vs Baseline)
2. **Inventory over time**
3. **Imbalance vs quoted spread**
4. **Market spread vs quoted spread**

All plots are generated from logged CSV data for transparency and reproducibility.

---

## Repository Structure

```
market-maker/
├── run.py              # Main execution loop (live UAT)
├── strategy.py         # Quoting logic (spread + skew)
├── simulator.py        # Fill simulation & PnL tracking
├── config.py           # Strategy parameters
├── logs/
│   └── mm_log.csv      # Timestamped market + strategy logs
├── plots/
│   └── *.png           # Analysis plots
├── analysis/
│   └── plot_results.py # Plotting script
└── README.md
```

---

## Assumptions & Limitations

* L1 order book only (no queue position modeling)
* Deterministic fills (no latency or partial fills)
* No volatility forecasting or option Greeks used
* Focused on clarity, robustness, and interpretability

These choices were intentional to align with the competition’s evaluation criteria.

---

## Conclusion

This submission demonstrates:

* A clear and well-structured market-making strategy
* Real-time responsiveness to order book conditions
* Effective inventory risk control
* Transparent benchmarking against a baseline

The strategy prioritizes **risk discipline and interpretability**, which are essential for deployable market-making systems.