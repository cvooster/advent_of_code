"""Solution --- Day 24: Blizzard Basin ---"""

import copy

import aoc_tools as aoc


def main():
    filename = "input_24.txt"
    length_shortest = compute_shortest(filename, 1)
    print(f"Shortest path to reach the sink is {length_shortest} long.")
    length_shortest = compute_shortest(filename, 2)
    print(f"Shortest path to twice reach the sink is {length_shortest} long.")


def compute_shortest(filename, nr_sink_visits):
    """Compute shortest back-and-forth path for given number of sink visits."""
    blizzards, grid_height, grid_width = initialize_blizzards(filename)
    minutes = 0
    no_reach = {
        "source": False,
        "in": [[False for _ in range(grid_width)] for _ in range(grid_height)],
        "sink": False,
    }

    for sink_visit in range(nr_sink_visits):
        can_reach = copy.deepcopy(no_reach)
        can_reach["source"] = True
        while not can_reach["sink"]:
            can_reach = dynamic_programming_update(blizzards, can_reach)
            minutes += 1
        if sink_visit == nr_sink_visits - 1:
            break
        can_reach = copy.deepcopy(no_reach)
        can_reach["sink"] = True
        while not can_reach["source"]:
            can_reach = dynamic_programming_update(blizzards, can_reach)
            minutes += 1
    return minutes


def initialize_blizzards(filename):
    """Read file input, and initialize the blizzards."""
    grid_lines = aoc.read_stripped_lines(filename)
    grid_height = len(grid_lines) - 2
    grid_width = len(grid_lines[0]) - 2
    blizzards = []
    for idx_y in range(1, grid_height + 1):
        for idx_x in range(1, grid_width + 1):
            if not grid_lines[idx_y][idx_x] == ".":
                blizzards.append(
                    Blizzard(idx_x - 1, idx_y - 1, grid_lines[idx_y][idx_x])
                )
    return blizzards, grid_height, grid_width


def dynamic_programming_update(blizzards, can_reach):
    """Given reachible locations, identify reachables after one more minute."""
    old_source = can_reach["source"]
    old_sink = can_reach["sink"]
    old_in = can_reach["in"]
    grid_height = len(old_in)
    grid_width = len(old_in[0])

    for blizzard in blizzards:
        blizzard.move(grid_height, grid_width)
    is_blizzard = map_valley(blizzards, grid_height, grid_width)

    new_source = old_source or old_in[0][0]
    new_sink = old_sink or old_in[-1][-1]
    new_in = [[False] * grid_width for _ in range(grid_height)]
    for idx_y in range(grid_height):
        for idx_x in range(grid_width):
            new_in[idx_y][idx_x] = not is_blizzard[idx_y][idx_x] and (
                old_in[idx_y][idx_x]
                or (idx_y > 0 and old_in[idx_y - 1][idx_x])
                or (idx_y < grid_height - 1 and old_in[idx_y + 1][idx_x])
                or (idx_x > 0 and old_in[idx_y][idx_x - 1])
                or (idx_x < grid_width - 1 and old_in[idx_y][idx_x + 1])
            )
    # It is also possible to enter valley from source or sink:
    new_in[0][0] = new_in[0][0] or (not is_blizzard[0][0] and old_source)
    new_in[-1][-1] = new_in[-1][-1] or (not is_blizzard[-1][-1] and old_sink)

    return {"source": new_source, "in": new_in, "sink": new_sink}


def map_valley(blizzards, grid_height, grid_width):
    """Generate a grid in which blizzard locations are marked as True."""
    is_blizzard = [[False] * grid_width for _ in range(grid_height)]
    for blizzard in blizzards:
        is_blizzard[blizzard.idx_y][blizzard.idx_x] = True
    return is_blizzard


class Blizzard:
    """Class to represent a blizzard."""

    def __init__(self, idx_x, idx_y, direction):
        """Create a blizzard with x- and y-indices and a direction of motion."""
        self.idx_x = idx_x
        self.idx_y = idx_y
        self.direction = direction

    def move(self, grid_height, grid_width):
        """Move the blizzard in its indicated direction."""
        if self.direction == "^":
            self.idx_y = (self.idx_y - 1) % grid_height
        elif self.direction == "v":
            self.idx_y = (self.idx_y + 1) % grid_height
        elif self.direction == "<":
            self.idx_x = (self.idx_x - 1) % grid_width
        elif self.direction == ">":
            self.idx_x = (self.idx_x + 1) % grid_width


if __name__ == "__main__":
    main()
