"""
Solution --- Day 17: Pyroclastic Flow ---

Simulate the falling of rocks until a repetition is detected (in that the next
shape, jet index, and relevant aspects of the pattern of stopped rocks in the
chamber have occurred before) or until the maximum number of rocks has been
reached, whichever occurs first.
"""

import aoc_tools as aoc

CHAMBER_WIDTH = 7
HORZ_DIST = 2
VERT_DIST = 4
SHAPE_UNITS = (
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
    ((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 0), (0, 1), (1, 0), (1, 1)),
)


def main():
    filename = "input_17.txt"
    tower_height = simulate_falling_rocks(filename, 2022)
    print(f"After 2022 rocks, it is {tower_height} units tall.")
    tower_height = simulate_falling_rocks(filename, 1_000_000_000_000)
    print(f"After 1_000_000_000_000 rocks, it is {tower_height} units tall.")


def simulate_falling_rocks(filename, nr_rocks):
    """Simulate the falling of rocks, and obtain the tower height."""
    chamber, jet_pattern, shapes = initialize_simulation(filename)
    has_repeated = False

    jet_idx, shape_idx, depths = 0, 0, tuple([VERT_DIST] * CHAMBER_WIDTH)
    state_hist = {(jet_idx, shape_idx, depths): 0}
    height = 0
    height_hist = [height]

    for i in range(1, nr_rocks + 1):
        shape = shapes[shape_idx]
        jet_idx = simulate_single_rock(chamber, jet_pattern, jet_idx, shape)
        shape_idx = (shape_idx + 1) % len(SHAPE_UNITS)
        depths = determine_depths(chamber)
        height = len(chamber) - VERT_DIST

        if not has_repeated:
            previous = check_repetition(state_hist, jet_idx, shape_idx, depths)
            if previous is None:
                state_hist[(jet_idx, shape_idx, depths)] = i
            elif previous is not None:
                has_repeated = True
                cycle_length = i - previous
                cycle_height_increase = height - height_hist[previous]
                transient_length = nr_rocks % cycle_length

        height_hist.append(height)
        if has_repeated and i >= transient_length:
            height_transient = height_hist[transient_length]
            height_cycles = (nr_rocks // cycle_length) * cycle_height_increase
            height = height_transient + height_cycles
            break
    return height


def initialize_simulation(filename):
    """Initialize the chamber, the jet pattern, and the shapes."""
    chamber = [[False] * CHAMBER_WIDTH for _ in range(VERT_DIST)]
    jet_pattern = aoc.read_stripped(filename)
    shapes = [Shape(units) for units in SHAPE_UNITS]
    return chamber, jet_pattern, shapes


def determine_depths(chamber):
    """Determine the depth of the latest stopped rock in every column."""
    depths = []
    for col in range(CHAMBER_WIDTH):
        row = len(chamber) - VERT_DIST
        while not chamber[row][col] and row > 0:
            row -= 1
        depths.append(len(chamber) - row)
    return tuple(depths)


def check_repetition(state_history, jet_idx, shape_idx, depths):
    """Check whether jet index, shape, and depths have occurred before."""
    return state_history.get((jet_idx, shape_idx, depths))


def simulate_single_rock(chamber, jet_pattern, jet_idx, shape):
    """Simulate the falling of a rock."""
    bottom_left_x = HORZ_DIST
    bottom_left_y = len(chamber) - 1

    # Initially, no need to check floor or stopped rock collisions:
    for _ in range(VERT_DIST):
        if jet_pattern[jet_idx] == "<":
            if bottom_left_x > 0:
                bottom_left_x -= 1
        elif jet_pattern[jet_idx] == ">":
            if bottom_left_x < CHAMBER_WIDTH - shape.width:
                bottom_left_x += 1
        jet_idx = (jet_idx + 1) % len(jet_pattern)
        if bottom_left_y == len(chamber) - VERT_DIST:
            break
        bottom_left_y -= 1

    # Thereafter, check for floor or stopped rock collisions:
    while bottom_left_y > 0 and not any(
        chamber[bottom_left_y + u[0] - 1][bottom_left_x + u[1]]
        for u in shape.units
    ):
        bottom_left_y -= 1
        if jet_pattern[jet_idx] == "<":
            if bottom_left_x > 0 and not any(
                chamber[bottom_left_y + u[0]][bottom_left_x + u[1] - 1]
                for u in shape.units
            ):
                bottom_left_x -= 1
        elif jet_pattern[jet_idx] == ">":
            if bottom_left_x < CHAMBER_WIDTH - shape.width and not any(
                chamber[bottom_left_y + u[0]][bottom_left_x + u[1] + 1]
                for u in shape.units
            ):
                bottom_left_x += 1
        jet_idx = (jet_idx + 1) % len(jet_pattern)

    # The rock has come to rest:
    for u in shape.units:
        chamber[bottom_left_y + u[0]][bottom_left_x + u[1]] = True

    # Add rows to chamber to ensure VERT_DIST on top of highest stopped rock:
    if bottom_left_y + shape.height > len(chamber) - VERT_DIST:
        for _ in range(bottom_left_y + shape.height - len(chamber) + VERT_DIST):
            chamber.append([False] * CHAMBER_WIDTH)
    return jet_idx


class Shape:
    """Class to represent a rock shape."""

    def __init__(self, units):
        """Create a shape, and set its height and width."""
        self.units = units
        self.height = max(u[0] for u in self.units) + 1
        self.width = max(u[1] for u in self.units) + 1

        # Violating the following condition would lead to IndexErrors later on:
        assert self.height <= VERT_DIST


if __name__ == "__main__":
    main()
