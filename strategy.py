from position import Position
import csv

class Strategy:

    # positions = []

    def __init__(self, stock_data, stop_loss, leverage, sell_limit, handle, invest):
        self.stock_data = stock_data
        self.stop_loss = stop_loss
        self.leverage = leverage
        self.sell_limit = sell_limit
        self.handle = handle
        self.invest = invest
        self.invested = 0
        self.positions = []

    def evaluate_strategy(self):
        counter = 0
        for entry in self.stock_data:
            counter += 1
            self.add_position(entry)
        # print("counter" + str(counter))
        self.short_liquidated_count = self.count_liquidated("short")
        self.long_liquidated_count = self.count_liquidated("long")
        self.absolute_lost_count = self.count_lost()
        self.absolute_win_count = self.count_win()
        self.balance = round(self.get_balance(), 2)
        self.still_open_count = self.count_still_open()
        self.profit_from_sold = round(self.balance - self.invested, 2)
        self.money_lost = self.absolute_lost_count * 100
        self.profit_in_percent = self.profit_from_sold / self.invested * 100

    def get_performanc_result(self):
        if self.profit_from_sold == None:
            return Exception("Strategy not yet evaluated")

        return {
            "handle": self.handle,
            "stop_loss": self.stop_loss,
            "leverage": self.leverage,
            "sell_limit": self.sell_limit,
            "short_liquidated_count": self.short_liquidated_count,
            "long_liquidated_count": self.long_liquidated_count,
            "absolut_lost_count": self.absolute_lost_count,
            "absolute_win_count": self.absolute_win_count,
            "still_open_count": self.still_open_count,
            "invested": self.invested,
            "balance": self.balance,
            "money_lost": self.money_lost,
            "profit_from_sold": self.profit_from_sold,
            "profit_in_percent": self.profit_in_percent
        }

    def add_position(self, price_now):
        self.invested = self.invested + self.invest * 2
        self.positions.append(Position(price_now, self.sell_limit, self.leverage, self.invest, self.stop_loss))
        for position in self.positions:
            position.eval(price_now)
        # print("length poisitions:" +  str(len(self.positions)))

    def count_liquidated(self, mode):
        count = 0
        for position in self.positions:
            if mode == "short" and position.short_liquidated:
                count = count + 1
            if mode == "long" and position.long_liquidated:
                count = count + 1
        return count

    def count_lost(self):
        count = 0
        for position in self.positions:
            if position.short_liquidated and position.long_liquidated:
                count = count + 1
        return count

    def count_win(self):
        count = 0
        for position in self.positions:
            if position.long_liquidated == False and position.short_liquidated == True and position.closed:
                count = count + 1
            if position.long_liquidated == True and position.short_liquidated == False and position.closed:
                count = count + 1
        return count

    def get_balance(self):
        balance = 0
        for position in self.positions:
            balance = balance + position.current_balance
        return balance

    def get_balance_from_sold(self):
        balance = 0
        for position in self.positions:
            if position.closed:
                balance = balance + position.balance
        return balance

    def count_still_open(self):
        count = 0
        for position in self.positions:
            if position.closed == False:
                count = count + 1
        return count

    def __str__(self):
        table = "Data:\n"
        table += "+-----------------------+------------------+\n"
        table += "| Field                 | Value            |\n"
        table += "+-----------------------+------------------+\n"
        for key, value in self.get_performanc_result().items():
            table += f"| {key.ljust(22)} | {str(value).ljust(16)} |\n"
        table += "+-----------------------+------------------+\n"
        return table        