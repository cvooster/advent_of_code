"""Solution --- Day 9: Rope Bridge ---"""

import aoc_tools as aoc


def main():
    filename = "input_09.txt"
    nr_visited = count_visited_positions(filename, 2)
    print(f"The tail of a rope with 2 knots visits {nr_visited} positions.")
    nr_visited = count_visited_positions(filename, 10)
    print(f"The tail of a rope with 10 knots visits {nr_visited} positions.")


def count_visited_positions(filename, nr_knots):
    """Initialize, simulate rope, and count positions visited by its tail."""
    directions, move_sizes = initialize_moves(filename)
    return simulate_rope(nr_knots, directions, move_sizes)


def initialize_moves(filename):
    """Read file input to get the directions and move sizes."""
    head_move_lines = aoc.read_stripped_lines(filename)
    directions = [line[0] for line in head_move_lines]
    move_sizes = [int(line[2:]) for line in head_move_lines]
    return directions, move_sizes


def simulate_rope(nr_knots, directions, move_sizes):
    """Simulate the rope and count the positions visited by its tail."""
    min_y, max_y, min_x, max_x = bound_rope_positions(directions, move_sizes)
    grid_height = max_y - min_y + 1
    grid_width = max_x - min_x + 1
    is_visited = [[False] * grid_width for _ in range(grid_height)]
    knots_y = [0] * nr_knots
    knots_x = [0] * nr_knots

    for direction, move_size in zip(directions, move_sizes):
        for _ in range(move_size):
            if direction == "U":
                knots_y[0] += 1
            elif direction == "D":
                knots_y[0] -= 1
            elif direction == "L":
                knots_x[0] -= 1
            elif direction == "R":
                knots_x[0] += 1
            for idx in range(1, nr_knots):
                knots_y, knots_x = move_knot(knots_y, knots_x, idx)
            is_visited[knots_y[-1] - min_y][knots_x[-1] - min_x] = True
    return sum(sum(row) for row in is_visited)


def bound_rope_positions(directions, move_sizes):
    """Simulate head movements to obtain bounds on area in which rope moves."""
    min_y, max_y, min_x, max_x = 0, 0, 0, 0
    head_y = 0
    head_x = 0
    for direction, move_size in zip(directions, move_sizes):
        if direction == "U":
            head_y += move_size
            max_y = max(max_y, head_y)
        elif direction == "D":
            head_y -= move_size
            min_y = min(min_y, head_y)
        elif direction == "L":
            head_x -= move_size
            min_x = min(min_x, head_x)
        elif direction == "R":
            head_x += move_size
            max_x = max(max_x, head_x)
    return min_y, max_y, min_x, max_x


def move_knot(knots_y, knots_x, idx):
    """Move the (idx+1)th knot in response to the idx-th knot."""
    dist_y = knots_y[idx - 1] - knots_y[idx]
    dist_x = knots_x[idx - 1] - knots_x[idx]
    if abs(dist_y) == 2 and abs(dist_x) == 2:
        knots_y[idx] += dist_y // 2
        knots_x[idx] += dist_x // 2
    elif abs(dist_y) == 2 and -1 <= dist_x <= 1:
        knots_y[idx] += dist_y // 2
        knots_x[idx] = knots_x[idx - 1]
    elif -1 <= dist_y <= 1 and abs(dist_x) == 2:
        knots_y[idx] = knots_y[idx - 1]
        knots_x[idx] += dist_x // 2
    return knots_y, knots_x


if __name__ == "__main__":
    main()
