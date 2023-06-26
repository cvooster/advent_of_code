"""Solution --- Day 18: Boiling Boulders ---"""

from itertools import product
import re

import aoc_tools as aoc


def main():
    filename = "input_18.txt"
    droplet_surface = calculate_surface(filename, False)
    print(f"The surface area of the lava droplet is {droplet_surface}.")
    droplet_surface = calculate_surface(filename, True)
    print(f"The outer surface area of the lava droplet is {droplet_surface}.")


def calculate_surface(filename, outer=False):
    """Loop through cubes to calculate the total surface or outer surface."""
    cube_list = set_cubes(filename)
    if not outer:
        return check_facets(cube_list)
    else:
        return check_outer_facets(cube_list, map_accessibility(cube_list))


def set_cubes(filename):
    """Read file input, and create a set with cube coordinates."""
    cube_lines = aoc.read_stripped_lines(filename)
    cube_regex = re.compile(r"(\d+),(\d+),(\d+)")
    cube_set = set()
    for line in cube_lines:
        cube_set.add(tuple(int(x) for x in cube_regex.search(line).groups()))
    return cube_set


def check_facets(cube_set):
    """For all facets, check whether they connect to empty space."""
    droplet_surface = 0
    for cube in cube_set:
        if (cube[0] + 1, cube[1], cube[2]) not in cube_set:
            droplet_surface += 1
        if (cube[0] - 1, cube[1], cube[2]) not in cube_set:
            droplet_surface += 1
        if (cube[0], cube[1] + 1, cube[2]) not in cube_set:
            droplet_surface += 1
        if (cube[0], cube[1] - 1, cube[2]) not in cube_set:
            droplet_surface += 1
        if (cube[0], cube[1], cube[2] + 1) not in cube_set:
            droplet_surface += 1
        if (cube[0], cube[1], cube[2] - 1) not in cube_set:
            droplet_surface += 1
    return droplet_surface


def map_accessibility(cube_set):
    """
    Determine whether empty spaces are accessible from outside.

    A box containing the droplet in its iterior is created. With the outside
    initialized as accessible, the procedure iteratively identifies accessible
    empty spaces in the interior until all such spaces have been identified.
    """
    bmin = [min(c[i] for c in cube_set) - 1 for i in range(3)]
    bmax = [max(c[i] for c in cube_set) + 1 for i in range(3)]
    box_list = list(product(*[range(bmin[i], bmax[i] + 1) for i in range(3)]))
    interior = list(product(*[range(bmin[i] + 1, bmax[i]) for i in range(3)]))

    is_accessible = {pos: True for pos in box_list}
    for pos in interior:
        is_accessible[pos] = False

    is_complete = False
    while not is_complete:
        is_complete = True
        for i, j, k in interior:
            if (i, j, k) not in cube_set and not is_accessible[(i, j, k)]:
                if (
                    is_accessible[(i - 1, j, k)]
                    or is_accessible[(i + 1, j, k)]
                    or is_accessible[(i, j - 1, k)]
                    or is_accessible[(i, j + 1, k)]
                    or is_accessible[(i, j, k - 1)]
                    or is_accessible[(i, j, k + 1)]
                ):
                    is_accessible[(i, j, k)] = True
                    is_complete = False
    return is_accessible


def check_outer_facets(cube_set, is_accessible):
    """For all facets, check whether they connect to accessible empty space."""
    droplet_surface = 0
    for cube in cube_set:
        if is_accessible[(cube[0] + 1, cube[1], cube[2])]:
            droplet_surface += 1
        if is_accessible[(cube[0] - 1, cube[1], cube[2])]:
            droplet_surface += 1
        if is_accessible[(cube[0], cube[1] + 1, cube[2])]:
            droplet_surface += 1
        if is_accessible[(cube[0], cube[1] - 1, cube[2])]:
            droplet_surface += 1
        if is_accessible[(cube[0], cube[1], cube[2] + 1)]:
            droplet_surface += 1
        if is_accessible[(cube[0], cube[1], cube[2] - 1)]:
            droplet_surface += 1
    return droplet_surface


if __name__ == "__main__":
    main()
