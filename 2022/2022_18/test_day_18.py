import unittest
import day_18 as d18

FILENAME = "input_18.txt"
FILENAME_EXAMPLE = "input_18_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 18."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        droplet_surface = d18.calculate_surface(FILENAME_EXAMPLE, outer=False)
        self.assertEqual(droplet_surface, 64)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        droplet_surface = d18.calculate_surface(FILENAME, outer=False)
        self.assertEqual(droplet_surface, 3364)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        droplet_surface = d18.calculate_surface(FILENAME_EXAMPLE, outer=True)
        self.assertEqual(droplet_surface, 58)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        droplet_surface = d18.calculate_surface(FILENAME, outer=True)
        self.assertEqual(droplet_surface, 2006)


if __name__ == "__main__":
    unittest.main()
