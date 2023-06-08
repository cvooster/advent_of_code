"""
Solution --- Day 22: Monkey Map ---

Simulates a path on the board either by wrapping around (part 1) or by walking
around a cube (part 2). In both cases, including part 1, this solution requires
the board to represent a cube net.
"""

import itertools
import math
import re

import aoc_tools as aoc

INITIAL_FACING = 3
INITIAL_TURN = "R"
MULTIPLIER_ROW = 1_000
MULTIPLIER_COL = 4
MULTIPLIER_FACING = 1


def main():
    filename_map = "input_22a.txt"
    filename_moves = "input_22b.txt"
    password = compute_password(filename_map, filename_moves, 1)
    print(f"The final password, wrapping around the board, is {password}.")
    password = compute_password(filename_map, filename_moves, 2)
    print(f"The final password, walking around the cube, is {password}.")


def compute_password(filename_map, filename_moves, part=2):
    """Compute the password from the final position and facing on the board."""    
    cube_net = read_map(filename_map)
    facets = fold_cube_net(cube_net)
    transitions = setup_transitions(facets, part)
    move_list = read_moves(filename_moves)
    row, col, facing = simulate_moves(move_list, facets, *transitions)
    return (
        MULTIPLIER_ROW * (row + 1)
        + MULTIPLIER_COL * (col + 1)
        + MULTIPLIER_FACING * facing
    )


def read_moves(filename_moves):
    """Read file input, and generate a list of one-move strings."""
    move_regex = re.compile(r"([LR]\d+)")
    move_string = INITIAL_TURN + aoc.read_stripped(filename_moves)
    return move_regex.findall(move_string)


def read_map(filename_map):
    """Read file input, and set the tiles for all cube net positions."""
    map_lines = aoc.read_stripped_lines(filename_map)

    # Determine the edge_length:
    surface_count = sum(line.count(".") + line.count("#") for line in map_lines)
    edge_length = math.sqrt(surface_count / 6)
    if not edge_length.is_integer():
        raise ValueError("The 2D map is not a cube net!")
    edge_length = int(edge_length)

    # Determine all positions (possibly with white space) in the input file:
    all_positions = []
    cube_net_max_y = len(map_lines) / edge_length
    if not cube_net_max_y.is_integer():
        raise ValueError("The 2D map is not a cube net!")
    cube_net_max_y = int(cube_net_max_y)

    for idx_y in range(cube_net_max_y):
        rows = range(idx_y * edge_length, (idx_y + 1) * edge_length)
        cube_net_max_x = min(len(map_lines[row]) for row in rows) / edge_length
        if not cube_net_max_x.is_integer():
            raise ValueError("The 2D map is not a cube net!")
        for idx_x in range(int(cube_net_max_x)):
            all_positions.append((idx_y, idx_x))

    # Check whether positions are tiled and, therefore, part of the cube net:
    cube_net = {}
    for idx_y, idx_x in all_positions:
        include = True
        is_wall = [[False] * edge_length for _ in range(edge_length)]
        for frow, fcol in itertools.product(range(edge_length), repeat=2):
            row = idx_y * edge_length + frow
            col = idx_x * edge_length + fcol
            if map_lines[row][col] == "#":
                is_wall[frow][fcol] = True
            elif map_lines[row][col] == " ":
                include = False
                break
        if include:
            cube_net[(idx_y, idx_x)] = is_wall
    return cube_net


def fold_cube_net(cube_net):
    """Fold a cube net and (arbitrarily) position it in a 3D grid."""
    # Arbitrarily set the bottom facet:
    facets = []
    cn_position, is_wall = cube_net.popitem()
    cornerpoints = ((0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0))
    facet = Facet(cn_position, is_wall, *cornerpoints)
    facets.append(facet)

    # Starting from this bottom facet, fold the rest of the cube net:
    fold_all_adjacent(cube_net, facets, cn_position, facet)

    # Perform one check that will be passed if the folded object is a cube:
    counts = {co: 0 for co in itertools.product(range(2), repeat=3)}
    for facet in facets:
        counts[facet.bl] += 1
        counts[facet.br] += 1
        counts[facet.tl] += 1
        counts[facet.tr] += 1
    if not all(counts[co] == 3 for co in itertools.product(range(2), repeat=3)):
        raise ValueError("The 2D map does not fold into a cube!")
    return facets


def fold_all_adjacent(cube_net, facets, current_cn_position, current_facet):
    """Fold facets adjacent to current one; cont. doing the same from there."""
    ccnp = current_cn_position
    cn_positions_methods = [
        ((ccnp[0] - 1, ccnp[1]), current_facet.fold_adjacent_up),
        ((ccnp[0] + 1, ccnp[1]), current_facet.fold_adjacent_down),
        ((ccnp[0], ccnp[1] + 1), current_facet.fold_adjacent_right),
        ((ccnp[0], ccnp[1] - 1), current_facet.fold_adjacent_left),
    ]
    for cn_position, fold_method in cn_positions_methods:
        if cn_position in cube_net:
            is_wall = cube_net.pop(cn_position)
            cornerpoints = fold_method()
            facet = Facet(cn_position, is_wall, *cornerpoints)
            facets.append(facet)
            fold_all_adjacent(cube_net, facets, cn_position, facet)


def setup_transitions(facets, part):
    """
    Set up mechanisms for how to continue when walking off the board.

    It is first established how the next facet and facing are determined, and
    whether the 'free' row or column (i.e., the one not implied by the facing at
    hich the current facet is left) is 'mirrored' to the next 'free' row or
    column. Next, functions are established to use this to compute the next row
    and column.
    """    
    if part == 1:
        f_transitions = setup_facet_transitions_p1(facets)
    elif part == 2:
        f_transitions = setup_facet_transitions_p2(facets)
    t_transitions = setup_tile_transitions(len(facets[0].is_wall))
    return f_transitions, t_transitions


def setup_facet_transitions_p1(facets):
    """
    Set next facet, facing, and mirroring for part 1.

    Note that the wrapping-around rule implies that facings are preserved and 
    there is no mirroring.
    """
    pos_facets = {f.cn_position: f for f in facets}
    f_transitions = {}  
    for facet_1 in facets:
        ccnp = facet_1.cn_position  # current cube net position

        # Facing 0: if cube net does not extend to the right, wrap around.
        if (ccnp[0], ccnp[1] + 1) in pos_facets:
            facet_2 = pos_facets[(ccnp[0], ccnp[1] + 1)]
        else:
            facet_2 = pos_facets[min(k for k in pos_facets if k[0] == ccnp[0])]
        f_transitions[(facet_1, 0)] = (facet_2, 0, False)
        # Facing 1: if cube net does not extend downward, wrap around.
        if (ccnp[0] + 1, ccnp[1]) in pos_facets:
            facet_2 = pos_facets[(ccnp[0] + 1, ccnp[1])]
        else:
            facet_2 = pos_facets[min(k for k in pos_facets if k[1] == ccnp[1])]
        f_transitions[(facet_1, 1)] = (facet_2, 1, False)
        # Facing 2: if cube net does not extend to the left, wrap around.
        if (ccnp[0], ccnp[1] - 1) in pos_facets:
            facet_2 = pos_facets[(ccnp[0], ccnp[1] - 1)]
        else:
            facet_2 = pos_facets[max(k for k in pos_facets if k[0] == ccnp[0])]
        f_transitions[(facet_1, 2)] = (facet_2, 2, False)
        # Facing 3: if cube net does not extend upward, wrap around.
        if (ccnp[0] - 1, ccnp[1]) in pos_facets:
            facet_2 = pos_facets[(ccnp[0] - 1, ccnp[1])]
        else:
            facet_2 = pos_facets[max(k for k in pos_facets if k[1] == ccnp[1])]
        f_transitions[(facet_1, 3)] = (facet_2, 3, False)
    return f_transitions


def setup_facet_transitions_p2(facets):
    """
    Set next facet, facing, and mirroring for part 2.

    Note that the walking-around-the-cube rule implies that facings can change,
    and there might be mirroring.
    """
    f_transitions = {}
    for facet_1, facet_2 in itertools.permutations(facets, 2):
        for edge in facet_1.exit:
            if edge in facet_2.entry:
                facing_1 = facet_1.exit[edge]
                facing_2 = facet_2.entry[edge]
                mirror = False
                f_transitions[(facet_1, facing_1)] = (facet_2, facing_2, mirror)
                break
            elif tuple(reversed(edge)) in facet_2.entry:
                facing_1 = facet_1.exit[edge]
                facing_2 = facet_2.entry[tuple(reversed(edge))]
                mirror = True
                f_transitions[(facet_1, facing_1)] = (facet_2, facing_2, mirror)
                break
    return f_transitions


def setup_tile_transitions(edge_length):
    """
    Set up functions to map the current facet row and column to the next ones.

    This is a wrapper to create such functions for every combination of a
    current facing, a next facing, and mirroring. The functions are stored in
    one dictionary.
    """
    t_transitions = {}
    for facing_1, facing_2 in itertools.product(range(4), repeat=2):
        fu, mir_fu = create_tile_transition_fu(facing_1, facing_2, edge_length)
        t_transitions[(facing_1, facing_2, False)] = fu
        t_transitions[(facing_1, facing_2, True)] = mir_fu
    return t_transitions


def create_tile_transition_fu(facing_1, facing_2, edge_length):
    """Create a row-and-column transition function within a set scope."""
    # Function to obtain relevant exit row or column:
    if facing_1 == 0 or facing_1 == 2:
        exfu = lambda frow, fcol: 1 * frow + 0 * fcol
    elif facing_1 == 1 or facing_1 == 3:
        exfu = lambda frow, fcol: 0 * frow + 1 * fcol

    # Function to obtain entry row and column from exit information:
    if facing_2 == 0:
        enfu = lambda var: (var, 0)
    elif facing_2 == 1:
        enfu = lambda var: (0, var)
    elif facing_2 == 2:
        enfu = lambda var: (var, edge_length - 1)
    elif facing_2 == 3:
        enfu = lambda var: (edge_length - 1, var)

    # Composite functions without and with mirroring:
    fu = lambda frow, fcol: enfu(exfu(frow, fcol))
    mir_fu = lambda frow, fcol: enfu(edge_length - 1 - exfu(frow, fcol))
    return fu, mir_fu


def simulate_moves(move_list, facets, f_transitions, t_transitions):
    """
    Simulate the path, and obtain the final row, column, and facing. 
    
    Throughout the execution of this path, the state is given by the current
    facet, the current row and column on the facet, and the current facing. Only
    after reaching the final position, the row and column with respect to the
    complete board are determined.
    """
    edge_length = len(facets[0].is_wall)

    # Set initial position:
    top_row_facets = [f for f in facets if f.cn_position[0] == 0]
    top_row_facets.sort(key=lambda f: f.cn_position[1])
    for i, facet in enumerate(top_row_facets):        
        try:
            fcol = facet.is_wall[0].index(False)
        except ValueError:
            if i < len(top_row_facets) - 1:
                continue
            else:
                raise ValueError("There is no open tile on the top row!")
        break
    frow = 0
    facing = INITIAL_FACING

    # Execute moves:
    for move in move_list:
        if move[0] == "L":
            facing = (facing - 1) % 4
        elif move[0] == "R":
            facing = (facing + 1) % 4

        for _ in range(int(move[1:])):
            if facing == 0:
                if fcol < edge_length - 1:
                    if not facet.is_wall[frow][fcol + 1]:
                        fcol += 1
                    else:
                        break
                elif fcol == edge_length - 1:
                    en_facet, en_facing, mirror = f_transitions[(facet, facing)]
                    k = (facing, en_facing, mirror)
                    en_frow, en_fcol = t_transitions[k](frow, fcol)
                    if not en_facet.is_wall[en_frow][en_fcol]:
                        facet = en_facet
                        facing = en_facing
                        frow = en_frow
                        fcol = en_fcol
                    else:
                        break
            elif facing == 1:
                if frow < edge_length - 1:
                    if not facet.is_wall[frow + 1][fcol]:
                        frow += 1
                    else:
                        break
                elif frow == edge_length - 1:
                    en_facet, en_facing, mirror = f_transitions[(facet, facing)]
                    k = (facing, en_facing, mirror)
                    en_frow, en_fcol = t_transitions[k](frow, fcol)
                    if not en_facet.is_wall[en_frow][en_fcol]:
                        facet = en_facet
                        facing = en_facing
                        frow = en_frow
                        fcol = en_fcol
                    else:
                        break
            elif facing == 2:
                if fcol > 0:
                    if not facet.is_wall[frow][fcol - 1]:
                        fcol -= 1
                    else:
                        break
                elif fcol == 0:
                    en_facet, en_facing, mirror = f_transitions[(facet, facing)]
                    k = (facing, en_facing, mirror)
                    en_frow, en_fcol = t_transitions[k](frow, fcol)
                    if not en_facet.is_wall[en_frow][en_fcol]:
                        facet = en_facet
                        facing = en_facing
                        frow = en_frow
                        fcol = en_fcol
                    else:
                        break
            elif facing == 3:
                if frow > 0:
                    if not facet.is_wall[frow - 1][fcol]:
                        frow -= 1
                    else:
                        break
                elif frow == 0:
                    en_facet, en_facing, mirror = f_transitions[(facet, facing)]
                    k = (facing, en_facing, mirror)
                    en_frow, en_fcol = t_transitions[k](frow, fcol)
                    if not en_facet.is_wall[en_frow][en_fcol]:
                        facet = en_facet
                        facing = en_facing
                        frow = en_frow
                        fcol = en_fcol
                    else:
                        break

    # Obtain row and column with respect to the complete board:
    row = facet.cn_position[0] * edge_length + frow
    col = facet.cn_position[1] * edge_length + fcol
    return row, col, facing


class Facet:
    """Class to represent a cube facet."""

    def __init__(self, cn_position, is_wall, bl, br, tl, tr):
        """
        Create a facet with tiles, positioned in a 3D grid.

        The facet is defined by its cube net position, tiles, and cornerpoints
        in the 3D grid. Other metrics are derived to facilitate setting the
        transition mechanism and to facilitate the folding process.
        """
        self.cn_position = cn_position
        self.is_wall = is_wall
        self.bl = bl  # (x, y, z) bottom-left
        self.br = br  # (x, y, z) bottom-right
        self.tl = tl  # (x, y, z) top-left
        self.tr = tr  # (x, y, z) top-right

        # Derived 'dimensions' of this facet (False if constant in dimension):
        self.dim = [self.bl[i] != self.tr[i] for i in range(3)]

        # Facing when entering or exiting at an edge:
        self.entry = {(tl, bl): 0, (tl, tr): 1, (tr, br): 2, (bl, br): 3}
        self.exit = {(tr, br): 0, (bl, br): 1, (tl, bl): 2, (tl, tr): 3}

    def fold_adjacent_left(self):
        """Get cornerpoints for facet left-adjacent in the cube net."""
        br = self.bl
        tr = self.tl
        bl = tuple(br[i] if self.dim[i] else (br[i] + 1) % 2 for i in range(3))
        tl = tuple(tr[i] if self.dim[i] else (tr[i] + 1) % 2 for i in range(3))
        return (bl, br, tl, tr)

    def fold_adjacent_right(self):
        """Get cornerpoints for facet right-adjacent in the cube net."""
        bl = self.br
        tl = self.tr
        br = tuple(bl[i] if self.dim[i] else (bl[i] + 1) % 2 for i in range(3))
        tr = tuple(tl[i] if self.dim[i] else (tl[i] + 1) % 2 for i in range(3))
        return (bl, br, tl, tr)

    def fold_adjacent_up(self):
        """Get cornerpoints for facet up-adjacent in the cube net."""
        bl = self.tl
        br = self.tr
        tl = tuple(bl[i] if self.dim[i] else (bl[i] + 1) % 2 for i in range(3))
        tr = tuple(br[i] if self.dim[i] else (br[i] + 1) % 2 for i in range(3))
        return (bl, br, tl, tr)

    def fold_adjacent_down(self):
        """Get cornerpoints for facet down-adjacent in the cube net."""
        tl = self.bl
        tr = self.br
        bl = tuple(tl[i] if self.dim[i] else (tl[i] + 1) % 2 for i in range(3))
        br = tuple(tr[i] if self.dim[i] else (tr[i] + 1) % 2 for i in range(3))
        return (bl, br, tl, tr)


if __name__ == "__main__":
    main()
