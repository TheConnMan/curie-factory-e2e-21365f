import io
import unittest
from contextlib import redirect_stdout

from unitconv.__main__ import main
from unitconv.convert import UnknownUnit, convert


class ConvertTests(unittest.TestCase):
    def test_celsius_to_fahrenheit(self):
        self.assertAlmostEqual(convert(100, "c", "f"), 212.0, places=6)

    def test_fahrenheit_to_celsius(self):
        self.assertAlmostEqual(convert(32, "f", "c"), 0.0, places=6)

    def test_km_to_mi(self):
        self.assertAlmostEqual(convert(5, "km", "mi"), 3.106856, places=6)

    def test_unknown_unit(self):
        with self.assertRaises(UnknownUnit):
            convert(1, "parsec", "m")

    def test_mixed_categories_rejected(self):
        with self.assertRaises(ValueError):
            convert(1, "c", "m")

    def test_celsius_to_rankine(self):
        self.assertAlmostEqual(convert(100, "c", "r"), 671.67, places=6)

    def test_rankine_to_celsius(self):
        self.assertAlmostEqual(convert(671.67, "r", "c"), 100.0, places=6)

    def test_fahrenheit_to_rankine(self):
        self.assertAlmostEqual(convert(32, "f", "r"), 491.67, places=6)

    def test_rankine_to_fahrenheit(self):
        self.assertAlmostEqual(convert(491.67, "r", "f"), 32.0, places=6)

    def test_rankine_identity(self):
        self.assertAlmostEqual(convert(45.6, "r", "r"), 45.6, places=6)

    def test_celsius_to_delisle(self):
        self.assertAlmostEqual(convert(38.6, "c", "de"), 92.1, places=6)

    def test_delisle_to_celsius(self):
        self.assertAlmostEqual(convert(92.1, "de", "c"), 38.6, places=6)

    def test_delisle_identity(self):
        self.assertAlmostEqual(convert(45.6, "de", "de"), 45.6, places=6)

    def test_delisle_celsius_round_trip(self):
        delisle = convert(38.6, "c", "de")
        self.assertAlmostEqual(delisle, 92.1, places=6)
        self.assertAlmostEqual(convert(delisle, "de", "c"), 38.6, places=6)

    def test_fahrenheit_delisle(self):
        self.assertAlmostEqual(convert(32, "f", "de"), 150.0, places=6)
        self.assertAlmostEqual(convert(150.0, "de", "f"), 32.0, places=6)

    def test_rankine_delisle(self):
        self.assertAlmostEqual(convert(491.67, "r", "de"), 150.0, places=6)
        self.assertAlmostEqual(convert(150.0, "de", "r"), 491.67, places=6)

    def test_cli_prints_delisle_two_decimals(self):
        captured = io.StringIO()
        with redirect_stdout(captured):
            code = main(["38.6", "c", "de"])
        self.assertEqual(code, 0)
        self.assertEqual(captured.getvalue(), "92.10\n")

    def test_cli_prints_two_decimal_places(self):
        captured = io.StringIO()
        with redirect_stdout(captured):
            code = main(["100", "c", "r"])
        self.assertEqual(code, 0)
        self.assertEqual(captured.getvalue(), "671.67\n")


if __name__ == "__main__":
    unittest.main()
