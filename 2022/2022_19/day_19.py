"""
Solution --- Day 19: Not Enough Minerals ---

This problem is solved in a branch-and-bound style. Every node is a combination
of a state (defined by resource levels and robot levels for ore, clay, and
obsidian) and the remaining horizon length. For every node, a maximum value to
arrive in the node is computed, representing the total number of geodes opened
over the entire horizon by the geode-cracking robots built up to that time. This
serves as a lower bound on the objective value that can be reached from the
node. An upper bound is obtained by supposing that a geode-cracking robot will
be built in every minute of the remaining horizon.

The largest remaining horizon length is used as the main criterion for selecting
the next node to branch on. This ensures the maximum value of a node is known
when it is branched on. In principle, branching creates a successor node for
every possible next robot type to build, as long as that next robot type will be
ready before the end of the horizon.

Several enhancements are used to accelerate the algorithm:

(1) In creating successor nodes, only robot types are considered that have added
value. There is no value in building a geode-cracking robot when there is 1
minute left, an ore-collecting or obsidian-collecting robot if there are 2
minutes or less left, or a clay-collecting robot if there are 3 minutes or less
left. Moreover, note that the definition of a blueprint implies for every
resource a maximum amount to spend per minute. Therefore, if the current
resource and robot levels for a type are sufficient to spend the maximum of
that type from the next minute onward until the end of the horizon, there is no
point in building an extra robot of that type in the current minute. Finally,
note that if an obsidian-collecting robot has no added value, then it follows
that a clay-collecting robot has no added value either!

(2) If there is no added value in ore-collecting and obsidian-collecting robots,
instead of creating a successor node by building one geode-cracking robot, the
algorithm immediately proceeds forward in time to the end of the horizon. The
successor node is the one reached after building (as early) as many
geode-cracking robots as possible along the way.

(3) To limit the generation of states that are not fundamentally different, a
postprocessing procedure is applied to successor nodes. If the current resource
and robot levels of a type are sufficient to spend the maximum rate from the
current minute onward until the end of the horizon, the resource and robot
levels are set to some default values (that are also sufficient).

(4) After all nodes with a given remaining horizon length have been generated,
and before they are selected for branching, a monotonicity property is used to
prune nodes: if in one state the resource and robot levels are higher than or
equal to those in another state, and the remaining horizon length is the same,
then the maximum value-to-go will be higher or equal.
"""

import math
import re

import aoc_tools as aoc


def main():
    filename = "input_19.txt"
    _, quality_level_sum = summarize_evaluations(filename, 24)
    print(f"The quality levels of blueprints add up to {quality_level_sum}.")
    max_geode_multiple, _ = summarize_evaluations(filename, 32, 3)
    print(f"The three geode maxima multiply to {max_geode_multiple}.")


def summarize_evaluations(filename, nr_minutes, max_blueprints=None):
    """Generate summary statistics of (a number of) evaluated blueprints."""
    blueprints = set_blueprints(filename, max_blueprints)
    max_geodes = [evaluate_blueprint(bp, nr_minutes) for bp in blueprints]
    quality_levels = [mg * bp.id_num for mg, bp in zip(max_geodes, blueprints)]
    return math.prod(max_geodes), sum(quality_levels)


def set_blueprints(filename, max_blueprints=None):
    """Read file input, and initialize (a number of) blueprints."""
    blueprint_lines = aoc.read_stripped_lines(filename)
    if max_blueprints is not None and len(blueprint_lines) > max_blueprints:
        blueprint_lines = blueprint_lines[:max_blueprints]
    blueprint_regex = re.compile(
        r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot "
        r"costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. "
        r"Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
    blueprints = []
    for line in blueprint_lines:
        blueprint_data = [int(x) for x in blueprint_regex.search(line).groups()]
        cost = {"ore": {}, "cla": {}, "obs": {}, "geo": {}}
        cost["ore"]["ore"] = blueprint_data[1]
        cost["cla"]["ore"] = blueprint_data[2]
        cost["obs"]["ore"] = blueprint_data[3]
        cost["obs"]["cla"] = blueprint_data[4]
        cost["geo"]["ore"] = blueprint_data[5]
        cost["geo"]["obs"] = blueprint_data[6]
        blueprints.append(Blueprint(blueprint_data[0], cost))
    return blueprints


def evaluate_blueprint(bp, nr_minutes):
    """For a given blueprint, compute the maximum number of geodes to open."""
    nodes = [{} for _ in range(nr_minutes + 1)]
    initial_state = State([0, 0, 0], [1, 0, 0])
    initial_value = 0
    nodes[nr_minutes][initial_state] = initial_value
    max_value = initial_value

    # Branch until there is 1 minute left:
    for time_to_go in range(nr_minutes, 1, -1):
        node_list = list(nodes[time_to_go].items())
        node_list = prune_using_monotonicity(node_list)

        for state, value in node_list:
            new_entries = generate_successors(bp, state, value, time_to_go)
            for new_s, new_v, new_ttg in new_entries:
                # Check whether the node improves on the best LB:
                if new_v > max_value:
                    nodes[new_ttg][new_s] = new_v
                    max_value = new_v
                # Check whether the node could improve on the best LB:
                elif new_v + new_ttg * (new_ttg - 1) / 2 > max_value:
                    # The node might already exist with a higher value:
                    current_v = nodes[new_ttg].get(new_s, 0)
                    nodes[new_ttg][new_s] = max(current_v, new_v)
    return max_value


def prune_using_monotonicity(node_list):
    """
    Prune monotonicity-dominated state-value tuples.

    If the value of one state is lower than or equal to that of another state,
    and so are all resource and robot levels (hence, the maximum value-to-go is
    also lower or equal), that state-value pair can be pruned.
    """
    if len(node_list) <= 1:
        return node_list
    else:
        to_prune = [False] * len(node_list)
        for idx_1 in range(len(node_list)):
            if to_prune[idx_1]:
                continue
            state_1, value_1 = node_list[idx_1]
            for idx_2 in range(idx_1 + 1, len(node_list)):
                if to_prune[idx_2]:
                    continue
                state_2, value_2 = node_list[idx_2]
                # Compare values and states:
                if value_2 <= value_1 and state_2 <= state_1:
                    to_prune[idx_2] = True
                elif value_1 <= value_2 and state_1 <= state_2:
                    to_prune[idx_1] = True
                    break
        pruned_list = [n for n, tp in zip(node_list, to_prune) if not tp]
        return pruned_list


def generate_successors(bp, state, value, time_to_go):
    """
    Given a current node, create its successor nodes by building robot types.

    Note that robot types are only built when they have added value, and it
    will also be checked whether building a robot type is feasible in the
    remainder of the horizon. The algorithm deviates and proceeds immediately to
    the end of the horizon if there is no added value in ore-collecting and
    obdisian-collecting robots.
    """
    resources, robots = state.resources, state.robots

    # Check whether robot types have added value. In particular, check whether
    # it is possible to spend the maximum obsidian/clay/ore rate from the next
    # minute onward:
    thres_obs = (bp.cost["geo"]["obs"] - robots[2]) * (time_to_go - 2)
    thres_cla = (bp.cost["obs"]["cla"] - robots[1]) * (time_to_go - 3)
    thres_or1 = (bp.cost["geo"]["ore"] - robots[0]) * (time_to_go - 2)
    thres_or2 = (bp.cost["obs"]["ore"] - robots[0]) * (time_to_go - 3)
    thres_or3 = (bp.cost["cla"]["ore"] - robots[0]) * (time_to_go - 4)

    valuable_obs = time_to_go >= 3 and resources[2] < thres_obs
    valuable_cla = time_to_go >= 4 and resources[1] < thres_cla and valuable_obs

    thres_ore = thres_or1
    if valuable_obs:
        thres_ore = max(thres_ore, thres_or2)
        if valuable_cla:
            thres_ore = max(thres_ore, thres_or3)
    valuable_ore = time_to_go >= 3 and resources[0] < thres_ore

    # If there is no value in obsidian-collecting and ore-collecting robots,
    # immediately proceed to the end of the horizon:
    if not valuable_obs and not valuable_ore:
        for time_to_go_ in range(time_to_go, 1, -1):
            does_suffice_ore = resources[0] >= bp.cost["geo"]["ore"]
            does_suffice_obs = resources[2] >= bp.cost["geo"]["obs"]
            if does_suffice_ore and does_suffice_obs:
                resources[0] -= bp.cost["geo"]["ore"]
                resources[2] -= bp.cost["geo"]["obs"]
                value += time_to_go_ - 1
            for i in range(3):
                resources[i] += robots[i]
        return [(State(resources, robots), value, 1)]

    # Try to build each of the considered robot types. Note that the conditions
    # robots[1] > 0 and robots[2] > 0 ensure that an obsdian-collecting robot
    # and a geode-cracking robot, respectively, can be built after a long enough
    # wait:
    successors = []
    if valuable_ore:
        st = build_ore_robot(bp, resources[:], robots[:], time_to_go)
        if st is not None:
            successors.append((st[0], value, st[1]))
    if valuable_cla:
        st = build_cla_robot(bp, resources[:], robots[:], time_to_go)
        if st is not None:
            successors.append((st[0], value, st[1]))
    if valuable_obs and robots[1] > 0:
        st = build_obs_robot(bp, resources[:], robots[:], time_to_go)
        if st is not None:
            successors.append((st[0], value, st[1]))
    if robots[2] > 0:
        st = build_geo_robot(bp, resources[:], robots[:], time_to_go)
        if st is not None:
            successors.append((st[0], value + st[1], st[1]))
    return successors


def build_ore_robot(bp, resources, robots, time_to_go):
    """Compute the state and time to go after building ore robot."""
    wait = max(math.ceil((bp.cost["ore"]["ore"] - resources[0]) / robots[0]), 0)
    if wait >= time_to_go - 2:
        return None
    resources[0] += (wait + 1) * robots[0] - bp.cost["ore"]["ore"]
    resources[1] += (wait + 1) * robots[1]
    resources[2] += (wait + 1) * robots[2]
    robots[0] += 1
    time_to_go -= wait + 1
    resources, robots = postprocess_state(bp, resources, robots, time_to_go)
    return State(resources, robots), time_to_go


def build_cla_robot(bp, resources, robots, time_to_go):
    """Compute the state and time to go after building clay robot."""
    wait = max(math.ceil((bp.cost["cla"]["ore"] - resources[0]) / robots[0]), 0)
    if wait >= time_to_go - 3:
        return None
    resources[0] += (wait + 1) * robots[0] - bp.cost["cla"]["ore"]
    resources[1] += (wait + 1) * robots[1]
    resources[2] += (wait + 1) * robots[2]
    robots[1] += 1
    time_to_go -= wait + 1
    resources, robots = postprocess_state(bp, resources, robots, time_to_go)
    return State(resources, robots), time_to_go


def build_obs_robot(bp, resources, robots, time_to_go):
    """Compute the state and time to go after building obsidian robot."""
    wait_1 = math.ceil((bp.cost["obs"]["ore"] - resources[0]) / robots[0])
    wait_2 = math.ceil((bp.cost["obs"]["cla"] - resources[1]) / robots[1])
    wait = max(wait_1, wait_2, 0)
    if wait >= time_to_go - 2:
        return None
    resources[0] += (wait + 1) * robots[0] - bp.cost["obs"]["ore"]
    resources[1] += (wait + 1) * robots[1] - bp.cost["obs"]["cla"]
    resources[2] += (wait + 1) * robots[2]
    robots[2] += 1
    time_to_go -= wait + 1
    resources, robots = postprocess_state(bp, resources, robots, time_to_go)
    return State(resources, robots), time_to_go


def build_geo_robot(bp, resources, robots, time_to_go):
    """Generate state and remaining time after building geode robot."""
    wait_1 = math.ceil((bp.cost["geo"]["ore"] - resources[0]) / robots[0])
    wait_2 = math.ceil((bp.cost["geo"]["obs"] - resources[2]) / robots[2])
    wait = max(wait_1, wait_2, 0)
    if wait >= time_to_go - 1:
        return None
    resources[0] += (wait + 1) * robots[0] - bp.cost["geo"]["ore"]
    resources[1] += (wait + 1) * robots[1]
    resources[2] += (wait + 1) * robots[2] - bp.cost["geo"]["obs"]
    time_to_go -= wait + 1
    resources, robots = postprocess_state(bp, resources, robots, time_to_go)
    return State(resources, robots), time_to_go


def postprocess_state(bp, resources, robots, time_to_go):
    """
    Apply a postprocessing procedure to the generated successor node.

    Check for all types whether resource and robot levels are sufficient to
    spend the maximum rate until the end of the horizon. If so, set resource and
    robot levels to default values (that are also sufficient).
    """
    mx_obs = bp.cost["geo"]["obs"]
    thres_obs = mx_obs * (time_to_go - 1) - robots[2] * (time_to_go - 2)
    if resources[2] >= thres_obs:
        resources[2] = mx_obs * (time_to_go - 1)
        robots[2] = mx_obs

    mx_cla = bp.cost["obs"]["cla"]
    thres_cla = mx_cla * (time_to_go - 2) - robots[1] * (time_to_go - 3)
    if resources[2] >= thres_obs or resources[1] >= thres_cla:
        resources[1] = mx_cla * (time_to_go - 2)
        robots[1] = mx_cla

    mxs_ore = {k: bp.cost[k]["ore"] for k in ("cla", "obs", "geo")}
    thres_or1 = mxs_ore["geo"] * (time_to_go - 1) - robots[0] * (time_to_go - 2)
    thres_or2 = mxs_ore["obs"] * (time_to_go - 2) - robots[0] * (time_to_go - 3)
    thres_or3 = mxs_ore["cla"] * (time_to_go - 3) - robots[0] * (time_to_go - 4)

    thres_ore = thres_or1
    if resources[2] < thres_obs:
        thres_ore = max(thres_ore, thres_or2)
        if resources[1] < thres_cla:
            thres_ore = max(thres_ore, thres_or3)

    if resources[0] >= thres_ore:
        resources[0] = max(mxs_ore.values()) * (time_to_go - 1)
        robots[0] = max(mxs_ore.values())
    return resources, robots


class Blueprint:
    """Class to represent a blueprint for the robot factory."""

    def __init__(self, id_num, cost):
        """Create a blueprint, defined by an id and a cost dictionary."""
        self.id_num = id_num
        self.cost = cost


class State:
    """Class to represent a state in the branch-and-bound algorithm."""

    def __init__(self, resources, robots):
        """Create a state defined by (non-geode) resource and robot levels."""
        self.resources = resources
        self.robots = robots

    def __le__(self, other):
        """Equip this class with the <= operator."""
        return all(
            self.resources[i] <= other.resources[i] for i in range(3)
        ) and all(self.robots[i] <= other.robots[i] for i in range(3))


if __name__ == "__main__":
    main()
