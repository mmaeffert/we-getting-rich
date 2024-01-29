import unittest
from short import Short

class TestShortClass(unittest.TestCase):

    def test_short_update_balance_profit(self):
        test_object = Short(87.3, 49, 10, 1, 1, None, "short")
        test_object.update_balance(78.4)
        self.assertEqual(round(test_object.get_balance_amt(), 2), 98.95)
        
    def test_short_update_balance_loss(self):
        test_object = Short(87.3, 49, 10, 1, 1, None, "short")
        test_object.update_balance(90.12)
        self.assertEqual(round(test_object.get_balance_amt(), 2), 33.17)

    def test_short_update_balance_for_negative_current_price(self):
        test_object = Short(87.3, 49, 10, 1, 1, None, "short")
        with self.assertRaises(Exception):
            test_object.update_balance(-10)

    def test_sell_for_loss(self):
        test_object = Short(110, 87, 15, 0.8, 2, None, "short")
        test_object.sell(115)
        self.assertEqual(round(test_object.get_balance_amt(), 2), 27.68)

    def test_sell_for_profit(self):
        test_object = Short(110, 87, 15, 0.8, 1.2, None, "short")
        test_object.sell(105)
        self.assertEqual(round(test_object.get_balance_amt(), 2), 146.32)

    def test_sell_when_closed(self):
        test_object = Short(110, 87, 15, 0.8, 1.2, None, "short")
        test_object.set_liquidated(True)
        test_object.update_is_closed()
        with self.assertRaises(Exception):
            test_object.sell(105)

    def test_sell_past_liquidated(self):
        test_object = Short(110, 87, 15, 0.8, 1.2, None, "short")
        test_object.set_liquidated(True)
        test_object.update_is_closed()
        with self.assertRaises(Exception):
            test_object.sell(140)

    def test_liquidate_price(self):
        test_object = Short(110, 87, 15, 0.8, 1.2, None, "short")
        self.assertEqual(round(test_object.liquidate_price, 2), 117.33)

    def test_stop_loss_price(self):
        test_object = Short(110, 87, 15, 0.8, 1.2, None, "short")
        self.assertEqual(round(test_object.stop_loss_price, 2), 115.87)

    def test_sell_limit_price(self):
        test_object = Short(110, 87, 15, 0.8, 1.2, None, "short")
        self.assertEqual(round(test_object.sell_limit_price, 2), 101.2)
