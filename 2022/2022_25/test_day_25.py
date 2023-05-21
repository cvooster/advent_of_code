import unittest
import day_25 as d25

FILENAME = "input_25.txt"
FILENAME_EXAMPLE = "input_25_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 25."""

    def test_example(self):
        """Test whether outcome for the example is as expected."""
        snafu_total = d25.compute_snafu_total(FILENAME_EXAMPLE)
        self.assertEqual(snafu_total, "2=-1=0")

    def test_aoc_verified(self):
        """Test whether outcome is as verified by AoC."""
        snafu_total = d25.compute_snafu_total(FILENAME)
        self.assertEqual(snafu_total, "2=01-0-2-0=-0==-1=01")


if __name__ == "__main__":
    unittest.main()
