"""
Solution --- Day 16: Proboscidea Volcanium ---

To elminate paths that are trivially suboptimal, this solution first computes
shortest distances between all valves with a positive flow rate ('key valves').
Once this has been done, there is no longer any need to consider jammed valves;
a path is defined by a sequence of key valves to be opened. 

The resulting problem of choosing a path (part 1) or multiple non-overlapping
paths (part 2) to maximize the total pressure release is known in the scientific
literature as the (team) orienteering problem with decreasing profits (and is
also known by several other names). See, for example, the following references:

* E. Erkut and J. Zhang. The Maximum Collection Problem with Time-Dependent
Rewards. Naval Research Logistics, 43(5):749-763, 1996.
* H.M. Afsar and N. Labadie. Team Orienteering Problem with Decreasing Profits.
Electronic Notes in Discrete Mathematics, 41(5):285-293, 2013.
* Q. Yu, C. Cheng, N. Zhu. Robust Team Orienteering Problem with Decreasing
Profits. INFORMS Journal on Computing, 34(6):3215-3233, 2022.

The time limits in the problem description and the number of key valves in the
input file (15) allow to employ a rather straightforward exact solution approach
that would not scale well to larger instances: First, the solution uses dynamic
programming to generate all key-valve subsets that can be visited by a single
path within the time limit. (The number of such sets would be prohibitive for
larger instances.) Next, dynamic programming is used to solve the 'master
problem' of selecting disjoint sets to maximize the sum of pressure releases.
(This is a set-packing-like problem. Again, the number of states in the dynamic
programming formulation would be prohibitive, and other approaches would be more
promising, in larger instances.)

Note: to facilitate state transitions in the DP formulations, the key valves are
indexed by a power of 2, and key-valve sets are identified by an integer equal
to the sum of the powers of 2 corresponding with the key valves in the subset.
Hence, bitwise operators can be used to check whether sets are disjoint, to take
the union of sets, or to add a key valve to a set.
"""

from collections import defaultdict
import itertools
import re

import aoc_tools as aoc

INITIAL_VALVE_STR = "AA"


def main():
    filename = "input_16.txt"
    max_pressure_release = maximize_pressure_release(filename, 30, 1)
    print(f"Without elephant, the maximum release is {max_pressure_release}.")
    max_pressure_release = maximize_pressure_release(filename, 26, 2)
    print(f"With elephant, the maximum release is {max_pressure_release}.")


def maximize_pressure_release(filename, nr_minutes, nr_agents):
    """Generate all path sets, and compute the max total pressure release."""
    init_valve, key_valves, dist = initialize_network(filename)
    path_vals = evaluate_paths(init_valve, key_valves, dist, nr_minutes)
    return maximize_total(path_vals, nr_agents)


def initialize_network(filename):
    """Read file input, identify initial and key valves, compute distances."""
    valve_lines = aoc.read_stripped_lines(filename)
    valve_regex = re.compile(
        r"Valve ([A-Z]+) has flow rate=(\d+); "
        r"(tunnels lead to valves|tunnel leads to valve) (.*)"
    )

    # Create the (key) valve objects and identify the initial valve:
    key_index = 1
    valves, key_valves, neighbor_names = [], [], {}
    for line in valve_lines:
        valve_data = valve_regex.search(line).groups()
        if int(valve_data[1]) > 0:
            valve = KeyValve(valve_data[0], int(valve_data[1]), key_index)
            valves.append(valve)
            key_valves.append(valve)
            key_index <<= 1
        else:
            valve = Valve(valve_data[0])
            valves.append(valve)
        if valve_data[0] == INITIAL_VALVE_STR:
            init_valve = valve
        # Fill a temporary dictionary with strings of neighbor names:
        neighbor_names[valve] = valve_data[3].split(", ")

    # Generate a dictionary with neighbor sets, and use to compute distances:
    lookup = {v.name: v for v in valves}
    neighbor_sets = {v: {lookup[n] for n in neighbor_names[v]} for v in valves}
    dist = compute_distances(valves, neighbor_sets)
    return init_valve, key_valves, dist


def compute_distances(valves, neighbor_sets):
    """Compute valve distances using the Floyd-Warshall algorithm."""
    dist = {v: {v: 0} for v in valves}
    for v1, v2 in itertools.combinations(valves, 2):
        dist[v1][v2] = 1 if v2 in neighbor_sets[v1] else len(valves)
        dist[v2][v1] = dist[v1][v2]

    # Iteratively expand the set of possible intermediate valves:
    for v3 in valves:
        for v1, v2 in itertools.combinations(valves, 2):
            if dist[v1][v3] + dist[v3][v2] < dist[v1][v2]:
                dist[v1][v2] = dist[v1][v3] + dist[v3][v2]
                dist[v2][v1] = dist[v1][v2]
    return dist


def evaluate_paths(init_valve, key_valves, dist, nr_minutes):
    """
    Evaluate max pressure release for all single-path key-valve sets.

    Throughout the dynamic programming recursion, the state is defined by the
    set of open valves, a current position, and a time to go. The state is
    associated with a value, representing the maximum total pressure release.
    However, if there are two states whose sets of open valves and current
    positions are the same, and if one state has a lower or equal time to go
    and is associated with a lower or equal value than the other state, this
    state can be excluded from further examination without affecting the final
    max pressure release for any key-valve subset that can be visited along a
    single path. Hence, a pruning procedure is applied. Moreover, it could turn
    out that one single-valve key-valve set is a strict subset of another set
    but corresponds with a higher or equal max pressure release; that is, the
    latter set is dominated. Dominated sets are deleted once the dynamic
    programming recursion is complete.
    """
    cache = [defaultdict(dict) for _ in range(len(key_valves) + 1)]
    pathset_vals = defaultdict(int)
    bench = defaultdict(int)

    # Initialize the recursion:
    open_set, position, value = 0, init_valve, 0
    cache[0][open_set][position] = [(nr_minutes, value)]
    pathset_vals[open_set] = value
    bench[open_set] = -1  # arbitrary value to ensure empty set is not dominated
    dominated = set()

    # Iteratively consider larger sets, and add new sets:
    for n in range(len(key_valves)):
        for open_set in cache[n]:
            if pathset_vals[open_set] > bench[open_set]:
                bench_input = pathset_vals[open_set]
            else:
                bench_input = bench[open_set]
                dominated.add(open_set)

            for v in key_valves:
                if open_set & v.index:
                    continue
                new_open_set = open_set | v.index
                if bench_input > bench[new_open_set]:
                    bench[new_open_set] = bench_input

                new_times_values = []
                for position in cache[n][open_set]:
                    elapse = dist[position][v] + 1
                    for time_to_go, value in cache[n][open_set][position]:
                        if time_to_go <= elapse:
                            break
                        new_time_to_go = time_to_go - elapse
                        new_value = value + new_time_to_go * v.flow_rate
                        new_times_values.append((new_time_to_go, new_value))

                if new_times_values:
                    new_times_values = sort_and_prune(new_times_values)
                    local_max = new_times_values[-1][1]
                    cache[n + 1][new_open_set][v] = new_times_values
                    if local_max > pathset_vals[new_open_set]:
                        pathset_vals[new_open_set] = local_max

    # Delete dominated sets:
    for open_set in dominated:
        del pathset_vals[open_set]
    return pathset_vals


def sort_and_prune(times_values):
    """Sort pairs of times to go and values, and delete the dominated ones."""
    if len(times_values) <= 1:
        return times_values
    else:
        # Sort pairs of times to go and values to make times to go descending:
        times_values.sort(reverse=True)
        # After deleting domninated pairs, values should be ascending:
        pruned_list = [times_values[0]]
        idx_1 = 0
        for idx_2 in range(1, len(times_values)):
            if times_values[idx_2][1] > times_values[idx_1][1]:
                pruned_list.append(times_values[idx_2])
                idx_1 = idx_2
        return pruned_list


def maximize_total(pathset_vals, nr_agents):
    """Compute max total pressure release for (nr_agents) disjoint path sets."""
    if nr_agents == 1:
        return max(pathset_vals.values())
    elif nr_agents == 2:
        return pair_max_symmetric(pathset_vals)
    elif nr_agents > 2:
        combset_vals = update_combined_values(pathset_vals)
        for _ in range(nr_agents - 3):
            combset_vals = update_combined_values(pathset_vals, combset_vals)
        return pair_max_asymmetric(pathset_vals, combset_vals)


def update_combined_values(pathset_vals, combset_vals=None):
    """Update combined-path sets and values if one more path can be selected."""
    break_symmetry = combset_vals is None
    if break_symmetry:
        combset_vals = pathset_vals
    new_combset_vals = defaultdict(int)
    max_index = 1 << max(pathset_vals).bit_length()
    cache = set()

    def combine(key_index, open_set_1, open_set_2):
        """Assign indexed valve to the current path, next path(s), or none."""
        if break_symmetry:
            cache.add((key_index, open_set_1, open_set_2))
        if key_index > max_index:
            return

        union = open_set_1 | key_index | open_set_2
        new_open_set_1 = open_set_1 | key_index
        new_open_set_2 = open_set_2 | key_index
        new_key_index = key_index << 1

        # Assign to current path:
        if new_open_set_1 in pathset_vals:
            evaluate_combination(new_open_set_1, open_set_2, union)
            combine(new_key_index, new_open_set_1, open_set_2)
        # Assign to next path:
        if new_open_set_2 in pathset_vals:
            if (new_key_index, new_open_set_2, open_set_1) not in cache:
                evaluate_combination(open_set_1, new_open_set_2, union)
                combine(new_key_index, open_set_1, new_open_set_2)
        # Do not assign:
        combine(new_key_index, open_set_1, open_set_2)

    def evaluate_combination(open_set_1, open_set_2, union):
        """Evaluate combination of a current-path set and next-path(s) set."""
        value = pathset_vals[open_set_1] + combset_vals[open_set_2]
        if value > new_combset_vals[union]:
            new_combset_vals[union] = value

    key_index, open_set_1, open_set_2 = 1, 0, 0
    combine(key_index, open_set_1, open_set_2)
    return new_combset_vals


def pair_max_symmetric(pathset_vals):
    """Select a current-path set and a next-path set to maximize value sum."""
    slist = sorted(pathset_vals.items(), key=lambda x: x[1], reverse=True)
    max_value = 0
    for idx_1, (open_set_1, value_1) in enumerate(slist):
        lb = max_value - value_1
        for idx_2 in range(idx_1 + 1, len(slist)):
            open_set_2, value_2 = slist[idx_2]
            if value_2 <= lb:
                break
            elif not open_set_1 & open_set_2:
                max_value = value_1 + value_2
                break
    return max_value


def pair_max_asymmetric(pathset_vals, combset_vals):
    """Select a current-path set and a next-paths set to maximize value sum."""
    slist_1 = sorted(pathset_vals.items(), key=lambda x: x[1], reverse=True)
    slist_2 = sorted(combset_vals.items(), key=lambda x: x[1], reverse=True)
    max_value = 0
    for open_set_1, value_1 in slist_1:
        lb = max_value - value_1
        for open_set_2, value_2 in slist_2:
            if value_2 <= lb:
                break
            elif not open_set_1 & open_set_2:
                max_value = value_1 + value_2
                break
    return max_value


class Valve:
    """Class to represent a valve."""

    def __init__(self, name):
        """Create a valve, defined by its name."""
        self.name = name


class KeyValve(Valve):
    """Class to represent a valve with a positive flow rate."""

    def __init__(self, name, flow_rate, index):
        """Create a valve with a name and flow rate, identified by an index."""
        super().__init__(name)
        self.flow_rate = flow_rate
        self.index = index


if __name__ == "__main__":
    main()
