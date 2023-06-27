import unittest
import day_16 as d16

FILENAME = "input_16.txt"
FILENAME_EXAMPLE = "input_16_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 16."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        max_pressure_release = d16.maximize_pressure_release(
            FILENAME_EXAMPLE, nr_minutes=30, nr_agents=1
        )
        self.assertEqual(max_pressure_release, 1651)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        max_pressure_release = d16.maximize_pressure_release(
            FILENAME, nr_minutes=30, nr_agents=1
        )
        self.assertEqual(max_pressure_release, 2059)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        max_pressure_release = d16.maximize_pressure_release(
            FILENAME_EXAMPLE, nr_minutes=26, nr_agents=2
        )
        self.assertEqual(max_pressure_release, 1707)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        max_pressure_release = d16.maximize_pressure_release(
            FILENAME, nr_minutes=26, nr_agents=2
        )
        self.assertEqual(max_pressure_release, 2790)


if __name__ == "__main__":
    unittest.main()
