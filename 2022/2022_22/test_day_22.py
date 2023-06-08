import unittest
import day_22 as d22

FILENAME_MAP = "input_22a.txt"
FILENAME_PATH = "input_22b.txt"
FILENAME_EXAMPLE_MAP = "input_22a_example.txt"
FILENAME_EXAMPLE_PATH = "input_22b_example.txt"


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 22."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        password = d22.compute_password(
            FILENAME_EXAMPLE_MAP, FILENAME_EXAMPLE_PATH, part=1
        )
        self.assertEqual(password, 6032)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        password = d22.compute_password(FILENAME_MAP, FILENAME_PATH, part=1)
        self.assertEqual(password, 66292)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        password = d22.compute_password(
            FILENAME_EXAMPLE_MAP, FILENAME_EXAMPLE_PATH, part=2
        )
        self.assertEqual(password, 5031)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        password = d22.compute_password(FILENAME_MAP, FILENAME_PATH, part=2)
        self.assertEqual(password, 127012)


if __name__ == "__main__":
    unittest.main()
