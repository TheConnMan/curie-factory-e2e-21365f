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

    def test_rounded_half_up_mode(self):
        # Half away from zero: 2.675 -> 2.68, 0.125 -> 0.13.
        # Python's round() gives 2.67 and 0.12, so this pins the mode.
        self.assertEqual(convert(2.675, "m", "m", rounded=True), 2.68)
        self.assertEqual(convert(0.125, "ft", "ft", rounded=True), 0.13)

    def test_rounded_temperature_identity(self):
        # Identity conversions round like every other family.
        self.assertEqual(convert(2.675, "c", "c", rounded=True), 2.68)

    def test_rounded_default_precision(self):
        # Default precision is 2 decimal places when none is named.
        self.assertEqual(convert(1, "km", "mi", rounded=True), 0.62)
        self.assertEqual(convert(98, "f", "c", rounded=True), 36.67)

    def test_rounded_explicit_precision(self):
        self.assertEqual(convert(1, "km", "mi", rounded=True, precision=4), 0.6214)
        self.assertEqual(convert(98, "f", "c", rounded=True, precision=0), 37.0)

    def test_no_rounding_option_returns_raw(self):
        # Without the option the raw float comes back untouched.
        self.assertEqual(convert(2.675, "m", "m"), 2.675)
        self.assertEqual(convert(5, "km", "mi"), 5 * 1000 / 1609.344)

    def test_no_rounding_temperature_identity(self):
        self.assertEqual(convert(2.675, "c", "c"), 2.675)

    def test_rounded_large_value_and_precision(self):
        # Magnitudes and precisions beyond the default 28-digit decimal
        # context still round instead of raising InvalidOperation.
        self.assertEqual(convert(1e26, "m", "m", rounded=True), 1e26)
        self.assertEqual(convert(1.0, "c", "c", rounded=True, precision=30), 1.0)

    def test_rounded_errors_preserved(self):
        with self.assertRaises(UnknownUnit):
            convert(1, "parsec", "m", rounded=True)
        with self.assertRaises(ValueError):
            convert(1, "c", "m", rounded=True)


if __name__ == "__main__":
    unittest.main()
