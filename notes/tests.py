import unittest
from pair import fac


class TestJ(unittest.TestCase):

    def test_fraction_int(self):
        result = (5/2)
        self.assertEqual(result, 2)

    def test_fraction_float(self):
        with self.assertRaises(AssertionError):
            fac(5/2.0)

    def test_two(self):
        result = fac(2)
        self.assertEqual(result, 2)

    def test_4(self):
        result = fac(4)
        self.assertEqual(result, 24)

    def test_fails_on_three_args(self):
        with self.assertRaises(TypeError):
            fac(1, 2, 3)

    def test_w_string(self):
        with self.assertRaises(TypeError):
            fac('1')

    def test_0(self):
        result = fac(0)
        self.assertEqual(result, 1)

    def test_neg(self):
        with self.assertRaises(AssertionError):
            fac(-1)

if __name__ == '__main__':
    unittest.main()