import unittest
from short import Short

class TestMyClass(unittest.TestCase):
    def test_short_update_balance_profit(self):
        test_object = Short(87.3, 49, 10, 1, 1, None, "short")
        test_object.update_balance(78.4)
        self.assertEqual(round(test_object.get_balance_amt(), 2), 98.95)
        
    def test_short_update_balance_loss(self):
        test_object = Short(87.3, 49, 10, 1, 1, None, "short")
        test_object.update_balance(90.12)
        self.assertEqual(round(test_object.get_balance_amt(), 2), 33.17)
