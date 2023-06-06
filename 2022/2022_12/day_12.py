"""
Solution --- Day 12: Hill Climbing Algorithm ---

Note that instead of using Dijkstra's algorithm to compute the shortest path to
the sink, I use it to compute the shortest path from the sink (either to a given
source or to all squares with elevation level 'a').
"""

import aoc_tools as aoc


def main():
    filename = "input_12.txt"
    shortest_length = compute_shortest(filename, True)
    print(f"The fewest steps to reach E from S is {shortest_length}.")
    shortest_length = compute_shortest(filename, False)
    print(f"The fewest steps to reach E from any a is {shortest_length}.")


def compute_shortest(filename, fix_source=True):
    """Apply Dijkstra's algorithm, and get the length of the shortest path."""
    elevation, source, sink = set_heightmap(filename)
    distances = compute_distances_from_sink(elevation, sink)
    if fix_source:
        return get_sink_source_distance(elevation, distances, source)
    else:
        return get_sink_source_distance(elevation, distances)


def set_heightmap(filename):
    """Read file input, and convert to numeric elevations."""
    elevation_lines = aoc.read_stripped_lines(filename)
    source = next(
        (
            (i, line.index("S"))
            for i, line in enumerate(elevation_lines)
            if "S" in line
        )
    )
    sink = next(
        (
            (i, line.index("E"))
            for i, line in enumerate(elevation_lines)
            if "E" in line
        )
    )
    elevation_lines[source[0]] = elevation_lines[source[0]].replace("S", "a")
    elevation_lines[sink[0]] = elevation_lines[sink[0]].replace("E", "z")
    elevation = [[ord(char) for char in line] for line in elevation_lines]
    return elevation, source, sink


def compute_distances_from_sink(elevation, sink):
    """Apply Dijkstra's algorithm. Neighbors must satisfy height condition."""
    grid_height = len(elevation)
    grid_width = len(elevation[0])
    upper_bound = grid_height * grid_width
    distances = [[upper_bound] * grid_width for _ in range(grid_height)]
    distances[sink[0]][sink[1]] = 0
    has_been_visited = [[False] * grid_width for _ in range(grid_height)]

    next_min_distance = 0
    current_y = sink[0]
    current_x = sink[1]

    while next_min_distance < upper_bound:
        has_been_visited[current_y][current_x] = True

        neighbors = []
        if current_y > 0:
            neighbors.append((current_y - 1, current_x))
        if current_y < grid_height - 1:
            neighbors.append((current_y + 1, current_x))
        if current_x > 0:
            neighbors.append((current_y, current_x - 1))
        if current_x < grid_width - 1:
            neighbors.append((current_y, current_x + 1))
        for neighbor_y, neighbor_x in neighbors:
            if (
                elevation[neighbor_y][neighbor_x]
                >= elevation[current_y][current_x] - 1
                and not has_been_visited[neighbor_y][neighbor_x]
            ):
                distances[neighbor_y][neighbor_x] = min(
                    distances[neighbor_y][neighbor_x],
                    distances[current_y][current_x] + 1,
                )

        next_min_distance = upper_bound
        for idx_y in range(grid_height):
            for idx_x in range(grid_width):
                if (
                    not has_been_visited[idx_y][idx_x]
                    and distances[idx_y][idx_x] < next_min_distance
                ):
                    next_min_distance = distances[idx_y][idx_x]
                    current_y = idx_y
                    current_x = idx_x
    return distances


def get_sink_source_distance(elevation, distances, source=None):
    """From all distances from the sink, select the one to the (best) source."""
    grid_height = len(elevation)
    grid_width = len(elevation[0])
    upper_bound = grid_height * grid_width

    if source is not None:
        shortest_length = distances[source[0]][source[1]]
    else:
        shortest_length = upper_bound
        for idx_y in range(grid_height):
            for idx_x in range(grid_width):
                if elevation[idx_y][idx_x] == ord("a"):
                    shortest_length = min(
                        shortest_length, distances[idx_y][idx_x]
                    )
    if shortest_length == upper_bound:
        raise ValueError("Reaching the sink is impossible!")
    return shortest_length


if __name__ == "__main__":
    main()
