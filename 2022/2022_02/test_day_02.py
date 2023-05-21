import unittest
import day_02 as d02

FILENAME = "input_02.txt"
FILENAME_EXAMPLE = "input_02_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 2."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        total_score = d02.evaluate_strategy_guide(FILENAME_EXAMPLE, part=1)
        self.assertEqual(total_score, 15)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        total_score = d02.evaluate_strategy_guide(FILENAME, part=1)
        self.assertEqual(total_score, 13009)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        total_score = d02.evaluate_strategy_guide(FILENAME_EXAMPLE, part=2)
        self.assertEqual(total_score, 12)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        total_score = d02.evaluate_strategy_guide(FILENAME, part=2)
        self.assertEqual(total_score, 10398)


if __name__ == "__main__":
    unittest.main()
