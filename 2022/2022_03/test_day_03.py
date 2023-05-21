import unittest
import day_03 as d03

FILENAME = "input_03.txt"
FILENAME_EXAMPLE = "input_03_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 3."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        priority_sum = d03.sum_two_type_priorities(FILENAME_EXAMPLE)
        self.assertEqual(priority_sum, 157)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        priority_sum = d03.sum_two_type_priorities(FILENAME)
        self.assertEqual(priority_sum, 8394)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        priority_sum = d03.sum_badge_type_priorities(FILENAME_EXAMPLE)
        self.assertEqual(priority_sum, 70)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        priority_sum = d03.sum_badge_type_priorities(FILENAME)
        self.assertEqual(priority_sum, 2413)


if __name__ == "__main__":
    unittest.main()
