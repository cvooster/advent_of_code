"""Solution --- Day 5: Supply Stacks ---"""

import re

import aoc_tools as aoc

STACK_DISTANCE = 4


def main():
    filename_initial, filename_moves = "input_05a.txt", "input_05b.txt"
    top_crates = get_final_top_crates(filename_initial, filename_moves, False)
    print(f"After one-at-a-time rearrangement, crates {top_crates} are on top.")
    top_crates = get_final_top_crates(filename_initial, filename_moves, True)
    print(f"After multiple rearrangement, crates {top_crates} are on top.")


def get_final_top_crates(filename_initial, filename_moves, mover_9001):
    """Identify the top crates after the rearrangement procedure."""
    initial_stacks = initialize_stacks(filename_initial)
    final_stacks = rearrange_stacks(initial_stacks, filename_moves, mover_9001)
    return get_top_crates(final_stacks)


def initialize_stacks(filename_initial):
    """Read file input, initialize stacks as a dictionary with list values."""
    crate_stack_lines = aoc.read_lines(filename_initial)
    nr_stacks = int(crate_stack_lines[-1].rstrip()[-1])
    crate_stacks = {}
    for i in range(nr_stacks):
        crate_stacks[i + 1] = []
        for line in crate_stack_lines[-2::-1]:
            crate = line[1 + i * STACK_DISTANCE]
            if crate != " ":
                crate_stacks[i + 1].append(crate)
            else:
                break
    return crate_stacks


def rearrange_stacks(crate_stacks, filename_moves, mover_9001):
    """Read file input, and move the crates between the stacks."""
    move_regex = re.compile(r"move (\d+) from (\d+) to (\d+)")
    move_lines = aoc.read_stripped_lines(filename_moves)
    for line in move_lines:
        move_size, from_stack, to_stack = move_regex.search(line).groups()
        move_size = int(move_size)
        from_stack = int(from_stack)
        to_stack = int(to_stack)
        if not mover_9001:
            for _ in range(move_size):
                crate_stacks[to_stack].append(crate_stacks[from_stack].pop())
        else:
            crates_to_move = crate_stacks[from_stack][-move_size:]
            crate_stacks[to_stack].extend(crates_to_move)
            del crate_stacks[from_stack][-move_size:]
    return crate_stacks


def get_top_crates(crate_stacks):
    """Join the top crates of all stacks into one string (space if no crate.)"""
    return "".join([cs[-1] if cs else " " for cs in crate_stacks.values()])


if __name__ == "__main__":
    main()
