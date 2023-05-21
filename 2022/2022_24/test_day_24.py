import unittest
import day_24 as d24

FILENAME = "input_24.txt"
FILENAME_EXAMPLE = "input_24_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 24."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        nr_sink_visits = 1
        length_shortest = d24.compute_shortest(FILENAME_EXAMPLE, nr_sink_visits)
        self.assertEqual(length_shortest, 18)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        nr_sink_visits = 1
        length_shortest = d24.compute_shortest(FILENAME, nr_sink_visits)
        self.assertEqual(length_shortest, 281)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        nr_sink_visits = 2
        length_shortest = d24.compute_shortest(FILENAME_EXAMPLE, nr_sink_visits)
        self.assertEqual(length_shortest, 54)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        nr_sink_visits = 2
        length_shortest = d24.compute_shortest(FILENAME, nr_sink_visits)
        self.assertEqual(length_shortest, 807)


if __name__ == "__main__":
    unittest.main()
