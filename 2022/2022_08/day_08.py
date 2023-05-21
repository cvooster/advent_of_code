"""Solution --- Day 8: Treetop Tree House ---"""

import math

import aoc_tools as aoc


def main():
    filename = "input_08.txt"
    nr_visible, max_scenic_score = calculate_tree_house_metrics(filename)
    print(f"From outside the grid {nr_visible} trees are visible.")
    print(f"The highest possible scenic score is {max_scenic_score}.")


def calculate_tree_house_metrics(filename):
    """Read file input, calculate viewing distances, and derive metrics."""
    tree_lines = aoc.read_stripped_lines(filename)
    tree_grid = [[int(x) for x in list(line)] for line in tree_lines]
    grid_width = len(tree_grid)
    grid_height = len(tree_grid[0])
    is_visible = [[False] * grid_width for _ in range(grid_height)]
    scenic_scores = [[-1] * grid_width for _ in range(grid_height)]

    for idx_y in range(0, grid_height):
        for idx_x in range(0, grid_width):
            view_distances = []
            is_visibles = []
            for d_y, d_x in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                dist, iv = evaluate_view(tree_grid, idx_y, idx_x, d_y, d_x)
                view_distances.append(dist)
                is_visibles.append(iv)
            scenic_scores[idx_y][idx_x] = math.prod(view_distances)
            is_visible[idx_y][idx_x] = any(is_visibles)

    max_scenic_score = max(max(row) for row in scenic_scores)
    nr_visible = sum(sum(row) for row in is_visible)
    return nr_visible, max_scenic_score


def evaluate_view(tree_grid, idx_y, idx_x, d_y, d_x):
    """Evaluate the number of visible trees in a given direction from a tree."""
    grid_width = len(tree_grid)
    grid_height = len(tree_grid[0])
    view_y = idx_y + d_y
    view_x = idx_x + d_x
    view_distance = 0
    is_visible = True

    while is_visible and 0 <= view_y < grid_height and 0 <= view_x < grid_width:
        view_distance += 1
        is_visible = tree_grid[view_y][view_x] < tree_grid[idx_y][idx_x]
        view_y += d_y
        view_x += d_x
    return view_distance, is_visible


if __name__ == "__main__":
    main()
