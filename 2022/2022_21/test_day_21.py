import unittest
import day_21 as d21

FILENAME = "input_21.txt"
FILENAME_EXAMPLE = "input_21_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 21."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        root_number = d21.calculate_number(FILENAME_EXAMPLE)
        self.assertEqual(root_number, 152)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        root_number = d21.calculate_number(FILENAME)
        self.assertEqual(root_number, 21208142603224)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        humn_number = d21.calculate_number(FILENAME_EXAMPLE, override_humn=True)
        self.assertEqual(humn_number, 301)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        humn_number = d21.calculate_number(FILENAME, override_humn=True)
        self.assertEqual(humn_number, 3882224466191)


if __name__ == "__main__":
    unittest.main()
