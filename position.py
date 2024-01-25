class Position:

    short_dead = None
    long_dead = None
    current_balance = 0
    short_liquidated = False
    long_liquidated = False
    closed = False
    leverage = None


    def __init__(self, entry, sell_limit, leverage, invest = 50.0, stop_loss = 1):
        invest = invest - 1
        self.entry = entry
        self.limit = sell_limit
        self.leverage = leverage
        self.stop_loss = stop_loss
        self.short_dead = entry * (1 + (1 / leverage) * self.stop_loss)
        self.long_dead = entry * (1 - (1 / leverage) * self.stop_loss)
        self.current_balance = invest * 2
        self.invest = invest

        # print(self.current_balance)

    def eval(self, current):
        if self.closed:
            return
        else:
            self.liquidate(current)
            self.sell(current)
            if self.short_liquidated and self.long_liquidated:
                self.closed = True

    def liquidate(self, current):
        if self.closed:
            return

        if current > self.short_dead and self.short_liquidated == False:
            self.current_balance = self.current_balance - self.invest
            self.short_liquidated = True
        
        if current < self.long_dead and self.long_liquidated == False:
            self.current_balance = self.current_balance - self.invest
            self.long_liquidated = True

    def sell(self, current):
        if(current >= self.entry * (1 + self.limit) and self.long_liquidated == False) or (current <= self.entry * (1 - self.limit) and self.short_liquidated == False):
            print(f"sold for {self.invest * (1 + (self.limit * self.leverage))}")
            self.current_balance = self.invest * (1 + (self.limit * self.leverage))
            self.closed = True
            self.subtract_fee()

    def subtract_fee(self, fee = 1):
        self.current_balance = self.current_balance - fee

    def __str__(self):
        return f"Position entry: {self.entry} - Current Balance: {self.current_balance} - Closed: {str(self.closed)} - Short liquidated: {self.short_liquidated} - Long Liquidated: {self.long_liquidated}"
    
    def liquidated_string(self):
        return f"Short Liquid: {self.short_liquidated} - long liquid: {self.long_liquidated} - Closed: {self.closed}"


