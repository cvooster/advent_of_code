import unittest
import day_13 as d13

FILENAME = "input_13.txt"
FILENAME_EXAMPLE = "input_13_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 13."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        indices_sum = d13.sum_indices(FILENAME_EXAMPLE)
        self.assertEqual(indices_sum, 13)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        indices_sum = d13.sum_indices(FILENAME)
        self.assertEqual(indices_sum, 5938)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        decoder_key = d13.compute_decoder_key(FILENAME_EXAMPLE)
        self.assertEqual(decoder_key, 140)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        decoder_key = d13.compute_decoder_key(FILENAME)
        self.assertEqual(decoder_key, 29025)


if __name__ == "__main__":
    unittest.main()
