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
        droplet_surface = check_facets(cube_list)
    else:
        is_accessible = map_accessibility(cube_list)
        droplet_surface = check_outer_facets(cube_list, is_accessible)
    return droplet_surface


def set_cubes(filename):
    """Read file input, and create a list with coordinates of the cubes."""
    cube_lines = aoc.read_stripped_lines(filename)
    cube_regex = re.compile(r"(\d+),(\d+),(\d+)")
    cube_list = []
    for line in cube_lines:
        cube_list.append([int(x) for x in cube_regex.search(line).groups()])
    return cube_list


def check_facets(cube_list):
    """For all facets, check whether they connect to empty space."""
    droplet_surface = 0
    for cube in cube_list:
        if [cube[0] + 1, cube[1], cube[2]] not in cube_list:
            droplet_surface += 1
        if [cube[0] - 1, cube[1], cube[2]] not in cube_list:
            droplet_surface += 1
        if [cube[0], cube[1] + 1, cube[2]] not in cube_list:
            droplet_surface += 1
        if [cube[0], cube[1] - 1, cube[2]] not in cube_list:
            droplet_surface += 1
        if [cube[0], cube[1], cube[2] + 1] not in cube_list:
            droplet_surface += 1
        if [cube[0], cube[1], cube[2] - 1] not in cube_list:
            droplet_surface += 1
    return droplet_surface


def map_accessibility(cube_list):
    """
    Determine whether empty spaces are accessible from outside. To this end, a
    box is created that contains the droplet in its interior. The outside is
    initialized as accessible, and iteratively empty spaces in the interior
    are identified as accessible until no new accessible spaces can be
    identified.
    """
    box_min = [min(c[dim] for c in cube_list) - 1 for dim in range(3)]
    box_max = [max(c[dim] for c in cube_list) + 1 for dim in range(3)]
    box = product(*[range(box_min[dim], box_max[dim] + 1) for dim in range(3)])

    is_accessible = {}
    for pos in box:
        if all(box_min[dim] < pos[dim] < box_max[dim] for dim in range(3)):
            is_accessible[pos] = False
        else:
            is_accessible[pos] = True

    is_mapped = False
    while not is_mapped:
        is_mapped = True
        for i in range(box_min[0] + 1, box_max[0]):
            for j in range(box_min[1] + 1, box_max[1]):
                for k in range(box_min[2] + 1, box_max[2]):
                    if (
                        not [i, j, k] in cube_list
                        and not is_accessible[(i, j, k)]
                        and (
                            is_accessible[(i - 1, j, k)]
                            or is_accessible[(i + 1, j, k)]
                            or is_accessible[(i, j - 1, k)]
                            or is_accessible[(i, j + 1, k)]
                            or is_accessible[(i, j, k - 1)]
                            or is_accessible[(i, j, k + 1)]
                        )
                    ):
                        is_accessible[(i, j, k)] = True
                        is_mapped = False
    return is_accessible


def check_outer_facets(cube_list, is_accessible):
    """For all facets, check whether they connect to accessible empty space."""
    droplet_surface = 0
    for cube in cube_list:
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
