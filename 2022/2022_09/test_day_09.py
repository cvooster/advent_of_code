import unittest
import day_09 as d09

FILENAME = "input_09.txt"
FILENAMES_EXAMPLES = ("input_09_example_1.txt", "input_09_example_2.txt")


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 9."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the first example is as expected."""
        filename = FILENAMES_EXAMPLES[0]
        nr_visited = d09.count_visited_positions(filename, nr_knots=2)
        self.assertEqual(nr_visited, 13)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        nr_visited = d09.count_visited_positions(FILENAME, nr_knots=2)
        self.assertEqual(nr_visited, 6087)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the examples is as expected."""
        expected_answers = (1, 36)
        for filename, expected in zip(FILENAMES_EXAMPLES, expected_answers):
            nr_visited = d09.count_visited_positions(filename, nr_knots=10)
            self.assertEqual(nr_visited, expected)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        nr_visited = d09.count_visited_positions(FILENAME, nr_knots=10)
        self.assertEqual(nr_visited, 2493)


if __name__ == "__main__":
    unittest.main()
