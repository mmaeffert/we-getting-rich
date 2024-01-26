class Position:
    """ Represents a trading position with both long and short components,
    including logic for trailing stop losses. """

    def __init__(self, entry_price, leverage, investment=50.0):
        """ Initialize the position with entry price and leverage. """
        if leverage <= 0:
            raise ValueError("Leverage must be greater than 0")

        self.entry_price = entry_price
        self.leverage = leverage
        self.investment = investment - 1  # accounting for some fixed fee
        self.current_balance = self.investment * 2
        self.short_stop_price = None
        self.long_stop_price = None
        self.highest_price_since_entry = None
        self.lowest_price_since_entry = None
        self.trailing_stop_loss_percentage = 0.05
        self.is_closed = False
        self.short_liquidated = False
        self.long_liquidated = False
        self.soft_liquidation_percentage = 0.10  # 10% soft liquidation point

    def update_trailing_stops(self, current_price):
        """ Update the trailing stop prices based on the current market price. """
        if not self.highest_price_since_entry:
            self.highest_price_since_entry = self.entry_price
        if not self.lowest_price_since_entry:
            self.lowest_price_since_entry = self.entry_price

        self.highest_price_since_entry = max(self.highest_price_since_entry, current_price)
        self.lowest_price_since_entry = min(self.lowest_price_since_entry, current_price)
        self.long_stop_price = self.highest_price_since_entry * (1 - self.trailing_stop_loss_percentage)
        self.short_stop_price = self.lowest_price_since_entry * (1 + self.trailing_stop_loss_percentage)

    def evaluate_position(self, current_price):
        """ Evaluate the current position based on the latest market price. """
        if self.is_closed:
            return

        self.soft_liquidate_if_needed(current_price)
        self.update_trailing_stops(current_price)
        self.sell_position_if_criteria_met(current_price)

    def soft_liquidate_if_needed(self, current_price):
        """ Soft liquidate the position if market conditions meet the soft liquidation criteria. """
        soft_liquidation_short = self.entry_price * (1 + self.soft_liquidation_percentage)  # +10%
        soft_liquidation_long = self.entry_price * (1 - self.soft_liquidation_percentage)  # -10%

        if current_price >= soft_liquidation_short and not self.short_liquidated:
            self.sell_short_position()
            self.long_stop_price = current_price  # Set trailing stop for long position

        if current_price <= soft_liquidation_long and not self.long_liquidated:
            self.sell_long_position()
            self.short_stop_price = current_price  # Set trailing stop for short position

    def sell_short_position(self):
        """ Sell the short position. """
        self.short_liquidated = True
        self.current_balance -= self.investment  # Assuming full loss of investment for simplicity
        print(f"Short position soft liquidated at {self.current_balance}")

    def sell_long_position(self):
        """ Sell the long position. """
        self.long_liquidated = True
        self.current_balance -= self.investment  # Assuming full loss of investment for simplicity
        print(f"Long position soft liquidated at {self.current_balance}")

    def sell_position_if_criteria_met(self, current_price):
        """ Sell the position if the current price meets the trailing stop loss criteria. """
        if (self.long_stop_price and current_price <= self.long_stop_price) or \
           (self.short_stop_price and current_price >= self.short_stop_price):
            self.current_balance = self.investment * (1 + (self.trailing_stop_loss_percentage * self.leverage))
            self.is_closed = True
            self.subtract_transaction_fee()
            print(f"Selling for {self.current_balance}")

    def subtract_transaction_fee(self, fee=1):
        """ Subtract a transaction fee from the current balance. """
        self.current_balance -= fee

    def __str__(self):
        """ String representation of the position's status. """
        return f"Position entry: {self.entry_price}, Current Balance: {self.current_balance}, " \
               f"Closed: {self.is_closed}, Short liquidated: {self.short_liquidated}, " \
               f"Long Liquidated: {self.long_liquidated}"

# Example usage:
# position = Position(entry_price=100, leverage=10)
# position.evaluate_position(current_price=110)  # Example of a +10% price movement triggering soft liquidation of short
# print(position)
