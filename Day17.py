from aocd import data
import itertools


def make_jet_pattern_generator(raw_data):
    """
    turns the raw input into a generator that yields the jet pattern in the cave
    :param raw_data: raw puzzle input
    :return: generator that yields the jet pattern in an infinite cycle
    """
    return itertools.cycle(raw_data)


class FallingRock:
    def __init__(self, name, coord_set):
        """
        crates a new falling rock object
        :param name: name
        :param left_edge_coord: left-most point.  If there are multiple, the one that's the lowest
        :param bottom_coord: lowest point, if multiple the left-most point
        :param coord_set: set of coordinates in the rock shape
        """
        self.name = name
        self.coord_set = coord_set


def make_rock_generator():
    """
    creates an infinite generator that returns the four rock objects
    :return: generator
    """
    # create the five rock types
    rock_type_ls = [
        ('-',
         {
             (0, 0),
             (1, 0),
             (2, 0),
             (3, 0),
         }
         ),
        ('+',

         {
             (1, 0),
             (0, 1),
             (1, 1),
             (2, 1),
             (1, 2),
         }
         ),
        ('L',

         {
             (0, 0),
             (1, 0),
             (2, 0),
             (2, 1),
             (2, 2),
         }
         ),
        ('I',

         {
             (0, 0),
             (0, 1),
             (0, 2),
             (0, 3),
         }
         ),
        ('.',

         {
             (0, 0),
             (1, 0),
             (0, 1),
             (1, 1),
         }
         ),
    ]
    rock_type_gen = itertools.cycle(rock_type_ls)
    new_rock = (FallingRock(rock_type[0], rock_type[1]) for rock_type in rock_type_gen)
    return new_rock


def draw_chamber(curr_rock, rock_nodes):
    """
    visualization of the chamber state
    :param curr_rock: object of the current rock
    :param rock_nodes: list of the top of the settled rocks
    :return: list of lists to print
    """

    highest_y = max(
        [
            max([x[1] for x in rock_nodes]),
            max([x[1] for x in curr_rock.coord_set])
        ]
    )

    lowest_y = min(
        [
            min([x[1] for x in rock_nodes]),
            min([x[1] for x in curr_rock.coord_set])
        ]
    )
    if lowest_y == -1:
        chamber_ls = ['-------']
        lowest_y = 0
    else:
        chamber_ls = []

    for curr_y in range(lowest_y, highest_y + 1):
        y_ls = []
        for curr_x in range(7):
            if (curr_x, curr_y) in rock_nodes:
                y_ls.append('#')
            elif (curr_x, curr_y) in curr_rock.coord_set:
                y_ls.append('@')
            else:
                y_ls.append('.')
        chamber_ls.insert(0, ''.join(y_ls))
    return chamber_ls


class UnknownPatternError(Exception):
    pass


def tuple_abs_diff(tuple1, tuple2):
    """
    calculates the differences between a pair of tuples
    :param tuple1:
    :param tuple2:
    :return: the absolute difference

    >>> tuple_abs_diff((1,1),(1,1))
    (0, 0)

    >>> tuple_abs_diff((2,2),(1,1))
    (1, 1)

    >>> tuple_abs_diff((1,1),(2,2))
    (1, 1)

    >>> tuple_abs_diff((3,4),(2,1))
    (1, 3)
    """

    return (abs(tuple1[0] - tuple2[0]), abs(tuple1[1] - tuple2[1]))


def find_next_node(curr_node, rock_nodes, roof_ls, path_ls):
    """
    finds the next node in top layer
    :param path_ls: path so far
    :param curr_node: node to move from
    :param rock_nodes: list of coordinates defined as rocks
    :param roof_ls: list of coordinates that are the highest nodes in each column

    >>> find_next_node((0,3),{(0, -1), (0, 3), (1, -1), (1, 3), (2, -1), (2, 0), (2, 2), (2, 3), (2, 4), (2, 5), (3, -1), (3, 1), (3, 3), (4, -1), (4, 0), (4, 2), (5, -1), (5, 0), (6, -1)}, [3, 3, 5, 3, 2, 0, -1], [(0,3)])
    (1, 3)

    >>> find_next_node((1,3),{(0, -1), (0, 3), (1, -1), (1, 3), (2, -1), (2, 0), (2, 2), (2, 3), (2, 4), (2, 5), (3, -1), (3, 1), (3, 3), (4, -1), (4, 0), (4, 2), (5, -1), (5, 0), (6, -1)}, [3, 3, 5, 3, 2, 0, -1], [(0,3), (1, 3)])
    (2, 4)

    >>> find_next_node((2,4),{(0, -1), (0, 3), (1, -1), (1, 3), (2, -1), (2, 0), (2, 2), (2, 3), (2, 4), (2, 5), (3, -1), (3, 1), (3, 3), (4, -1), (4, 0), (4, 2), (5, -1), (5, 0), (6, -1)}, [3, 3, 5, 3, 2, 0, -1], [(0, 3), (1, 3), (2, 4), (2, 5), (2, 4)])
    (3, 3)

    >>> find_next_node((3,1),{(0, -1), (0, 3), (1, -1), (1, 3), (2, -1), (2, 0), (2, 2), (2, 3), (2, 4), (2, 5), (3, -1), (3, 1), (3, 3), (4, -1), (4, 0), (4, 2), (5, -1), (5, 0), (6, -1)}, [3, 3, 5, 3, 2, 0, -1], [(0, 3), (1, 3), (2, 4), (2, 5), (2, 4), (3, 3), (4, 2), (3, 1)])
    (4, 0)
    """
    curr_x, curr_y = curr_node
    next_roof_node = (curr_x + 1, roof_ls[curr_x + 1])
    if (roof_ls[curr_x] == curr_y) and (tuple_abs_diff(curr_node, next_roof_node) in {
        (1, 0),
        (1, 1),
    }):  # node is roof node and touches next roof node
        return next_roof_node

    else:
        # can you move to a roof node?
        next_node_gen = ((x[0], x[1]) for x in [
            (curr_x - 1, roof_ls[curr_x - 1]),
            (curr_x, roof_ls[curr_x]),
            (curr_x + 1, roof_ls[curr_x + 1]),

        ]
                         )
        for next_node in next_node_gen:
            if (next_node not in path_ls) and (next_node in rock_nodes) and (
                    tuple_abs_diff(curr_node, next_roof_node) in {(1, 0), (1, 1)}):
                return next_node

        # try different coordinates to find next connected node
        next_node_gen = ((x[0], x[1]) for x in [
            (curr_x - 1, curr_y),
            (curr_x - 1, curr_y + 1),
            (curr_x, curr_y + 1),
            (curr_x + 1, curr_y + 1),
            (curr_x + 1, curr_y),
            (curr_x + 1, curr_y - 1),
            (curr_x, curr_y - 1),
        ]
                         )
        next_node = next(next_node_gen)
        while ((next_node not in rock_nodes) or (
                next_node == path_ls[-2] if len(path_ls) > 1 else False)) or (  # prevent flip flopping
                roof_ls[next_node[0]] == next_node[1]):  # not a roof node
            try:
                next_node = next(next_node_gen)
            except StopIteration:  # run out of nodes
                return path_ls[-2]  # backtrack
        return next_node


def find_top_layer(rock_nodes, roof_ls, start_node):
    """
    defines the highest path from the left to right wall
    :param rock_nodes: list of coordinates defined as rocks
    :param path_ls: path so far
    :return: path_ls
    >>> find_top_layer({(0, -1), (0, 3), (1, -1), (1, 3), (2, -1), (2, 0), (2, 2), (2, 3), (2, 4), (2, 5), (3, -1), (3, 1), (3, 3), (4, -1), (4, 0), (4, 2), (5, -1), (5, 0), (6, -1)}, [3, 3, 5, 3, 2, 0, -1], (0,3))
    [(0, 3), (1, 3), (2, 4), (2, 5), (2, 4), (3, 3), (4, 2), (3, 1), (4, 0), (5, 0), (6, -1)]

    >>> find_top_layer({(0, -1), (0, 3), (1, -1), (1, 3), (2, -1), (2, 0), (2, 2), (2, 3), (2, 4), (2, 5), (3, -1), (3, 1), (3, 3), (4, -1), (4, 0), (4, 2), (5, -1), (5, 0), (6, -1)}, [-1, -1, 2, 3, 2, 0, -1], (0,-1))
    [(0, -1), (1, -1), (2, 0), (3, 1), (2, 2), (3, 3), (4, 2), (3, 1), (4, 0), (5, 0), (6, -1)]
    """
    curr_node = start_node
    path_ls = [curr_node]
    while curr_node != (6, roof_ls[-1]):
        curr_node = find_next_node(curr_node, rock_nodes, roof_ls, path_ls)
        path_ls.append(curr_node)
    return path_ls


def analyze_cycle(curr_step, cycle_nodes, cycle_rock_nodes_ls, fingerprint_ls, fingerprint_zero_cycle_index,
                  num_full_cycles, cycle_height_ls, top_point, step_height_ls, cycle_length, num_rocks, total_height):
    """
    detects cyclic behaviour in the node pattern
    :param total_height: total height of fully modeled stack
    :param num_rocks: total number of rocks to drop (steps)
    :param cycle_length: length of the cycle
    :param step_height_ls: height of the stones at each step of the cycle
    :param top_point: height of the stack.
    :param cycle_height_ls: height of stones at each full_cycle
    :param curr_step: current cycle
    :param cycle_nodes: nodes in the current cycle
    :param cycle_rock_nodes_ls: nodes in the cycles so far
    :param fingerprint_ls: nodes defining the current potential cycle
    :param fingerprint_zero_cycle_index: index of cycle_rock_nodes_ls that corresponds to index 0 of fingerprint_ls
    :param num_full_cycles: number of full cycles detected so far.
    :return: fingerprint_ls, fingerprint_zero_cycle_index, num_full_cycles, step_height_ls, cycle_length
    """

    matching_index = cycle_rock_nodes_ls.index(cycle_nodes)
    if num_full_cycles == 0:  # full cycle not defined
        if fingerprint_ls:  # if there's an active list
            if matching_index == fingerprint_zero_cycle_index:
                cycle_length = len(fingerprint_ls)
                # print(f"full cycle complete, cycle is {cycle_length} steps long")
                num_full_cycles += 1
                cycle_height_ls.append(top_point)
            elif fingerprint_zero_cycle_index + len(fingerprint_ls) == matching_index:  # cycle continues
                fingerprint_ls.append(cycle_nodes)
                step_height_ls.append(top_point)
                # print(f"\ncurr cycle:{curr_step}\nnodes:{cycle_nodes}\n")
                # print(
                #   f"matching cycle: {matching_index}\nnodes:{cycle_rock_nodes_ls[matching_index]}\n\n")
            else:  # cycle broke
                # print(f"cycle broke at position {len(fingerprint_ls)}")
                fingerprint_ls = []
                step_height_ls = []
                fingerprint_zero_cycle_index = None
        else:  # new list
            fingerprint_zero_cycle_index = matching_index
            fingerprint_ls.append(cycle_nodes)
            step_height_ls.append(top_point)
            # print(f"\ncurr cycle:{curr_step}\nnodes:{cycle_nodes}\n")
            # print(
            #   f"matching cycle: {matching_index}\nnodes:{cycle_rock_nodes_ls[matching_index]}\n\n")
            cycle_height_ls.append(top_point)
    else:
        if num_full_cycles == 2:  # two full cycles seems good.
            # does the stack gain the same height each full cycle?
            height_diff_ls = [cycle_height_ls[i + 1] - cycle_height_ls[i] for i in range(len(cycle_height_ls) - 1)]
            if len(set(height_diff_ls)) <= 1:  # all are same value:
                # how many rocks left to drop
                num_remaining_rocks = num_rocks - curr_step
                # how many full cycles is that and how many remaining steps?
                quotient, remainder = divmod(num_remaining_rocks, cycle_length)
                full_cycle_height = quotient * height_diff_ls[0]
                partial_cycle_height = step_height_ls[remainder] - step_height_ls[0]
                total_height = top_point + full_cycle_height + partial_cycle_height - 1
        elif matching_index == fingerprint_zero_cycle_index:
            num_full_cycles += 1
            # print(f"full cycle complete, cycle is {len(fingerprint_ls)} steps long, cycle number {num_full_cycles}")
            cycle_height_ls.append(top_point)
        elif fingerprint_ls.index(cycle_nodes) + fingerprint_zero_cycle_index != matching_index: # cycle broke
            # print(f"cycle broke at position {len(fingerprint_ls)}")
            fingerprint_ls = []
            step_height_ls = []
            fingerprint_zero_cycle_index = None

    return fingerprint_ls, fingerprint_zero_cycle_index, num_full_cycles, cycle_height_ls, step_height_ls, cycle_length, total_height


def model_falling_rocks(raw_input, num_rocks):
    """
    models the falling of num_rocks given the pattern of jet streams in the puzzle input
    :param raw_input: puzzle input
    :param num_rocks: number of rocks to model
    :return:
    """
    jet_pattern_gen = make_jet_pattern_generator(raw_input)
    rock_gen = make_rock_generator()

    # define landmarks
    top_point = -1  # highest point (use to determine drop point)
    rock_nodes = {(x, -1) for x in range(7)}  # points that are fallen rock

    total_height = None  # height of the whole modeled stack
    curr_step = 0

    cycle_rock_nodes_ls = []  # "fingerprint" or rock nodes at each step.  used to find repeating cycles)
    fingerprint_ls = []

    step_height_ls = []
    fingerprint_zero_cycle_index = None
    num_full_cycles = 0
    cycle_length = None
    cycle_height_ls = []  # height of pile at the end of each cycle

    while (not total_height) and (curr_step < num_rocks):
        if curr_step % 100 == 0:
            print(f"i = {curr_step}")
            print(f"num rock nodes = {len(rock_nodes)}")
        curr_rock = next(rock_gen)
        # postion drop point of the new rock
        x_offset = 2
        y_offset = top_point + 4

        curr_rock.coord_set = {
            (curr_coord[0] + x_offset, curr_coord[1] + y_offset) for curr_coord in curr_rock.coord_set
        }
        falling = True
        next_step_gen = itertools.cycle(["jet", "fall"])
        while falling:
            next_action = next(next_step_gen)
            if next_action == "jet":
                next_jet_pattern = next(jet_pattern_gen)
                if next_jet_pattern == ">":
                    if max([x[0] for x in curr_rock.coord_set]) < 6:  # there is room to move right
                        test_coord_set = {
                            (curr_coord[0] + 1, curr_coord[1]) for curr_coord in curr_rock.coord_set
                        }
                elif next_jet_pattern == "<":
                    if min([x[0] for x in curr_rock.coord_set]) > 0:  # there is room to move left
                        test_coord_set = {
                            (curr_coord[0] - 1, curr_coord[1]) for curr_coord in curr_rock.coord_set
                        }
                else:
                    raise UnknownPatternError("unknown jet pattern")

                # does the proposed movement intersect with existing rock?
                if not test_coord_set.intersection(rock_nodes):
                    curr_rock.coord_set = test_coord_set  # update coordinates
            elif next_action == 'fall':
                test_coord_set = {
                    (curr_coord[0], curr_coord[1] - 1) for curr_coord in curr_rock.coord_set
                }
                # can it fall further?
                if not test_coord_set.intersection(rock_nodes):  # can fall further?
                    curr_rock.coord_set = test_coord_set  # update coordinates
                else:  # blocked
                    # comes to rest
                    falling = False
                    rock_nodes = rock_nodes.union(curr_rock.coord_set)
                    top_point = max([x[1] for x in rock_nodes])

                    # can we get rid of some nodes?

                    # define  "roof" (top layer of rock
                    roof_ls = [max([x[1] for x in [y for y in rock_nodes if y[0] == x_coord]]) for x_coord in range(7)]
                    # drop all nodes lower than the lowest roof

                    lowest_roof = min(roof_ls)
                    rock_nodes = {x for x in rock_nodes if x[1] >= lowest_roof}

                    # find the cycle

                    # tare rock nodes against the lowest roof

                    cycle_nodes = {(node[0], node[1] - lowest_roof) for node in rock_nodes}

                    if cycle_nodes in cycle_rock_nodes_ls:
                        fingerprint_ls, fingerprint_zero_cycle_index, num_full_cycles, cycle_height_ls, step_height_ls, cycle_length, total_height = analyze_cycle(
                            curr_step,
                            cycle_nodes,
                            cycle_rock_nodes_ls,
                            fingerprint_ls,
                            fingerprint_zero_cycle_index,
                            num_full_cycles,
                            cycle_height_ls,
                            top_point,
                            step_height_ls,
                            cycle_length,
                            num_rocks,
                            total_height,
                        )

                    cycle_rock_nodes_ls.append(cycle_nodes)
        curr_step += 1
    return total_height


if __name__ == '__main__':
    print(f"height of final tower is {model_falling_rocks(data, 2022)}")
