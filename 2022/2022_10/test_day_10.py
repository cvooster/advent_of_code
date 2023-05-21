import unittest
import day_10 as d10

FILENAME = "input_10.txt"
SCREEN_OUTPUT = """
####.#..#.###..#..#.####.###..#..#.####.
#....#.#..#..#.#..#.#....#..#.#..#....#.
###..##...#..#.####.###..#..#.#..#...#..
#....#.#..###..#..#.#....###..#..#..#...
#....#.#..#.#..#..#.#....#....#..#.#....
####.#..#.#..#.#..#.####.#.....##..####.
"""
EXPECTED_PATTERN = "".join(SCREEN_OUTPUT.splitlines())

FILENAME_EXAMPLE = "input_10_example.txt"
SCREEN_OUTPUT_EXAMPLE = """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
"""
EXPECTED_PATTERN_EXAMPLE = "".join(SCREEN_OUTPUT_EXAMPLE.splitlines())


class TestSolution(unittest.TestCase):
    """Tests for the solution of day 10."""

    def test_example_part_1(self):
        """Test whether part 1 outcome for the example is as expected."""
        signal_strength_sum, _ = d10.simulate_crt(FILENAME_EXAMPLE)
        self.assertEqual(signal_strength_sum, 13140)

    def test_aoc_verified_part_1(self):
        """Test whether part 1 outcome is as verified by AoC."""
        signal_strength_sum, _ = d10.simulate_crt(FILENAME)
        self.assertEqual(signal_strength_sum, 14560)

    def test_example_part_2(self):
        """Test whether part 2 outcome for the example is as expected."""
        _, pixel_pattern = d10.simulate_crt(FILENAME_EXAMPLE)
        self.assertEqual(pixel_pattern, EXPECTED_PATTERN_EXAMPLE)

    def test_aoc_verified_part_2(self):
        """Test whether part 2 outcome is as verified by AoC."""
        _, pixel_pattern = d10.simulate_crt(FILENAME)
        self.assertEqual(pixel_pattern, EXPECTED_PATTERN)


if __name__ == "__main__":
    unittest.main()
