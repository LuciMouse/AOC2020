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
    rocks_ls = []

    rocks_ls.append(
        FallingRock(
            '-',
            {
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
            }
        )
    )

    rocks_ls.append(
        FallingRock(
            '+',

            {
                (1, 0),
                (0, 1),
                (1, 1),
                (2, 1),
                (1, 2),
            }
        )
    )

    rocks_ls.append(
        FallingRock(
            'L',

            {
                (0, 0),
                (1, 0),
                (2, 0),
                (2, 1),
                (2, 2),
            }
        )
    )

    rocks_ls.append(
        FallingRock(
            'I',

            {
                (0, 0),
                (0, 1),
                (0, 2),
                (0, 3),
            }
        )
    )

    rocks_ls.append(
        FallingRock(
            '.',

            {
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1),
            }
        )
    )
    return itertools.cycle(rocks_ls)


def draw_chamber(curr_rock, top_layer):
    """
    visualization of the chamber state
    :param curr_rock: object of the current rock
    :param top_layer: list of the top of the settled rocks
    :return: list of lists to print
    """

    highest_y = max(
        [
            max([x[1] for x in top_layer]),
            max([x[1] for x in curr_rock.coord_set])
        ]
    )

    chamber_ls = ['-------']

    for curr_y in range(highest_y+1):
        y_ls = []
        for curr_x in range(7):
            if (curr_x, curr_y) in top_layer:
                y_ls.append('#')
            elif (curr_x, curr_y) in curr_rock.coord_set:
                y_ls.append('@')
            else:
                y_ls.append('.')
        chamber_ls.insert(0, ''.join(y_ls))
    return chamber_ls

class UnknownPatternError(Exception):
    pass

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
    top_layer = {(x, -1) for x in range(7)}  # points that form the "path" of blocking rock

    for i in range(num_rocks):
        curr_rock = next(rock_gen)
        #postion drop point of the new rock
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
                    if max([x[0] for x in curr_rock.coord_set])<6: #there is room to move right
                        test_coord_set = {
                            (curr_coord[0] + 1, curr_coord[1]) for curr_coord in curr_rock.coord_set
                        }
                elif next_jet_pattern == "<":
                    if min([x[0] for x in curr_rock.coord_set])>0: #there is room to move left
                        test_coord_set = {
                            (curr_coord[0] - 1, curr_coord[1]) for curr_coord in curr_rock.coord_set
                        }
                else:
                    raise UnknownPatternError("unknown jet pattern")

                #does the proposed movement intersect with existing rock?
                if not test_coord_set.intersection(top_layer):
                    curr_rock.coord_set = test_coord_set #update coordinates
            elif next_action == 'fall':
                test_coord_set = {
                    (curr_coord[0], curr_coord[1] - 1) for curr_coord in curr_rock.coord_set
                }
                #can it fall further?
                if not test_coord_set.intersection(top_layer): #can fall further?
                    curr_rock.coord_set = test_coord_set #update coordinates
                else: #blocked
                    #comes to rest
                    falling = False
                    top_point = max([x[1] for x in curr_rock.coord_set])
                    top_layer = top_layer.union(curr_rock.coord_set)

    return top_point


if __name__ == '__main__':
    print(f"{data[4]}")
