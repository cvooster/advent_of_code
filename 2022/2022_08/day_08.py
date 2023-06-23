"""Solution --- Day 8: Treetop Tree House ---"""

import aoc_tools as aoc


def main():
    filename = "input_08.txt"
    nr_visible, max_scenic_score = calculate_tree_house_metrics(filename)
    print(f"From outside the grid {nr_visible} trees are visible.")
    print(f"The highest possible scenic score is {max_scenic_score}.")


def calculate_tree_house_metrics(filename):
    """Read file input, calculate viewing distances, and derive metrics."""
    tree_lines = aoc.read_stripped_lines(filename)
    grid = [[int(x) for x in list(line)] for line in tree_lines]
    grid_height = len(grid)
    grid_width = len(grid[0])

    scenic_scores = [[1] * grid_width for _ in range(grid_height)]
    is_visibles = [[False] * grid_width for _ in range(grid_height)]
    for idx_y in range(grid_height):
        for idx_x in range(grid_width):
            for d_y, d_x in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                view_distance, is_visible = evaluate_direction(
                    grid, grid_height, grid_width, idx_y, idx_x, d_y, d_x
                )
                scenic_scores[idx_y][idx_x] *= view_distance
                if not is_visibles[idx_y][idx_x]:
                    is_visibles[idx_y][idx_x] = is_visible

    max_scenic_score = max(max(row) for row in scenic_scores)
    nr_visible = sum(sum(row) for row in is_visibles)
    return nr_visible, max_scenic_score


def evaluate_direction(grid, grid_height, grid_width, idx_y, idx_x, d_y, d_x):
    """Evaluate the number of visible trees in a given direction from a tree."""
    view_distance = 0
    is_visible = True
    target_y = idx_y + d_y
    target_x = idx_x + d_x

    while 0 <= target_y < grid_height and 0 <= target_x < grid_width:
        view_distance += 1
        is_visible = grid[target_y][target_x] < grid[idx_y][idx_x]
        target_y += d_y
        target_x += d_x
        if not is_visible:
            break
    return view_distance, is_visible


if __name__ == "__main__":
    main()
