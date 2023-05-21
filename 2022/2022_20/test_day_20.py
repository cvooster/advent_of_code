import unittest
import day_20 as d20

FILENAME = "input_20.txt"
FILENAME_EXAMPLE = "input_20_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 20."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        coordinate_sum = d20.sum_grove_coordinates(
            FILENAME_EXAMPLE, decryption_key=1, nr_mixes=1
        )
        self.assertEqual(coordinate_sum, 3)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        coordinate_sum = d20.sum_grove_coordinates(
            FILENAME, decryption_key=1, nr_mixes=1
        )
        self.assertEqual(coordinate_sum, 13183)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        coordinate_sum = d20.sum_grove_coordinates(
            FILENAME_EXAMPLE, decryption_key=811589153, nr_mixes=10
        )
        self.assertEqual(coordinate_sum, 1623178306)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        coordinate_sum = d20.sum_grove_coordinates(
            FILENAME, decryption_key=811589153, nr_mixes=10
        )
        self.assertEqual(coordinate_sum, 6676132372578)


if __name__ == "__main__":
    unittest.main()
