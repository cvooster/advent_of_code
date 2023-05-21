import unittest
import day_17 as d17

FILENAME = "input_17.txt"
FILENAME_EXAMPLE = "input_17_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 17."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        nr_rocks = 2022
        tower_height = d17.simulate_falling_rocks(FILENAME_EXAMPLE, nr_rocks)
        self.assertEqual(tower_height, 3068)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        nr_rocks = 2022
        tower_height = d17.simulate_falling_rocks(FILENAME, nr_rocks)
        self.assertEqual(tower_height, 3177)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        nr_rocks = 1_000_000_000_000
        tower_height = d17.simulate_falling_rocks(FILENAME_EXAMPLE, nr_rocks)
        self.assertEqual(tower_height, 1514285714288)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        nr_rocks = 1_000_000_000_000
        tower_height = d17.simulate_falling_rocks(FILENAME, nr_rocks)
        self.assertEqual(tower_height, 1565517241382)


if __name__ == "__main__":
    unittest.main()
