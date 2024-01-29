import unittest
from position import Position

class TestPositionClass(unittest.TestCase):

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
        
