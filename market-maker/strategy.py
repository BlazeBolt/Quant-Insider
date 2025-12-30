def round_to_tick(price, tick_size):
    if price <= 0:
        return price
    return round(price / tick_size) * tick_size


def compute_quotes(bid, ask, v_bid, v_ask, inventory, cfg):
    mid = (bid + ask) / 2

    imbalance = (v_bid - v_ask) / max(v_bid + v_ask, 1)

    s0 = cfg["BASE_SPREAD_TICKS"] * cfg["TICK_SIZE"]
    spread = s0 * (1 + cfg["ALPHA"] * abs(imbalance))

    inv_time = cfg.get("INV_TIME", 0)
    time_penalty = min(inv_time / 50, 1)  # caps at 1
    skew = cfg["K_INVENTORY"] * inventory * (1 + time_penalty)

    imb = imbalance
    # asymmetric spread based on imbalance direction
    bid_adj = spread * (0.5 - 0.25 * imb)
    ask_adj = spread * (0.5 + 0.25 * imb)

    bid_q = mid - bid_adj - skew
    ask_q = mid + ask_adj - skew

    # Controlled aggression: cross touch on strong imbalance
    if imbalance > 0.6:
        bid_q = ask   # cross to buy
    elif imbalance < -0.6:
        ask_q = bid   # cross to sell

    if inventory >= cfg["Q_MAX"]:
        bid_q = 0
    if inventory <= -cfg["Q_MAX"]:
        ask_q = 10**9

    bid_q = round_to_tick(bid_q, cfg["TICK_SIZE"])
    ask_q = round_to_tick(ask_q, cfg["TICK_SIZE"])

    return bid_q, ask_q
