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
SHAPE_UNITS = [
    ((0, 0), (0, 1), (0, 2), (0, 3)),
    ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1)),
    ((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)),
    ((0, 0), (1, 0), (2, 0), (3, 0)),
    ((0, 0), (0, 1), (1, 0), (1, 1)),
]


def main():
    filename = "input_17.txt"
    tower_height = simulate_falling_rocks(filename, 2022)
    print(f"After 2022 rocks, it is {tower_height} units tall.")
    tower_height = simulate_falling_rocks(filename, 1_000_000_000_000)
    print(f"After 1_000_000_000_000 rocks, it is {tower_height} units tall.")


def simulate_falling_rocks(filename, nr_rocks):
    """Simulate the falling of rocks, and obtain the tower height."""
    chamber, shapes, jet_pattern = initialize_simulation(filename)
    shape_idx = 0
    jet_idx = 0
    sim_history = {
        "shape_idx": [shape_idx],
        "jet_idx": [jet_idx],
        "height": [0],
        "depths": [[VERT_DIST] * CHAMBER_WIDTH],
    }
    has_repeated = False

    for i in range(nr_rocks):
        shape = shapes[shape_idx]
        jet_idx = simulate_single_rock(chamber, shape, jet_pattern, jet_idx)
        shape_idx = (shape_idx + 1) % len(SHAPE_UNITS)
        depths = determine_depths(chamber)
        height = len(chamber) - VERT_DIST

        if not has_repeated:
            previous = check_repetition(sim_history, shape_idx, jet_idx, depths)
            if previous is not None:
                has_repeated = True
                cycle_length = (i + 1) - previous
                cycle_height_increase = height - sim_history["height"][previous]
                transient_length = nr_rocks % cycle_length

        sim_history["shape_idx"].append(shape_idx)
        sim_history["jet_idx"].append(jet_idx)
        sim_history["depths"].append(depths)
        sim_history["height"].append(height)

        if has_repeated and i >= transient_length - 1:
            height_transient = sim_history["height"][transient_length]
            height_cycles = (nr_rocks // cycle_length) * cycle_height_increase
            height = height_transient + height_cycles
            break
    return height


def initialize_simulation(filename):
    """Initialize the chamber, the shapes, and the jet pattern."""
    chamber = [[False] * CHAMBER_WIDTH for _ in range(VERT_DIST)]
    shapes = []
    for units in SHAPE_UNITS:
        shapes.append(Shape(units))
    jet_pattern = aoc.read_stripped(filename)
    return chamber, shapes, jet_pattern


def determine_depths(chamber):
    """Determine the depth of the latest stopped rock in every column."""
    depths = []
    for col in range(CHAMBER_WIDTH):
        depth = VERT_DIST
        while len(chamber) - depth >= 0:
            if not chamber[len(chamber) - depth][col]:
                depth += 1
            else:
                break
        depths.append(depth)
    return depths


def check_repetition(sim_history, shape_idx, jet_idx, depths):
    """Check whether shape, jet index, and depths have occurred before."""
    zipped_history = zip(
        sim_history["shape_idx"], sim_history["jet_idx"], sim_history["depths"]
    )
    try:
        previous = list(zipped_history).index((shape_idx, jet_idx, depths))
    except ValueError:
        previous = None
    return previous


def simulate_single_rock(chamber, shape, jet_pattern, jet_idx):
    """Simulate the falling of a rock."""
    bottom_left_x = HORZ_DIST
    bottom_left_y = len(chamber) - 1

    # Initially, no need to check floor or stopped rock collisions:
    for _ in range(VERT_DIST - 1):
        if jet_pattern[jet_idx] == "<":
            if bottom_left_x > 0:
                bottom_left_x -= 1
        elif jet_pattern[jet_idx] == ">":
            if bottom_left_x < CHAMBER_WIDTH - shape.width:
                bottom_left_x += 1
        jet_idx = (jet_idx + 1) % len(jet_pattern)
        bottom_left_y -= 1

    # Thereafter, check for floor or stopped rock collisions:
    while True:
        if jet_pattern[jet_idx] == "<":
            if bottom_left_x > 0 and not any(
                chamber[bottom_left_y + unit[0]][bottom_left_x + unit[1] - 1]
                for unit in shape.units
            ):
                bottom_left_x -= 1
        elif jet_pattern[jet_idx] == ">":
            if bottom_left_x < CHAMBER_WIDTH - shape.width and not any(
                chamber[bottom_left_y + unit[0]][bottom_left_x + unit[1] + 1]
                for unit in shape.units
            ):
                bottom_left_x += 1
        jet_idx = (jet_idx + 1) % len(jet_pattern)
        if bottom_left_y > 0 and not any(
            chamber[bottom_left_y + unit[0] - 1][bottom_left_x + unit[1]]
            for unit in shape.units
        ):
            bottom_left_y -= 1
        else:
            break
    for unit in shape.units:
        chamber[bottom_left_y + unit[0]][bottom_left_x + unit[1]] = True

    # In the chamber, ensure VERT_DIST rows on top of highest stopped rock:
    if bottom_left_y + shape.height > len(chamber) - VERT_DIST:
        for _ in range(bottom_left_y + shape.height - len(chamber) + VERT_DIST):
            chamber.append([False for _ in range(CHAMBER_WIDTH)])
    return jet_idx


class Shape:
    """Class to represent a rock shape."""

    def __init__(self, units):
        """Create a shape, and set its height and width."""
        self.units = units
        self.height = max(unit[0] for unit in self.units) + 1
        self.width = max(unit[1] for unit in self.units) + 1


if __name__ == "__main__":
    main()
