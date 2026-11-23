import io
import unittest
from contextlib import redirect_stdout

from unitconv.__main__ import main
from unitconv.convert import UnknownUnit, convert


class ConvertTests(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(convert(100, "c", "f"), 212.0)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(convert(32, "f", "c"), 0.0)

    def test_km_to_mi(self):
        self.assertAlmostEqual(convert(5, "km", "mi"), 3.10686, places=4)

    def test_unknown_unit(self):
        with self.assertRaises(UnknownUnit):
            convert(1, "parsec", "m")

    def test_mixed_categories_rejected(self):
        with self.assertRaises(ValueError):
            convert(1, "c", "m")

    def test_celsius_to_rankine(self):
        self.assertEqual(convert(100, "c", "r"), 671.67)

    def test_rankine_to_celsius(self):
        self.assertEqual(convert(671.67, "r", "c"), 100.0)

    def test_fahrenheit_to_rankine(self):
        self.assertEqual(convert(32, "f", "r"), 491.67)

    def test_rankine_to_fahrenheit(self):
        self.assertEqual(convert(491.67, "r", "f"), 32.0)

    def test_rankine_identity(self):
        self.assertEqual(convert(45.6, "r", "r"), 45.6)

    def test_cli_prints_two_decimal_places(self):
        captured = io.StringIO()
        with redirect_stdout(captured):
            code = main(["100", "c", "r"])
        self.assertEqual(code, 0)
        self.assertEqual(captured.getvalue(), "671.67\n")


if __name__ == "__main__":
    unittest.main()
