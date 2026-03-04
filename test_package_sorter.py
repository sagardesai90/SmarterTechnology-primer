"""
Tests for the package sorter function.
"""

import unittest
from package_sorter import sort


class TestStandardPackages(unittest.TestCase):
    """Packages that are neither bulky nor heavy."""

    def test_small_light_package(self):
        self.assertEqual(sort(10, 10, 10, 5), "STANDARD")

    def test_medium_package_below_thresholds(self):
        self.assertEqual(sort(99, 99, 99, 19), "STANDARD")  # Volume = 970,299

    def test_max_standard_volume(self):
        # Volume = 999,999, all dims < 150, mass < 20
        self.assertEqual(sort(99, 101, 100, 19), "STANDARD")

    def test_max_standard_dimension(self):
        # One dimension at 149 cm (just under 150)
        self.assertEqual(sort(149, 10, 10, 10), "STANDARD")

    def test_max_standard_mass(self):
        self.assertEqual(sort(10, 10, 10, 19.9), "STANDARD")

    def test_tiny_package(self):
        self.assertEqual(sort(1, 1, 1, 0.1), "STANDARD")

    def test_rectangular_below_thresholds(self):
        self.assertEqual(sort(50, 80, 120, 15), "STANDARD")  # vol=480,000

    def test_fractional_dimensions_and_mass(self):
        self.assertEqual(sort(10.5, 20.3, 30.7, 5.2), "STANDARD")

    def test_volume_just_under_one_million(self):
        # 100 * 100 * 99.99 = 999,900
        self.assertEqual(sort(100, 100, 99.99, 10), "STANDARD")

    def test_all_dimensions_near_limit(self):
        self.assertEqual(sort(149, 149, 44, 19), "STANDARD")  # vol=976,556


class TestSpecialPackages(unittest.TestCase):
    """Packages that are either bulky OR heavy (but not both)."""

    def test_bulky_only_by_volume(self):
        # Volume = 1,000,000 exactly
        self.assertEqual(sort(100, 100, 100, 10), "SPECIAL")

    def test_bulky_only_by_dimension(self):
        self.assertEqual(sort(150, 10, 10, 10), "SPECIAL")
        self.assertEqual(sort(10, 150, 10, 10), "SPECIAL")
        self.assertEqual(sort(10, 10, 150, 10), "SPECIAL")

    def test_heavy_only(self):
        self.assertEqual(sort(10, 10, 10, 20), "SPECIAL")
        self.assertEqual(sort(10, 10, 10, 25), "SPECIAL")

    def test_bulky_by_volume_heavy_mass_boundary(self):
        # Bulky (vol >= 1M) but mass = 19 (not heavy)
        self.assertEqual(sort(100, 100, 100, 19), "SPECIAL")

    def test_bulky_by_volume_non_cubic(self):
        # 200 * 100 * 50 = 1,000,000
        self.assertEqual(sort(200, 100, 50, 10), "SPECIAL")

    def test_bulky_by_single_large_dimension(self):
        self.assertEqual(sort(200, 5, 5, 5), "SPECIAL")

    def test_heavy_with_fractional_mass(self):
        self.assertEqual(sort(10, 10, 10, 20.0), "SPECIAL")
        self.assertEqual(sort(10, 10, 10, 19.999999), "STANDARD")  # still under 20

    def test_volume_just_over_one_million(self):
        self.assertEqual(sort(100, 100, 100.01, 10), "SPECIAL")

    def test_dimension_exactly_150_all_axes(self):
        self.assertEqual(sort(150, 150, 150, 1), "SPECIAL")


class TestRejectedPackages(unittest.TestCase):
    """Packages that are both bulky AND heavy."""

    def test_bulky_and_heavy_by_volume(self):
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")

    def test_bulky_and_heavy_by_dimension(self):
        self.assertEqual(sort(150, 10, 10, 20), "REJECTED")

    def test_both_thresholds_exactly(self):
        # Volume = 1,000,000, mass = 20
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")

    def test_large_heavy_package(self):
        self.assertEqual(sort(200, 200, 200, 50), "REJECTED")

    def test_bulky_by_dimension_heavy_mass(self):
        self.assertEqual(sort(151, 1, 1, 20), "REJECTED")

    def test_multiple_dimensions_over_150(self):
        self.assertEqual(sort(200, 200, 100, 25), "REJECTED")

    def test_volume_and_dimension_both_bulky(self):
        # Bulky by both volume and dimension
        self.assertEqual(sort(150, 100, 100, 30), "REJECTED")

    def test_mass_just_over_20(self):
        self.assertEqual(sort(100, 100, 100, 20.01), "REJECTED")


class TestEdgeCases(unittest.TestCase):
    """Boundary conditions and edge cases."""

    def test_exact_volume_threshold(self):
        # 100 * 100 * 100 = 1,000,000
        self.assertEqual(sort(100, 100, 100, 19), "SPECIAL")
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")

    def test_exact_dimension_threshold(self):
        self.assertEqual(sort(150, 1, 1, 19), "SPECIAL")
        self.assertEqual(sort(150, 1, 1, 20), "REJECTED")

    def test_exact_mass_threshold(self):
        self.assertEqual(sort(10, 10, 10, 20), "SPECIAL")  # heavy only
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")  # both

    def test_zero_dimensions(self):
        # Volume would be 0 - not bulky by volume, no dim >= 150
        self.assertEqual(sort(0, 10, 10, 5), "STANDARD")

    def test_zero_mass(self):
        self.assertEqual(sort(10, 10, 10, 0), "STANDARD")

    def test_mass_exactly_20(self):
        self.assertEqual(sort(10, 10, 10, 20), "SPECIAL")
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")

    def test_dimension_exactly_150(self):
        self.assertEqual(sort(150, 1, 1, 19), "SPECIAL")
        self.assertEqual(sort(150, 1, 1, 20), "REJECTED")

    def test_volume_exactly_one_million(self):
        self.assertEqual(sort(100, 100, 100, 19), "SPECIAL")
        self.assertEqual(sort(100, 100, 100, 20), "REJECTED")

    def test_very_large_numbers(self):
        self.assertEqual(sort(1000, 1000, 1000, 100), "REJECTED")

    def test_floating_point_mass_boundary(self):
        self.assertEqual(sort(10, 10, 10, 19.9999999), "STANDARD")


if __name__ == "__main__":
    unittest.main()
