import unittest
import day_14 as d14

FILENAME = "input_14.txt"
FILENAME_EXAMPLE = "input_14_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 14."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        rest_units = d14.compute_rest_units(FILENAME_EXAMPLE, has_floor=False)
        self.assertEqual(rest_units, 24)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        rest_units = d14.compute_rest_units(FILENAME, has_floor=False)
        self.assertEqual(rest_units, 799)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        rest_units = d14.compute_rest_units(FILENAME_EXAMPLE, has_floor=True)
        self.assertEqual(rest_units, 93)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        rest_units = d14.compute_rest_units(FILENAME, has_floor=True)
        self.assertEqual(rest_units, 29076)


if __name__ == "__main__":
    unittest.main()
