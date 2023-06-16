import unittest
import day_19 as d19

FILENAME = "input_19.txt"
FILENAME_EXAMPLE = "input_19_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 19."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        _, quality_level_sum = d19.summarize_evaluations(
            FILENAME_EXAMPLE, nr_minutes=24
        )
        self.assertEqual(quality_level_sum, 33)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        _, quality_level_sum = d19.summarize_evaluations(FILENAME, nr_minutes=24)
        self.assertEqual(quality_level_sum, 2193)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        max_geode_multiple, _ = d19.summarize_evaluations(
            FILENAME_EXAMPLE, nr_minutes=32, max_blueprints=3
        )
        self.assertEqual(max_geode_multiple, 56 * 62)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        max_geode_multiple, _ = d19.summarize_evaluations(
            FILENAME, nr_minutes=32, max_blueprints=3
        )
        self.assertEqual(max_geode_multiple, 7200)


if __name__ == "__main__":
    unittest.main()
