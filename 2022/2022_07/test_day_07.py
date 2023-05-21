import unittest
import day_07 as d07

FILENAME = "input_07.txt"
FILENAME_EXAMPLE = "input_07_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 7."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        size_sum = d07.sum_small_directory_sizes(FILENAME_EXAMPLE)
        self.assertEqual(size_sum, 95437)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        size_sum = d07.sum_small_directory_sizes(FILENAME)
        self.assertEqual(size_sum, 1453349)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        del_size = d07.get_size_delete_directory(FILENAME_EXAMPLE)
        self.assertEqual(del_size, 24933642)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        del_size = d07.get_size_delete_directory(FILENAME)
        self.assertEqual(del_size, 2948823)


if __name__ == "__main__":
    unittest.main()
