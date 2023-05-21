import unittest
import day_12 as d12

FILENAME = "input_12.txt"
FILENAME_EXAMPLE = "input_12_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 12."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        fix_source = True
        shortest_length = d12.compute_shortest(FILENAME_EXAMPLE, fix_source)
        self.assertEqual(shortest_length, 31)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        fix_source = True
        length_shortest = d12.compute_shortest(FILENAME, fix_source)
        self.assertEqual(length_shortest, 380)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        fix_source = False
        length_shortest = d12.compute_shortest(FILENAME_EXAMPLE, fix_source)
        self.assertEqual(length_shortest, 29)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        fix_source = False
        length_shortest = d12.compute_shortest(FILENAME, fix_source)
        self.assertEqual(length_shortest, 375)


if __name__ == "__main__":
    unittest.main()
