import contextlib
import io
import math
import unittest

from unitconv.__main__ import main
from unitconv.convert import UnknownUnit, convert


class ConvertTests(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(convert(100, "c", "f"), 212.0)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(convert(32, "f", "c"), 0.0)

    def test_celsius_to_rankine(self):
        self.assertAlmostEqual(convert(100, "c", "r"), 671.67)

    def test_rankine_to_celsius(self):
        self.assertAlmostEqual(convert(671.67, "r", "c"), 100.0)

    def test_fahrenheit_to_rankine(self):
        self.assertAlmostEqual(convert(32, "f", "r"), 491.67)

    def test_rankine_to_fahrenheit(self):
        self.assertAlmostEqual(convert(491.67, "r", "f"), 32.0)

    def test_fahrenheit_to_rankine_extreme_stays_finite(self):
        self.assertTrue(math.isfinite(convert(1e308, "f", "r")))

    def test_rankine_identity(self):
        self.assertEqual(convert(300, "r", "r"), 300)

    def test_km_to_mi(self):
        self.assertAlmostEqual(convert(5, "km", "mi"), 3.10686, places=4)

    def test_unknown_unit(self):
        with self.assertRaises(UnknownUnit):
            convert(1, "parsec", "m")

    def test_mixed_categories_rejected(self):
        with self.assertRaises(ValueError):
            convert(1, "c", "m")

    def test_cli_prints_two_decimal_places(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            status = main(["5", "km", "mi"])
        self.assertEqual(status, 0)
        self.assertEqual(buffer.getvalue(), "3.11\n")


if __name__ == "__main__":
    unittest.main()


if __name__ == "__main__":
    unittest.main()
