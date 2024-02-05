import unittest
from position import Position

class TestPositionClass(unittest.TestCase):

    def test_position_initialization(self):
        entry_price = 100
        invest = 50
        leverage = 10
        stop_loss_decimal = 0.1
        sell_limit_decimal = 0.2
        type = "long"
        fee = 1.0

        test_object = Position(entry_price, invest, leverage, stop_loss_decimal, sell_limit_decimal, fee, type)

        self.assertEqual(test_object.entry_price, entry_price)
        self.assertEqual(test_object.invest, invest)
        self.assertEqual(test_object.leverage, leverage)
        self.assertEqual(test_object.stop_loss_decimal, stop_loss_decimal)
        self.assertEqual(test_object.sell_limit_decimal, sell_limit_decimal)
        self.assertEqual(test_object.fee, fee)
        self.assertEqual(test_object.type, type)
        self.assertFalse(test_object.is_closed, False)
        self.assertEqual(test_object.balance, invest)

    def test_position_type_validation(self):
        with self.assertRaises(Exception) as context:
            Position(100, 50, 10, 0.1, 0.2, None, "invalid_type")
        
        self.assertTrue("Type must be 'short' or 'long'" in str(context.exception))

    def test_update_is_closed_for_not_set(self):
        test_object = Position(87.3, 49, 10, 1, 1, None, "short")
        test_object.update_is_closed()
        self.assertEqual(test_object.is_closed, False)

    def test_update_is_closed_for_liquidated_true(self):
        test_object = Position(87.3, 49, 10, 1, 1, None, "short")
        test_object.set_liquidated(True)
        test_object.update_is_closed()
        self.assertEqual(test_object.is_closed, True)

    def test_update_is_closed_for_liquidated_false(self):
        test_object = Position(87.3, 49, 10, 1, 1, None, "short")
        test_object.set_liquidated(False)
        test_object.update_is_closed()
        self.assertEqual(test_object.is_closed, False)

    def test_update_is_closed_for_sold_at_sell_limit_false(self):
        test_object = Position(87.3, 49, 10, 1, 1, None, "short")
        test_object.set_sold_at_sell_limit(False)
        test_object.update_is_closed()
        self.assertEqual(test_object.is_closed, False)

    def test_update_is_closed_for_sold_at_sell_limit_true(self):
        test_object = Position(87.3, 49, 10, 1, 1, None, "short")
        test_object.set_sold_at_sell_limit(True)
        test_object.update_is_closed()
        self.assertEqual(test_object.is_closed, True)

    def test_update_is_closed_for_stop_loss_triggered_false(self):
        test_object = Position(87.3, 49, 10, 1, 1, None, "short")
        test_object.set_stop_loss_triggered(False)
        test_object.update_is_closed()
        self.assertEqual(test_object.is_closed, False)

    def test_update_is_closed_for_stop_loss_triggered_true(self):
        test_object = Position(87.3, 49, 10, 1, 1, None, "short")
        test_object.set_stop_loss_triggered(True)
        test_object.update_is_closed()
        self.assertEqual(test_object.is_closed, True)
        
    def test_set_balance(self):
        test_object = Position(100, 50, 10, 0.1, 0.2, None, "long")
        new_balance = 60
        test_object.set_balance(new_balance)
        self.assertEqual(test_object.balance, new_balance)

    def test_get_balance_pc(self):
        test_object = Position(100, 50, 10, 0.1, 0.2, None, "long")
        test_object.set_balance(60)
        expected_balance_pc = 60 / 50
        self.assertEqual(test_object.get_balance_pc(), expected_balance_pc)

    def test_get_balance_amt(self):
        test_object = Position(100, 50, 10, 0.1, 0.2, None, "long")
        self.assertEqual(test_object.get_balance_amt(), test_object.balance)
