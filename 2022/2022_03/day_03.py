"""Solution --- Day 3: Rucksack Reorganization ---"""

import aoc_tools as aoc

GROUP_SIZE = 3


def main():
    filename = "input_03.txt"
    priority_sum = sum_two_type_priorities(filename)
    print(f"The priorities of two-compartment items sum to {priority_sum}.")
    priority_sum = sum_badge_type_priorities(filename)
    print(f"The priorities of the badge item types sum to {priority_sum}.")


def sum_two_type_priorities(filename):
    """Sum the priorities of items that appear in two compartments."""
    rucksacks = aoc.read_stripped_lines(filename)
    return sum(assign_priority(get_item(rucksack)) for rucksack in rucksacks)


def get_item(rucksack):
    """For a given rucksack, get the type of the two-compartment item."""
    if len(rucksack) % 2 != 0:
        raise ValueError("Rucksack contains an odd number of items!")
    compartment_1 = rucksack[: len(rucksack) // 2]
    compartment_2 = rucksack[len(rucksack) // 2 :]
    duplicate_items = set.intersection(set(compartment_1), set(compartment_2))
    if len(duplicate_items) != 1:
        raise ValueError(f"Rucksack has {len(duplicate_items)} shared items!")
    return duplicate_items.pop()


def sum_badge_type_priorities(filename):
    """Sum the priorities of the badge item types."""
    rucksacks = aoc.read_stripped_lines(filename)
    if len(rucksacks) % GROUP_SIZE != 0:
        raise ValueError(f"Number of rucksacks not a multiple of {GROUP_SIZE}!")
    priority_sum = 0
    for i in range(0, len(rucksacks), GROUP_SIZE):
        priority_sum += assign_priority(
            get_badge(rucksacks[i : i + GROUP_SIZE])
        )
    return priority_sum


def get_badge(rucksack_group):
    """Get the item type that appears in all rucksacks in a given group."""
    rucksack_sets = [set(rucksack) for rucksack in rucksack_group]
    common_items = set.intersection(*rucksack_sets)
    if len(common_items) != 1:
        raise ValueError(f"Group has {len(common_items)} item types in common!")
    return common_items.pop()


def assign_priority(item_type):
    """Convert an item type to a priority."""
    return ord(item_type) - 96 if item_type.islower() else ord(item_type) - 38


if __name__ == "__main__":
    main()
