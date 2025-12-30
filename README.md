Got it. Below is your **fully GitHub-safe version** of the same README.
I have **only changed the math formatting**, not the content or tone.

You can **replace your current README entirely with this**.

---

# Market Making Strategy – NIFTY Options (UAT Live)

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

Order book imbalance is defined as:

```text
imbalance = (V_bid - V_ask) / (V_bid + V_ask)
```

Interpretation:

* Positive imbalance → stronger buying pressure
* Negative imbalance → stronger selling pressure
* Higher absolute value → higher adverse selection risk

---

### 3. Adaptive Spread Logic

Base spread is defined using tick size:

```text
base_spread = 2 * tick_size
```

The quoted spread adapts based on imbalance:

```text
spread = base_spread * (1 + alpha * abs(imbalance))
```

Where:

* `alpha` controls how aggressively the spread widens under imbalance

This allows the strategy to:

* Tighten spreads during balanced, liquid conditions
* Widen spreads during one-sided markets

---

### 4. Inventory-Based Skew (Risk Control)

To control inventory risk, quotes are skewed based on current position:

```text
bid_quote = mid - spread / 2 - k * inventory
ask_quote = mid + spread / 2 - k * inventory
```

Where:

* `inventory` is the current position
* `k` controls the strength of inventory pressure

Behavior:

* Long inventory → bid becomes less aggressive, ask more aggressive
* Short inventory → bid more aggressive, ask less aggressive

Inventory is capped to prevent runaway exposure.

---

### 5. Fill Simulation (L1 Deterministic)

To focus on strategy logic rather than exchange microstructure, fills are simulated using deterministic Level-1 rules:

```text
If bid_quote >= market_ask → buy filled at market_ask
If ask_quote <= market_bid → sell filled at market_bid
```

State updates:

* Inventory
* Cash
* Mark-to-market PnL

---

## Baseline Strategy (Benchmark)

A naive constant-spread market maker is implemented as a benchmark:

```text
bid_base = mid - base_spread / 2
ask_base = mid + base_spread / 2
```

Characteristics:

* Fixed spread
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

---

If you want next:

* a **short “judge skim” version**, or
* a **parameter explanation (alpha, k) justification**, or
* help writing the **final submission note**

say the word.
