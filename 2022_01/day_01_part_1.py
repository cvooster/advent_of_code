"""This module finds the maximum total number of calories carried by an elf."""

import pytest
import sys

EXAMPLE_FILENAME = "input_01_example.txt"
EXAMPLE_ANSWER = 24000


def main():
    """Test example input, and then process the actual puzzle input."""
    test_outcome(EXAMPLE_ANSWER, EXAMPLE_FILENAME)
    filename = "input_01.txt"
    max_total = get_max_total(filename)
    print(f"\nThe maximum calorie total carried by an elf is {max_total}.")


def get_max_total(filename):
    """Read input from a file, and compute the maximum total."""
    with open(filename) as file_object:
        calorie_lines = file_object.readlines()
    if not calorie_lines:
        sys.exit("The elves have provided an empty list!")
    calorie_lines.append("")  # Add empty string at end of last elf's items.

    return max(get_elf_totals(calorie_lines))


def get_elf_totals(calorie_lines):
    """Determine the calorie totals of all elves."""
    all_totals, calorie_list = [], []
    for calorie_line in calorie_lines:
        if calorie_line.rstrip():
            calorie_list.append(int(calorie_line.rstrip()))
        else:
            all_totals.append(sum(calorie_list))
            calorie_list = []
    return all_totals


def test_outcome(expected, filename):
    """Given input for which an answer is expected, check obtained result."""
    actual = get_max_total(filename)
    try:
        assert actual == expected
        print(f"Expected outcome for input {filename} confirmed.")
    except AssertionError:
        print(f"\nUnexpected outcome for input {filename}:")
        print(f"Answer {expected} expected, but {actual} obtained.")


if __name__ == "__main__":
    main()
