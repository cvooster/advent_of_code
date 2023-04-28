"""This module sums the priorities of the badge item types."""

import sys

EXAMPLE_FILENAME = "input_03_example.txt"
EXAMPLE_ANSWER = 70


def main():
    """Test example input, and then process the actual puzzle input."""
    test_outcome(EXAMPLE_ANSWER, EXAMPLE_FILENAME)
    filename = "input_03.txt"
    priority_sum = sum_priorities(filename)
    print(f"\nThe priorities of the badge item types sum to {priority_sum}.")


def sum_priorities(filename):
    """Read rucksack contents from a file, and compute the priority sum."""
    with open(filename) as file_object:
        rucksacks = [line.rstrip() for line in file_object]
    if len(rucksacks) % 3 != 0:
        sys.exit("The number of elves is not a multiple of three!")

    priority_sum = 0
    for i in range(0, len(rucksacks), 3):
        priority_sum += assign_priority(get_badge_type(rucksacks[i : i + 3]))
    return priority_sum


def get_badge_type(rucksack_group):
    """Given a rucksack group, get the item type that appears in all of them."""
    rucksack_sets = [set(rucksack) for rucksack in rucksack_group]
    common_items = set.intersection(*rucksack_sets)
    if len(common_items) != 1:
        sys.exit(f"There are {len(common_items)} common types in this group!")
    return common_items.pop()


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
