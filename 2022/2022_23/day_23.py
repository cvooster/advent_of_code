"""Solution --- Day 23: Unstable Diffusion ---"""

import aoc_tools as aoc


def main():
    filename = "input_23.txt"
    empty_tiles, _ = simulate_elves(filename, 10)
    print(f"The number of empty tiles in the rectangle is {empty_tiles}.")
    _, nr_rounds = simulate_elves(filename)
    print(f"The first round without moves is {nr_rounds}.")


def simulate_elves(filename, max_rounds=None):
    """Simulate movements for a given number of rounds or until completion."""
    elves = initialize_elves(filename)
    idx_preferred_direction = 0
    is_complete = False
    empty_tiles = None
    nr_rounds = 0

    while not is_complete:
        nr_rounds += 1
        simulate_proposals(elves, idx_preferred_direction)
        is_complete = simulate_execution(elves)
        idx_preferred_direction = (idx_preferred_direction + 1) % 4
        if max_rounds is not None and nr_rounds == max_rounds:
            break
    if max_rounds is not None:
        empty_tiles = count_empty_tiles(elves)
    return empty_tiles, nr_rounds


def initialize_elves(filename):
    """Read file input, and initialize the elves."""
    grid_lines = aoc.read_stripped_lines(filename)
    elves = []
    for i, line in enumerate(grid_lines):
        for j, char in enumerate(line):
            if char == "#":
                elves.append(Elf(j, i))
    return elves


def simulate_proposals(elves, idx_preferred_direction):
    """Generate the proposed moves of all elves."""
    min_x, min_y, elf_grid = generate_pos_grid(elves)
    for elf in elves:
        idx_y = elf.pos_y - min_y + 1
        idx_x = elf.pos_x - min_x + 1
        if not (
            elf_grid[idx_y - 1][idx_x - 1]
            or elf_grid[idx_y - 1][idx_x]
            or elf_grid[idx_y - 1][idx_x + 1]
            or elf_grid[idx_y][idx_x - 1]
            or elf_grid[idx_y][idx_x + 1]
            or elf_grid[idx_y + 1][idx_x - 1]
            or elf_grid[idx_y + 1][idx_x]
            or elf_grid[idx_y + 1][idx_x + 1]
        ):
            elf.is_pending = False
        else:
            shift = 0
            while not elf.is_pending and shift < 4:
                idx_direction = (idx_preferred_direction + shift) % 4
                if idx_direction == 0:
                    if not (
                        elf_grid[idx_y - 1][idx_x - 1]
                        or elf_grid[idx_y - 1][idx_x]
                        or elf_grid[idx_y - 1][idx_x + 1]
                    ):
                        elf.proposal_x = elf.pos_x
                        elf.proposal_y = elf.pos_y - 1
                        elf.is_pending = True
                elif idx_direction == 1:
                    if not (
                        elf_grid[idx_y + 1][idx_x - 1]
                        or elf_grid[idx_y + 1][idx_x]
                        or elf_grid[idx_y + 1][idx_x + 1]
                    ):
                        elf.proposal_x = elf.pos_x
                        elf.proposal_y = elf.pos_y + 1
                        elf.is_pending = True
                elif idx_direction == 2:
                    if not (
                        elf_grid[idx_y - 1][idx_x - 1]
                        or elf_grid[idx_y][idx_x - 1]
                        or elf_grid[idx_y + 1][idx_x - 1]
                    ):
                        elf.proposal_x = elf.pos_x - 1
                        elf.proposal_y = elf.pos_y
                        elf.is_pending = True
                elif idx_direction == 3:
                    if not (
                        elf_grid[idx_y - 1][idx_x + 1]
                        or elf_grid[idx_y][idx_x + 1]
                        or elf_grid[idx_y + 1][idx_x + 1]
                    ):
                        elf.proposal_x = elf.pos_x + 1
                        elf.proposal_y = elf.pos_y
                        elf.is_pending = True
                shift += 1


def simulate_execution(elves):
    """Decide on the execution of proposed moves."""
    is_complete = True
    min_x, min_y, elf_grid = generate_proposal_grid(elves)
    for elf in elves:
        if elf.is_pending:
            idx_y = elf.proposal_y - min_y + 1
            idx_x = elf.proposal_x - min_x + 1
            if elf_grid[idx_y][idx_x] == 1:
                elf.pos_x = elf.proposal_x
                elf.pos_y = elf.proposal_y
                elf.is_pending = False
                is_complete = False
            else:
                elf.proposal_x = elf.pos_x
                elf.proposal_y = elf.pos_y
                elf.is_pending = False
    return is_complete


def generate_pos_grid(elves):
    """
    Generate a grid in which elf positions are marked as True. An extra top and
    bottom row and extra left and right column is added to avoid IndexErrors
    when elves are checking whether a direction is valid.
    """
    min_x, max_x, min_y, max_y = get_rectangle_dimensions(elves)
    grid_height = max_y - min_y + 1 + 2
    grid_width = max_x - min_x + 1 + 2
    elf_grid = [[False] * grid_width for _ in range(grid_height)]
    for elf in elves:
        idx_y = elf.pos_y - min_y + 1
        idx_x = elf.pos_x - min_x + 1
        elf_grid[idx_y][idx_x] = True
    return min_x, min_y, elf_grid


def generate_proposal_grid(elves):
    """
    Generate a grid that counts the number of elves proposing a position. An
    extra top and bottom row and extra left and right column is added because
    elves' proposals can be outside the current smallest rectangle.
    """
    min_x, max_x, min_y, max_y = get_rectangle_dimensions(elves)
    grid_height = max_y - min_y + 1 + 2
    grid_width = max_x - min_x + 1 + 2
    elf_grid = [[0] * grid_width for _ in range(grid_height)]
    for elf in elves:
        if elf.is_pending:
            idx_y = elf.proposal_y - min_y + 1
            idx_x = elf.proposal_x - min_x + 1
            elf_grid[idx_y][idx_x] += 1
    return min_x, min_y, elf_grid


def count_empty_tiles(elves):
    """Count the empty tiles in the smallest rectangle containing all elves."""
    min_x, max_x, min_y, max_y = get_rectangle_dimensions(elves)
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


def get_rectangle_dimensions(elves):
    """Determine dimensions of the smallest rectangle containing all elves."""
    min_x = min([elf.pos_x for elf in elves])
    max_x = max([elf.pos_x for elf in elves])
    min_y = min([elf.pos_y for elf in elves])
    max_y = max([elf.pos_y for elf in elves])
    return min_x, max_x, min_y, max_y


class Elf:
    "Class to represent an elf."

    def __init__(self, pos_x, pos_y):
        "Create an elf, with a position and (possibly pending) proposal."
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.proposal_x = pos_x
        self.proposal_y = pos_y
        self.is_pending = False


if __name__ == "__main__":
    main()
