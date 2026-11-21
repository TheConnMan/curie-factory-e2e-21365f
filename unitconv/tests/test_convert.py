import unittest

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

    def test_no_rounding_by_default(self):
        self.assertEqual(convert(5, "km", "mi"), 5000 / 1609.344)
        self.assertEqual(convert(37, "c", "f"), 37 * 9 / 5 + 32)
        self.assertEqual(convert(0.125, "m", "m"), 0.125)

    def test_rounding_mode_half_to_even(self):
        self.assertEqual(convert(0.125, "m", "m", rounding=2), 0.12)
        self.assertEqual(convert(0.375, "m", "m", rounding=2), 0.38)

    def test_default_precision(self):
        self.assertEqual(convert(5, "km", "mi", rounding=True), 3.11)
        self.assertEqual(convert(37, "c", "f", rounding=True), 98.6)

    def test_explicit_precision(self):
        self.assertEqual(convert(5, "km", "mi", rounding=4), 3.1069)
        self.assertEqual(convert(5, "km", "mi", rounding=0), 3.0)

    def test_rounding_applies_to_temperature_and_identity(self):
        self.assertEqual(convert(100, "f", "c", rounding=1), 37.8)
        self.assertEqual(convert(100, "c", "c", rounding=2), 100.0)


if __name__ == "__main__":
    unittest.main()
