import unittest
import day_04 as d04

FILENAME = "input_04.txt"
FILENAME_EXAMPLE = "input_04_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 4."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        nr_supersets = d04.count_supersets(FILENAME_EXAMPLE)
        self.assertEqual(nr_supersets, 2)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        nr_supersets = d04.count_supersets(FILENAME)
        self.assertEqual(nr_supersets, 534)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        nr_overlaps = d04.count_overlaps(FILENAME_EXAMPLE)
        self.assertEqual(nr_overlaps, 4)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        nr_overlaps = d04.count_overlaps(FILENAME)
        self.assertEqual(nr_overlaps, 841)


if __name__ == "__main__":
    unittest.main()
