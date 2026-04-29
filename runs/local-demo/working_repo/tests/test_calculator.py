import unittest

from src.calculator import add, divide


class CalculatorTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_divide(self):
        self.assertEqual(divide(10, 2), 5)


    def test_divide_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            divide(10, 0)


if __name__ == "__main__":
    unittest.main()
