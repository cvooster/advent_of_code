"""This module sums the top-n total number of calories carried by the elves."""

import pytest
import sys

EXAMPLE_FILENAME = "input_01_example.txt"
EXAMPLE_ANSWER = 24000
PART_ONE_ANSWER = 71934


def main():
    """Test example input and part 1 answer, then solve part 2."""
    test_outcome(EXAMPLE_ANSWER, EXAMPLE_FILENAME, number_of_elves=1)
    filename = "input_01.txt"
    test_outcome(PART_ONE_ANSWER, filename, number_of_elves=1)
    top_totals_sum = sum_top_totals(filename, number_of_elves=3)
    print(f"\nThe sum of the top-three calorie totals is {top_totals_sum}.")


def sum_top_totals(filename, number_of_elves):
    """Read input from a file, and sum the {number_of_elves}-highest totals."""
    with open(filename) as file_object:
        calorie_lines = file_object.readlines()
    if not calorie_lines:
        sys.exit("The elves have provided an empty list!")
    calorie_lines.append("")  # Add empty string at end of last elf's items.

    sorted_totals = sorted(get_elf_totals(calorie_lines), reverse=True)
    if number_of_elves > len(sorted_totals):
        sys.exit(
            f"Top-{number_of_elves} asked, but there are"
            f"only {len(sorted_totals)} elves on the list."
        )
    return sum(sorted_totals[:number_of_elves])


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


def test_outcome(expected, filename, number_of_elves):
    """Given input for which an answer is expected, check obtained result."""
    actual = sum_top_totals(filename, number_of_elves)
    try:
        assert actual == expected
        print(f"Expected top-{number_of_elves} sum for {filename} confirmed.")
    except AssertionError:
        print(f"\nUnexpected top-{number_of_elves} sum for input {filename}:")
        print(f"Answer {expected} expected, but {actual} obtained.")


if __name__ == "__main__":
    main()
