# This class represents a short position, it inherits from the Position class

from position import Position

class Short(Position):

    def __init__(self, entry_price, invest, leverage, stop_loss_decimal, sell_limit_decimal, fee, type):

        # Execute the parent constructor first
        super().__init__(entry_price, invest, leverage, stop_loss_decimal, sell_limit_decimal, fee, type)

        # Set the short specific prices
        self.set_liquidate_price()
        self.set_stop_loss_price()
        self.set_sell_limit_price()


    # Sets the market price where position is liquidated
    def set_liquidate_price(self):
        self.liquidate_price = self.entry_price * (1 + 1 / self.leverage)

    # Sets the market price where position is sold for set profit
    def set_sell_limit_price(self):
        self.sell_limit_price = ( 1 - self.sell_limit_decimal / self.leverage ) * self.entry_price

    # Sets the market price where position is sold for set stop loss
    def set_stop_loss_price(self):
        self.stop_loss_price = ( 1 + self.stop_loss_decimal / self.leverage ) * self.entry_price


    # Updates the balance of the position
    def update_balance(self, current_price):

        if current_price <= 0:
            raise Exception("Current price can not be negative")

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

    # Sells the current position for given price, no matter if liquidated, sold at profit or stop loss triggered
    def sell(self, current_price):

        # Abort when position is closed
        if self.is_closed:
            raise Exception("Can not sell, position already closed")
        
        # Abort when liquidation price is reached
        if current_price > self.liquidate_price:
            raise Exception("Price is past liquidation")
        

        factor = (current_price / self.entry_price - 1) * (-1)
        factor_with_leverage = factor * self.leverage
        multiplicator_to_apply = factor_with_leverage + 1
        new_balance = self.invest * multiplicator_to_apply
        self.set_balance(new_balance)
    

        
        


