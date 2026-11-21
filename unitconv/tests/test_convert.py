import unittest

from unitconv.convert import UnknownUnit, convert


class RoundingTests(unittest.TestCase):
    def test_round_half_up_mode(self):
        # 2.125 is exact in binary; half-up gives 2.13 while banker's
        # rounding (built-in round) would give 2.12.
        self.assertEqual(convert(2.125, "m", "m", round_result=True), 2.13)

    def test_default_precision(self):
        self.assertEqual(convert(5, "km", "mi", round_result=True), 3.11)

    def test_explicit_precision(self):
        self.assertEqual(
            convert(5, "km", "mi", round_result=True, round_digits=3), 3.107
        )

    def test_call_without_option_unchanged(self):
        self.assertEqual(convert(5, "km", "mi"), 3.1068559611866697)
        self.assertEqual(convert(2.125, "m", "m"), 2.125)
        # The option can also be passed explicitly as False.
        self.assertEqual(
            convert(5, "km", "mi", round_result=False), 3.1068559611866697
        )

    def test_rounding_applies_to_temperature(self):
        self.assertEqual(convert(35.825, "f", "c", round_result=True), 2.13)

    def test_rounding_large_value(self):
        self.assertEqual(convert(1e26, "m", "m", round_result=True), 1e26)

    def test_rounding_many_digits(self):
        self.assertEqual(
            convert(2.125, "m", "m", round_result=True, round_digits=10), 2.125
        )

    def test_error_unchanged_with_rounding(self):
        with self.assertRaises(ValueError):
            convert(1, "c", "m", round_result=True)
        with self.assertRaises(UnknownUnit):
            convert(1, "parsec", "m", round_result=True)


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


if __name__ == "__main__":
    unittest.main()
