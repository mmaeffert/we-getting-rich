# This class represents a short position, it inherits from the Position class

from position import Position

class Short(Position):

    def __init__(self, entry_price, invest, leverage, stop_loss_decimal, sell_limit_decimal, fee, type):

        # Execute the parent constructor first
        super().__init__(entry_price, invest, leverage, stop_loss_decimal, sell_limit_decimal, fee, type)

    # Updates the balance of the position
    def update_balance(self, current_price):

        self.update_is_closed()
        
        # abort if position is closed
        if self.is_closed:
            return None
        
        # if current price is higher than the entry price:
        if current_price >= self.entry_price:
            
            balance_in_percent = current_price / self.entry_price - 1
            balance_in_percent_with_leverage = balance_in_percent * self.leverage
            multiplicator_to_apply = 1 - balance_in_percent_with_leverage
            self.balance = self.balance * multiplicator_to_apply

        # If price is lower than entry price
        else:

            balance_in_percent = (current_price / self.entry_price - 1) * (-1)
            balance_in_percent_with_leverage = balance_in_percent * self.leverage
            multiplicator_to_apply = balance_in_percent_with_leverage + 1
            self.balance = self.balance * multiplicator_to_apply

        
test_object = Short(87.3, 49, 10, 1, 1, None, "short")
test_object.update_balance(78.4)
