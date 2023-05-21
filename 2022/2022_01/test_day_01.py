import unittest
import day_01 as d01

FILENAME = "input_01.txt"
FILENAME_EXAMPLE = "input_01_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 1."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        max_total = d01.sum_top_totals(FILENAME_EXAMPLE, cut_off_rank=1)
        self.assertEqual(max_total, 24000)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        max_total = d01.sum_top_totals(FILENAME, cut_off_rank=1)
        self.assertEqual(max_total, 71934)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        top_totals_sum = d01.sum_top_totals(FILENAME_EXAMPLE, cut_off_rank=3)
        self.assertEqual(top_totals_sum, 45000)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        top_totals_sum = d01.sum_top_totals(FILENAME, cut_off_rank=3)
        self.assertEqual(top_totals_sum, 211447)


if __name__ == "__main__":
    unittest.main()
