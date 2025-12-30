# Adaptive Market Making Strategy – NIFTY Options (UAT Live)

## Instrument
- Underlying: NIFTY
- Expiry: 6 January 2026
- Option: ATM Call Option
- Ref ID: 1933042
- Lot Size: 65
- Tick Size: ₹0.05

---

## Objective
Build a simulated market-making strategy using live UAT order-book data and benchmark its performance against a constant-spread baseline.

---

## Strategy Overview

### 1. Mid-Price Quoting
The mid-price is computed as:
m_t = (best_bid + best_ask) / 2


A base spread of two ticks is applied symmetrically around the mid-price.

---

### 2. Order Book Imbalance
An imbalance signal is computed using L1 volumes:
A base spread of two ticks is applied symmetrically around the mid-price.

---

### 2. Order Book Imbalance
An imbalance signal is computed using L1 volumes:
I_t = (V_bid - V_ask) / (V_bid + V_ask)

The quoted spread adapts dynamically:
s_t = s_0 * (1 + α * |I_t|)

This widens spreads during demand–supply asymmetry to reduce adverse selection.

---

### 3. Inventory-Based Skew
To control risk, inventory-based skew is applied:
bid = m_t - s_t/2 - k * Q_t
ask = m_t + s_t/2 - k * Q_t

If inventory reaches a predefined limit, quoting on the risk-increasing side is disabled.

---

### 4. Baseline Strategy
The benchmark strategy uses a constant spread with no imbalance awareness or inventory control.

---

## Simulation & Evaluation

- Deterministic L1 fill rules
- Unit inventory updates
- Mark-to-market PnL tracking
- CSV logging of prices, imbalance, spreads, inventory, and PnL
- Visual comparison of adaptive vs baseline strategy

---

## Results
The adaptive strategy demonstrates:
- Higher cumulative PnL than baseline
- Stable, bounded inventory
- Responsive spread widening during imbalance
- Improved risk-adjusted performance

---

## Files
- `run.py` – main simulation loop
- `strategy.py` – quoting logic
- `simulator.py` – fill & PnL logic
- `logs/mm_log.csv` – execution logs
- `plots/plot_results.py` – visualization

---

## Notes
The strategy prioritizes clarity, stability, and robustness over complexity, aligning with real-world