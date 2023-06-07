"""--- Day 15: Beacon Exclusion Zone ---"""

import re

import aoc_tools as aoc

X_MULTIPLIER = 4_000_000
Y_MULTIPLIER = 1


def main():
    filename = "input_15.txt"
    nr_positions = count_infeasible_positions(filename, 2_000_000)
    print(f"In the given row, {nr_positions} positions cannot contain beacons.")
    range_x, range_y = (0, 4_000_000), (0, 4_000_000)
    tuning_frequency = calculate_tuning_frequency(filename, range_x, range_y)
    print(f"The tuning frequency is {tuning_frequency}.")


def count_infeasible_positions(filename, pos_y):
    """
    For a given row, count the positions that cannot contain beacons.

    First, determine for every sensor an interval of x-coordinates that are
    within its coverage (if there are any such x-coordinates). Then, loop
    through these intervals to get their union. Finally, correct for
    x-coordinates that actually do contain a beacon.
    """
    sensors = initialize_sensors(filename)
    intervals_x = []
    for s in sensors:
        interval_radius = s.radius - abs(s.pos_y - pos_y)
        if interval_radius >= 0:
            interval = (s.pos_x - interval_radius, s.pos_x + interval_radius)
            intervals_x.append(interval)
    intervals_x.sort(key=lambda i: i[0])

    nr_infeasible = 0
    if intervals_x:
        current_min = intervals_x[0][0]
        current_max = intervals_x[0][1]
        for idx in range(1, len(intervals_x)):
            if intervals_x[idx][0] > current_max + 1:
                nr_infeasible += current_max - current_min + 1
                current_min = intervals_x[idx][0]
                current_max = intervals_x[idx][1]
            else:
                current_max = max(current_max, intervals_x[idx][1])
        nr_infeasible += current_max - current_min + 1

    beacon_coordinates = set(s.beacon_x for s in sensors if s.beacon_y == pos_y)
    nr_infeasible -= len(beacon_coordinates)
    return nr_infeasible


def calculate_tuning_frequency(filename, range_x, range_y):
    """Get coordinates of distress beacon, and derive the tuning frequency."""
    sensors = initialize_sensors(filename)
    pos_x, pos_y = find_distress_beacon(sensors, range_x, range_y)
    return pos_x * X_MULTIPLIER + pos_y * Y_MULTIPLIER


def initialize_sensors(filename):
    """Read input file, and initialize the sensors."""
    sensor_lines = aoc.read_stripped_lines(filename)
    sensor_regex = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): "
        r"closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    sensors = []
    for line in sensor_lines:
        sensor_data = sensor_regex.search(line).groups()
        pos_x, pos_y, beacon_x, beacon_y = (int(x) for x in sensor_data)
        sensors.append(Sensor(pos_x, pos_y, beacon_x, beacon_y))
    return sensors


def find_distress_beacon(sensors, range_x, range_y):
    """
    In an area with only one feasible distress beacon location, find the beacon.

    The procedure uses the observation that for every sensor, the coverage area
    'starts' and 'ends' at a minimum and maximum Manhattan distance from the
    top-left corner of the search area. For a fixed top-left distance between
    this minimum and maximum, the positions in the coverage area of a sensor
    form an interval looking from bottom-left to top-right. Moreover, the
    distances from the start and end points of this interval to the bottom-left
    corner of the search area are the same for every top-left distance.

    One possibility is to check for every top-left distance whether, among all
    positions on the diagonal with that top-left distance, there exists one not
    covered by the sensors' intervals. That may be either because there is a gap
    between intervals or because the bottom-left-most or top-right-most position
    on the diagonal is not covered.

    Closer examination shows that it suffices to check only a selected number of
    top-left distances: those just before the coverage of a sensor starts and
    just after the coverage of a sensor ends, supplemented by those that include
    the bottom-left and top-right corner of the search area.

    NOTE: In the code below, top-left distance of position (x,y) is defined as
    x + y and bottom-left distance of position (x,y) is defined as x - y,
    irrespective of the actual positions of the top-left and bottom-left corner
    of the search area. The distance to those actual positions will differ by a
    constant that is identical for all positions.
    """
    sensors.sort(key=lambda s: s.min_bottom_left)
    top_left_distances = select_top_left_distances(sensors, range_x, range_y)
    top_left_idx = 0
    is_found = False

    while not is_found and top_left_idx < len(top_left_distances):
        top_left_distance = top_left_distances[top_left_idx]

        # Set the bottom-left-most and top-right-most position on diagonal:
        if top_left_distance <= range_x[0] + range_y[1]:
            min_bottom_left = 2 * range_x[0] - top_left_distance
        elif top_left_distance > range_x[0] + range_y[1]:
            min_bottom_left = top_left_distance - 2 * range_y[1]
        if top_left_distance <= range_y[0] + range_x[1]:
            max_bottom_left = top_left_distance - 2 * range_y[0]
        elif top_left_distance > range_y[0] + range_x[1]:
            max_bottom_left = 2 * range_x[1] - top_left_distance

        # Determine the sensors with coverage on diagonal:
        active_sensors = []
        for sensor in sensors:
            if sensor.min_top_left <= top_left_distance <= sensor.max_top_left:
                active_sensors.append(sensor)

        # Check whether bottom-left-most position on diagonal is covered:
        if active_sensors:
            current_min = active_sensors[0].min_bottom_left
            current_max = active_sensors[0].max_bottom_left
        if (not active_sensors) or (current_min > min_bottom_left):
            pos_x = (top_left_distance + min_bottom_left) // 2
            pos_y = (top_left_distance - min_bottom_left) // 2
            is_found = True
            break

        # Check whether coverage intervals of sensors are adjacent:
        # (Not all combinations of a top_left_distance and bottom_left_distance
        # corresponds with integer x and y coordinates; hence the parity tests.)
        for sensor_idx in range(1, len(active_sensors)):
            sensor = active_sensors[sensor_idx]
            if sensor.min_bottom_left <= current_max + 1:
                current_max = max(current_max, sensor.max_bottom_left)
            elif (top_left_distance + current_max + 1) % 2 == 0:
                pos_x = (top_left_distance + current_max + 1) // 2
                pos_y = (top_left_distance - current_max - 1) // 2
                is_found = True
                break
            elif sensor.min_bottom_left == current_max + 2:
                current_max = max(current_max, sensor.max_bottom_left)
            else:
                pos_x = (top_left_distance + current_max + 2) // 2
                pos_y = (top_left_distance - current_max - 2) // 2
                is_found = True
                break

        # Check whether top-right-most position on diagonal is covered:
        if not is_found and current_max <= max_bottom_left:
            pos_x = (top_left_distance + max_bottom_left) // 2
            pos_y = (top_left_distance - max_bottom_left) // 2
            is_found = True

        top_left_idx += 1
    return pos_x, pos_y


def select_top_left_distances(sensors, range_x, range_y):
    """Select top-left distances to be considered in distress beacon search."""
    potential_distances = []
    for sensor in sensors:
        potential_distances.append(sensor.min_top_left - 2)
        potential_distances.append(sensor.min_top_left - 1)
        potential_distances.append(sensor.max_top_left + 1)
        potential_distances.append(sensor.max_top_left + 2)
    potential_distances = set(potential_distances)

    top_left_distances = [range_x[0] + range_y[1], range_y[0] + range_x[1]]
    for distance in potential_distances:
        if range_x[0] + range_y[0] <= distance <= range_x[1] + range_y[1]:
            top_left_distances.append(distance)
    return top_left_distances


class Sensor:
    """Class to represent a sensor."""

    def __init__(self, pos_x, pos_y, beacon_x, beacon_y):
        """Create a sensor with a position and closest beacon position."""
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.beacon_x = beacon_x
        self.beacon_y = beacon_y
        # Derived metrics that facilitate beacon search:
        self.radius = abs(pos_x - beacon_x) + abs(pos_y - beacon_y)
        self.min_top_left = self.pos_x + self.pos_y - self.radius
        self.max_top_left = self.pos_x + self.pos_y + self.radius
        self.min_bottom_left = self.pos_x - self.pos_y - self.radius
        self.max_bottom_left = self.pos_x - self.pos_y + self.radius


if __name__ == "__main__":
    main()
