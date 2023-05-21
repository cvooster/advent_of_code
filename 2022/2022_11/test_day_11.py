import unittest
import day_11 as d11

FILENAME = "input_11.txt"
FILENAME_EXAMPLE = "input_11_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 11."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        business_level = d11.calculate_business_level(
            FILENAME_EXAMPLE, nr_rounds=20, worry_management=1
        )
        self.assertEqual(business_level, 10605)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        business_level = d11.calculate_business_level(
            FILENAME, nr_rounds=20, worry_management=1
        )
        self.assertEqual(business_level, 54253)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        business_level = d11.calculate_business_level(
            FILENAME_EXAMPLE, nr_rounds=10_000, worry_management=2
        )
        self.assertEqual(business_level, 2713310158)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        business_level = d11.calculate_business_level(
            FILENAME, nr_rounds=10_000, worry_management=2
        )
        self.assertEqual(business_level, 13119526120)


if __name__ == "__main__":
    unittest.main()
