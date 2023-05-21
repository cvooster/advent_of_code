import unittest
import day_05 as d05

FILENAME_INITIAL = "input_05a.txt"
FILENAME_MOVES = "input_05b.txt"
FILENAME_EXAMPLE_INITIAL = "input_05a_example.txt"
FILENAME_EXAMPLE_MOVES = "input_05b_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 5."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        top_crates = d05.get_final_top_crates(
            FILENAME_EXAMPLE_INITIAL, FILENAME_EXAMPLE_MOVES, mover_9001=False
        )
        self.assertEqual(top_crates, "CMZ")

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        top_crates = d05.get_final_top_crates(
            FILENAME_INITIAL, FILENAME_MOVES, mover_9001=False
        )
        self.assertEqual(top_crates, "MQSHJMWNH")

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        top_crates = d05.get_final_top_crates(
            FILENAME_EXAMPLE_INITIAL, FILENAME_EXAMPLE_MOVES, mover_9001=True
        )
        self.assertEqual(top_crates, "MCD")

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        top_crates = d05.get_final_top_crates(
            FILENAME_INITIAL, FILENAME_MOVES, mover_9001=True
        )
        self.assertEqual(top_crates, "LLWJRBHVZ")


if __name__ == "__main__":
    unittest.main()
