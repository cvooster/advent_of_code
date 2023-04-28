"""This module identifies the top crates after the rearrangement."""

import sys
import re

EXAMPLE_FILENAME_INITIAL = "input_05a_example.txt"
EXAMPLE_FILENAME_MOVES = "input_05b_example.txt"
EXAMPLE_ANSWER = "MCD"

STACK_DISTANCE = 4


def main():
    """Test example input, and then process the actual puzzle input."""
    test_outcome(
        EXAMPLE_ANSWER, EXAMPLE_FILENAME_INITIAL, EXAMPLE_FILENAME_MOVES
    )
    filename_initial = "input_05a.txt"
    filename_moves = "input_05b.txt"
    initial_stacks = initialize_stacks(filename_initial)
    final_stacks = rearrange_stacks(initial_stacks, filename_moves)
    top_crates = get_top_crates(final_stacks)
    print(f"\nAfter the rearrangement, crates {top_crates} are on top.")


def initialize_stacks(filename):
    """Represent initial crate stacks using a dictionary with list values."""
    with open(filename) as file_object:
        crate_stack_lines = file_object.readlines()
    if len(crate_stack_lines) == 0:
        sys.exit("The file with the initial stacks is empty!")
    elif len(crate_stack_lines) == 1:
        sys.exit("The initial stacks are empty!")

    crate_stack_lines.reverse()
    nr_stacks = int(crate_stack_lines[0].rstrip()[-1])
    crate_stacks = {}
    for i in range(nr_stacks):
        crate_stacks[i + 1] = []
        for line in crate_stack_lines[1:]:
            crate = line[1 + i * STACK_DISTANCE]
            if crate == " ":
                break
            else:
                crate_stacks[i + 1].append(crate)
    return crate_stacks


def rearrange_stacks(crate_stacks, filename):
    """Create regex, read moves from input file, and move the creates."""
    move_regex = re.compile(r"move (\d+) from (\d+) to (\d+)")
    with open(filename) as file_object:
        for line in file_object:
            move_size, from_stack, to_stack = move_regex.search(line).groups()
            move_size = int(move_size)
            from_stack, to_stack = int(from_stack), int(to_stack)
            crates_to_move = crate_stacks[from_stack][-move_size:]
            crate_stacks[to_stack].extend(crates_to_move)
            del crate_stacks[from_stack][-move_size:]
    return crate_stacks


def get_top_crates(crate_stacks):
    top_crates = ""
    for i in range(len(crate_stacks)):
        if crate_stacks[i + 1]:
            top_crates += crate_stacks[i + 1][-1]
        else:
            top_crates += " "
    return top_crates


def test_outcome(expected, filename_initial, filename_moves):
    """Given input for which an answer is expected, check obtained result."""
    initial_stacks = initialize_stacks(filename_initial)
    final_stacks = rearrange_stacks(initial_stacks, filename_moves)
    actual = get_top_crates(final_stacks)
    filenames = " ".join([filename_initial, "and", filename_moves])
    try:
        assert actual == expected
        print(f"Expected outcome for input {filenames} confirmed.")
    except AssertionError:
        print(f"\nUnexpected outcome for input {filenames}:")
        print(f"Answer {expected} expected, but {actual} obtained.")


if __name__ == "__main__":
    main()
