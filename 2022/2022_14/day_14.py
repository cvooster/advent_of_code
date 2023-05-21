"""Solution --- Day 14: Regolith Reservoir ---"""

import copy
import re

import aoc_tools as aoc

SAND_ENTRANCE = (500, 0)
FLOOR_DISTANCE = 2


def main():
    filename = "input_14.txt"
    rest_units = compute_rest_units(filename, False)
    print(f"Before sand flows into the abyss, {rest_units} units come to rest.")
    rest_units = compute_rest_units(filename, True)
    print(f"Before the source gets blocked, {rest_units} units come to rest.")


def compute_rest_units(filename, has_floor=False):
    """Initialize a grid, simulate sand, and count units that come to rest."""
    is_rock, min_x, max_y = initialize_grid(filename, has_floor)
    if not has_floor:
        is_occupied = simulate_without_floor(is_rock, min_x, max_y)
    else:
        is_occupied = simulate_with_floor(is_rock, min_x)
    return sum(sum(io) for io in is_occupied) - sum(sum(ir) for ir in is_rock)


def initialize_grid(filename, has_floor):
    """Read file input, and initialize a grid with rocks marked as True."""
    rock_coordinate_regex = re.compile(r"(\d+),(\d+)")
    rock_lines = aoc.read_stripped_lines(filename)
    rock_paths = []
    for rock_line in rock_lines:
        coordinates = rock_coordinate_regex.findall(rock_line)
        rock_paths.append([(int(co[0]), int(co[1])) for co in coordinates])

    # Obtain grid dimensions:
    comin_x = min(min(co[0] for co in rock_path) for rock_path in rock_paths)
    comax_x = max(max(co[0] for co in rock_path) for rock_path in rock_paths)
    comax_y = max(max(co[1] for co in rock_path) for rock_path in rock_paths)
    if not has_floor:
        max_y = comax_y
        min_x = comin_x - 1
        max_x = comax_x + 1
    else:
        max_y = comax_y + FLOOR_DISTANCE
        min_x = min(comin_x - 1, SAND_ENTRANCE[0] - max_y)
        max_x = max(comax_x + 1, SAND_ENTRANCE[0] + max_y)
    is_rock = [[False] * (max_x - min_x + 1) for _ in range(0, max_y + 1)]

    # Set points on the rock path (and the floor) to True:
    for rock_path in rock_paths:
        for co_idx in range(len(rock_path) - 1):
            if rock_path[co_idx][0] == rock_path[co_idx + 1][0]:
                start_y = min(rock_path[co_idx][1], rock_path[co_idx + 1][1])
                end_y = max(rock_path[co_idx][1], rock_path[co_idx + 1][1])
                for pos_y in range(start_y, end_y + 1):
                    is_rock[pos_y][rock_path[co_idx][0] - min_x] = True
            elif rock_path[co_idx][1] == rock_path[co_idx + 1][1]:
                start_x = min(rock_path[co_idx][0], rock_path[co_idx + 1][0])
                end_x = max(rock_path[co_idx][0], rock_path[co_idx + 1][0])
                for pos_x in range(start_x, end_x + 1):
                    is_rock[rock_path[co_idx][1]][pos_x - min_x] = True
    if has_floor:
        for pos_x in range(min_x, max_x + 1):
            is_rock[max_y][pos_x - min_x] = True
    return is_rock, min_x, max_y


def simulate_without_floor(is_rock, min_x, max_y):
    """Simulate the falling of sand until it flows into the abyss."""
    is_occupied = copy.deepcopy(is_rock)
    into_abyss = False
    while not into_abyss:
        sand_x, sand_y = SAND_ENTRANCE
        while not into_abyss:
            if not is_occupied[sand_y + 1][sand_x - min_x]:
                sand_y += 1
            elif not is_occupied[sand_y + 1][sand_x - min_x - 1]:
                sand_x -= 1
                sand_y += 1
            elif not is_occupied[sand_y + 1][sand_x - min_x + 1]:
                sand_x += 1
                sand_y += 1
            else:
                is_occupied[sand_y][sand_x - min_x] = True
                break
            into_abyss = sand_y == max_y
    return is_occupied


def simulate_with_floor(is_rock, min_x):
    """Simulate the falling of sand until the source gets blocked."""
    is_occupied = copy.deepcopy(is_rock)
    while not is_occupied[0][SAND_ENTRANCE[0] - min_x]:
        sand_x, sand_y = SAND_ENTRANCE
        while True:
            if not is_occupied[sand_y + 1][sand_x - min_x]:
                sand_y += 1
            elif not is_occupied[sand_y + 1][sand_x - min_x - 1]:
                sand_x -= 1
                sand_y += 1
            elif not is_occupied[sand_y + 1][sand_x - min_x + 1]:
                sand_x += 1
                sand_y += 1
            else:
                is_occupied[sand_y][sand_x - min_x] = True
                break
    return is_occupied


if __name__ == "__main__":
    main()
