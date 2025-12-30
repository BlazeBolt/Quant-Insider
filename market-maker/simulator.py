class Simulator:
    def __init__(self):
        self.inventory = 0
        self.cash = 0

        self.inventory_base = 0
        self.cash_base = 0

        self.inventory_time = 0

    def step(self, bid, ask, bid_q, ask_q):
        trade_occurred = False

        # -------------------------
        # Adaptive strategy fills
        # -------------------------
        if bid_q >= ask:
            self.inventory += 1
            self.cash -= ask
            trade_occurred = True

        elif ask_q <= bid:
            self.inventory -= 1
            self.cash += bid
            trade_occurred = True

        # Inventory time tracking
        if trade_occurred:
            self.inventory_time = 0
        else:
            if self.inventory != 0:
                self.inventory_time += 1
            else:
                self.inventory_time = 0

        # -------------------------
        # Baseline strategy fills
        # -------------------------
        base_mid = (bid + ask) / 2
        base_spread = 10  # 2 ticks = 10 paise
        base_bid = base_mid - base_spread / 2
        base_ask = base_mid + base_spread / 2

        if base_bid >= ask:
            self.inventory_base += 1
            self.cash_base -= ask

        elif base_ask <= bid:
            self.inventory_base -= 1
            self.cash_base += bid

    def pnl(self, mid):
        return self.cash + self.inventory * mid

    def pnl_base(self, mid):
        return self.cash_base + self.inventory_base * mid