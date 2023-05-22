import unittest
import day_15 as d15

FILENAME = "input_15.txt"
FILENAME_EXAMPLE = "input_15_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 15."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        pos_y = 10
        nr_positions = d15.count_infeasible_positions(FILENAME_EXAMPLE, pos_y)
        self.assertEqual(nr_positions, 26)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        pos_y = 2_000_000
        nr_positions = d15.count_infeasible_positions(FILENAME, pos_y)
        self.assertEqual(nr_positions, 5525990)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        tuning_frequency = d15.calculate_tuning_frequency(
            FILENAME_EXAMPLE, range_x=(0, 20), range_y=(0, 20)
        )
        self.assertEqual(tuning_frequency, 56000011)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        tuning_frequency = d15.calculate_tuning_frequency(
            FILENAME, range_x=(0, 4_000_000), range_y=(0, 4_000_000)
        )
        self.assertEqual(tuning_frequency, 11756174628223)


if __name__ == "__main__":
    unittest.main()
