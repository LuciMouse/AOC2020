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
    def __init__(self, name, left_edge_coord, bottom_coord, coord_set):
        """
        crates a new falling rock object
        :param name: name
        :param left_edge_coord: left-most point.  If there are multiple, the one that's the lowest
        :param bottom_coord: lowest point, if multiple the left-most point
        :param coord_set: set of coordinates in the rock shape
        """
        self.name = name
        self.left_edge_coord = left_edge_coord
        self.bottom_coord = bottom_coord,
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
            (0, 0),
            (0, 0),
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
            (0, 1),
            (1, 0),
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
            (0, 0),
            (0, 0),
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
            (0, 0),
            (0, 0),
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
            (0, 0),
            (0, 0),
            {
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1),
            }
        )
    )
    return itertools.cycle(rocks_ls)


if __name__ == '__main__':
    print(f"{data[4]}")
