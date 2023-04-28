"""This module determines the number of pairs with sub/superset assignments."""

import re

EXAMPLE_FILENAME = "input_04_example.txt"
EXAMPLE_ANSWER = 2


def main():
    """Test example input, and then process the actual puzzle input."""
    test_outcome(EXAMPLE_ANSWER, EXAMPLE_FILENAME)
    filename = "input_04.txt"
    nr_supersets = count_supersets(filename)
    print(f"\nIn {nr_supersets} pairs, one range fully contains the other.")


def count_supersets(filename):
    """Create regex, read pair assignments, and count sub/superset pairs."""
    pair_regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    with open(filename) as file_object:
        nr_supersets = 0
        for line in file_object:
            nr_supersets += is_superset(*pair_regex.search(line).groups())
    return nr_supersets


def is_superset(lower_1, upper_1, lower_2, upper_2):
    """Check whether string range 1 is a sub- or superset of string range 2."""
    lower_1, upper_1 = int(lower_1), int(upper_1)
    lower_2, upper_2 = int(lower_2), int(upper_2)
    return (lower_1 >= lower_2 and upper_1 <= upper_2) or (
        lower_1 <= lower_2 and upper_1 >= upper_2
    )


def test_outcome(expected, filename):
    """Given input for which an answer is expected, check obtained result."""
    actual = count_supersets(filename)
    try:
        assert actual == expected
        print(f"Expected outcome for input {filename} confirmed.")
    except AssertionError:
        print(f"\nUnexpected outcome for input {filename}:")
        print(f"Answer {expected} expected, but {actual} obtained.")


if __name__ == "__main__":
    main()
