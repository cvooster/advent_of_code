import unittest
import day_08 as d08

FILENAME = "input_08.txt"
FILENAME_EXAMPLE = "input_08_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 8."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        nr_visible, _ = d08.calculate_tree_house_metrics(FILENAME_EXAMPLE)
        self.assertEqual(nr_visible, 21)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        nr_visible, _ = d08.calculate_tree_house_metrics(FILENAME)
        self.assertEqual(nr_visible, 1684)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        _, scenic_score = d08.calculate_tree_house_metrics(FILENAME_EXAMPLE)
        self.assertEqual(scenic_score, 8)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        _, scenic_score = d08.calculate_tree_house_metrics(FILENAME)
        self.assertEqual(scenic_score, 486540)


if __name__ == "__main__":
    unittest.main()
