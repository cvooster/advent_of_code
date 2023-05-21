import unittest
import day_06 as d06

FILENAME = "input_06.txt"
FILENAMES_EXAMPLES = (
    "input_06_example_1.txt",
    "input_06_example_2.txt",
    "input_06_example_3.txt",
    "input_06_example_4.txt",
    "input_06_example_5.txt",
)


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 6."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the examples is as expected."""
        pattern_length = 4
        expected_answers = (7, 5, 6, 10, 11)
        for filename, expected in zip(FILENAMES_EXAMPLES, expected_answers):
            nr_characters = d06.get_first_start_marker(filename, pattern_length)
            self.assertEqual(nr_characters, expected)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        pattern_length = 4
        nr_characters = d06.get_first_start_marker(FILENAME, pattern_length)
        self.assertEqual(nr_characters, 1623)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the examples is as expected."""
        pattern_length = 14
        expected_answers = (19, 23, 23, 29, 26)
        for filename, expected in zip(FILENAMES_EXAMPLES, expected_answers):
            nr_characters = d06.get_first_start_marker(filename, pattern_length)
            self.assertEqual(nr_characters, expected)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        pattern_length = 14
        nr_characters = d06.get_first_start_marker(FILENAME, pattern_length)
        self.assertEqual(nr_characters, 3774)


if __name__ == "__main__":
    unittest.main()
