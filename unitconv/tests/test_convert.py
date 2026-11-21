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

    def test_rounding_mode_half_up(self):
        self.assertEqual(convert(2.5, "m", "m", rounded=True, digits=0), 3.0)
        self.assertEqual(convert(-2.5, "m", "m", rounded=True, digits=0), -3.0)

    def test_rounded_default_precision(self):
        self.assertEqual(convert(5, "km", "mi", rounded=True), 3.11)
        self.assertEqual(convert(36.6, "c", "f", rounded=True), 97.88)

    def test_rounded_explicit_precision(self):
        self.assertEqual(convert(5, "km", "mi", rounded=True, digits=4), 3.1069)

    def test_rounded_decimal_midpoint(self):
        self.assertEqual(convert(2.675, "m", "m", rounded=True), 2.68)

    def test_rounded_extreme_magnitude(self):
        self.assertEqual(convert(1e30, "m", "m", rounded=True), 1e30)
        self.assertEqual(
            convert(1, "km", "mi", rounded=True, digits=300), 0.62137119223733397
        )

    def test_no_rounding_by_default(self):
        self.assertEqual(convert(5, "km", "mi"), 3.1068559611866697)
        self.assertEqual(convert(2.5, "m", "m"), 2.5)


if __name__ == "__main__":
    unittest.main()
