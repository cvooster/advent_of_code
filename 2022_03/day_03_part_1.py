"""This module sums the priorities of items that appear in two compartments."""

import pytest
import sys

EXAMPLE_FILENAME = "input_03_example.txt"
EXAMPLE_ANSWER = 157


def main():
    """Test example input, and then process the actual puzzle input."""
    test_outcome(EXAMPLE_ANSWER, EXAMPLE_FILENAME)
    filename = "input_03.txt"
    priority_sum = sum_priorities(filename)
    print(f"\nThe priorities of two-compartment items sum to {priority_sum}.")


def sum_priorities(filename):
    """Read rucksack contents from a file, and compute the priority sum."""
    with open(filename) as file_object:
        return sum(
            [assign_priority(get_item(line.rstrip())) for line in file_object]
        )


def get_item(rucksack):
    """Given a rucksack, get the item type that appears in two compartments."""
    if len(rucksack) % 2 != 0:
        sys.exit("There exists a rucksack with an odd number of items!")
    compartment1 = rucksack[: len(rucksack) // 2]
    compartment2 = rucksack[len(rucksack) // 2 :]

    duplicate_items = set(compartment1).intersection(set(compartment2))
    if len(duplicate_items) != 1:
        sys.exit(f"A rucksack exists with {len(duplicate_items)} shared items!")
    return duplicate_items.pop()


def assign_priority(item_type):
    """Convert an item type to a priority."""
    return ord(item_type) - 96 if item_type.islower() else ord(item_type) - 38


def test_outcome(expected, filename):
    """Given input for which an answer is expected, check obtained result."""
    actual = sum_priorities(filename)
    try:
        assert actual == expected
        print(f"Expected outcome for input {filename} confirmed.")
    except AssertionError:
        print(f"\nUnexpected outcome for input {filename}:")
        print(f"Answer {expected} expected, but {actual} obtained.")


if __name__ == "__main__":
    main()
