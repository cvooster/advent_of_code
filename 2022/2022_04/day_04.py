"""Solution --- Day 4: Camp Cleanup ---"""

import re

import aoc_tools as aoc


def main():
    filename = "input_04.txt"
    nr_supersets = count_supersets(filename)
    print(f"In {nr_supersets} pairs, one range fully contains the other.")
    nr_overlaps = count_overlaps(filename)
    print(f"In {nr_overlaps} pairs, the ranges overlap.")


def count_supersets(filename):
    """Count the number of pairs where one range fully contains the other."""
    pair_regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    pair_lines = aoc.read_stripped_lines(filename)
    nr_supersets = 0
    for line in pair_lines:
        range_endpoints = (int(x) for x in pair_regex.search(line).groups())
        nr_supersets += is_superset(*range_endpoints)
    return nr_supersets


def is_superset(lower_1, upper_1, lower_2, upper_2):
    """Check whether range 1 is a sub- or superset of range 2."""
    return (lower_1 >= lower_2 and upper_1 <= upper_2) or (
        lower_1 <= lower_2 and upper_1 >= upper_2
    )


def count_overlaps(filename):
    """Count the number of pairs whose ranges overlap."""
    pair_regex = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    pair_lines = aoc.read_stripped_lines(filename)
    nr_overlaps = 0
    for line in pair_lines:
        range_endpoints = (int(x) for x in pair_regex.search(line).groups())
        nr_overlaps += has_overlap(*range_endpoints)
    return nr_overlaps


def has_overlap(lower_1, upper_1, lower_2, upper_2):
    """Check whether range 1 has an overlap with range 2."""
    return not (lower_1 > upper_2 or upper_1 < lower_2)


if __name__ == "__main__":
    main()
