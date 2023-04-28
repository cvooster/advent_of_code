"""This module determines the number of pairs with overlapping assignments."""

import pytest
import re

EXAMPLE_FILENAME = "input_04_example.txt"
EXAMPLE_ANSWER = 4


def main():
    """Test example input, and then process the actual puzzle input."""
    test_outcome(EXAMPLE_ANSWER, EXAMPLE_FILENAME)
    filename = "input_04.txt"
    nr_overlaps = count_overlaps(filename)
    print(f"\nIn {nr_overlaps} pairs, the ranges overlap.")


def count_overlaps(filename):
    """Create regex, read pair assignments, and count sub/superset pairs."""
    pair_regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    with open(filename) as file_object:
        nr_overlaps = 0
        for line in file_object:
            nr_overlaps += has_overlap(*pair_regex.search(line).groups())
    return nr_overlaps


def has_overlap(lower_1, upper_1, lower_2, upper_2):
    """Check whether string range 1 has an overlap with string range 2."""
    lower_1, upper_1 = int(lower_1), int(upper_1)
    lower_2, upper_2 = int(lower_2), int(upper_2)
    return not (lower_1 > upper_2 or upper_1 < lower_2)


def test_outcome(expected, filename):
    """Given input for which an answer is expected, check obtained result."""
    actual = count_overlaps(filename)
    try:
        assert actual == expected
        print(f"Expected outcome for input {filename} confirmed.")
    except AssertionError:
        print(f"\nUnexpected outcome for input {filename}:")
        print(f"Answer {expected} expected, but {actual} obtained.")


if __name__ == "__main__":
    main()
