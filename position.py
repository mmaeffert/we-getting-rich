# This the superclass of either a short or a long position. This class should never be instantiated, you should use the short and long class instead

class Position:

    # Price where positions were opened
    entry_price = None

    # Amount invested per position - 50 means 50 for short and 50 for long, meaning investing 100 overall
    invest = None

    # Current balance
    balance = None

    # leverage
    leverage = None

    # Bool whether a position was sold for set sell limit
    sold_at_sell_limit = None

    # Sell limit in percent decimal notation, uncluding leverage
    # If you want to sell at 20% profit, you have to set this to 0.2
    # This refers to the profit when taking leverage into account
    # Lets say you have a leverage of 20 and want to sell when your position is at +80% (meaning the stock moved 4% because 20 * 4% equals 80%), you have to set this to 0.8
    sell_limit_decimal = None

    # Defines the stock price where the position is set to be sold
    sell_limit_price = None

    # Same as sell_limit_decimal, only with stop loss
    stop_loss_decimal = None

    # Defines the stock price where the position is sold for loss
    stop_loss_price = None

    # Bool whether a stop loss has triggered
    stop_loss_triggered = None

    # Defines the stock price where the position is liquidated
    liquidate_price = None

    # Bool whether a position has been liquidated
    liquidated = None

    # Defines whether a position is closed, meaning sold for profit, stop loss triggered of liquidated
    is_closed = None

    # Defines the type of the Position with it being either "long" or "short"
    type = None

    # Fee object to take into account when ever a transaction is executed
    fee = None

    def __init__(self, entry_price, invest, leverage, stop_loss_decimal, sell_limit_decimal, fee):

        self.entry_price = entry_price
        self.invest = invest
        self.leverage = leverage
        self.stop_loss_decimal = stop_loss_decimal
        self. stop_loss_decimal = sell_limit_decimal
        self.fee = fee

    def update_is_closed(self):

        # Set is_closed when either liquidated, stop_loss_triggered or sold_at_sell_limit is true
        if self.sold_at_sell_limit or self.liquidated or self. stop_loss_triggered:
            self.is_closed = True

    # returns a decimal percent value of current balance divided by invest
    def get_balance_pc(self):
        return self.balance / self.invest
    
    def set_liquidated(self, i):
        self.liquidated = i

    def set_sold_at_sell_limit(self, i):
        self.sold_at_sell_limit = i

    def set_stop_loss_triggered(self, i):
        self.stop_loss_triggered = i

    # Returns current balance in it's value - e.g. 50
    def get_balance_amt(self):
        return self.balance


        