import unittest
import day_23 as d23

FILENAME = "input_23.txt"
FILENAMES_EXAMPLES = ("input_23_example_1.txt", "input_23_example_2.txt")


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 23."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the examples is as expected."""
        expected_answers = (25, 110)
        for filename, expected in zip(FILENAMES_EXAMPLES, expected_answers):
            empty_tiles, _ = d23.simulate_elves(filename, max_rounds=10)
            self.assertEqual(empty_tiles, expected)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        empty_tiles, _ = d23.simulate_elves(FILENAME, max_rounds=10)
        self.assertEqual(empty_tiles, 4218)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the examples is as expected."""
        expected_answers = (4, 20)
        for filename, expected in zip(FILENAMES_EXAMPLES, expected_answers):
            _, nr_rounds = d23.simulate_elves(filename)
            self.assertEqual(nr_rounds, expected)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        _, nr_rounds = d23.simulate_elves(FILENAME)
        self.assertEqual(nr_rounds, 976)


if __name__ == "__main__":
    unittest.main()
