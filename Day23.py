from aocd import data


class ElfLocationMap():
    def __init__(self, elf_position_ls, bounding_rectangle_ls):
        self.elf_position_ls = elf_position_ls
        self.bounding_rectangle_ls = bounding_rectangle_ls


def parse_input(raw_data):
    """
    takes the raw puzzle input and transforms it into an array representing the positions of all the elves
    (row, column)
    0,0 is the upper left (NW) corner of the defined rectangle

    bounding rectangle as defined by [NE, NW, SW, SE] corners
    :param raw_data: raw puzzle input
    :return: ElfLocationMap object
    """
    elf_positions_ls = []
    split_data = raw_data.split('\n')
    num_rows = len(split_data)
    num_cols = len(split_data[0])
    for row_index in range(num_rows):
        for col_index in range(num_cols):
            if split_data[row_index][col_index] == "#":
                elf_positions_ls.append((row_index, col_index))


    return ElfLocationMap(
        elf_position_ls=elf_positions_ls,
        bounding_rectangle_ls=[(0, 0), (0, num_cols), (num_rows, num_cols), (num_rows, 0)]
    )


def find_surrounding_elves(curr_index, elf_position_ls):
    """
    determines the number and positions of elves in the eight surrounding positions

    position_array is is the following order:
    [N,NE,E,SE,S,SW,W,NW]

    :param curr_index: index of current elf in elf_position_ls
    :param elf_position_ls: current positions of each elf
    :return: array of positions of elves in surrounding positions
    """
    position_array = [
        (-1, 0),
        (-1, 1),
        (0, 1),
        (1, 1),
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, -1)
    ]
    curr_elf_position = elf_position_ls[curr_index]


def determine_proposed_move(surrounding_elves_ls, direction_ls):
    """
    given the list of surrounding elves, determines the proposed move for the
    :param direction_ls: order of directions to consider
    :param surrounding_elves_ls: list of surrounding elves
    :return: proposed move for the current elf
    """
    ...


def move_elves(elf_position_ls, proposed_moves_ls):
    """
    given the list of proposed moves for each elf, updates position of each elf
    :param elf_position_ls: current positions of each elf
    :param proposed_moves_ls: proposed move for each elf
    :return: updated elf_position_ls
    """
    ...


def update_direction_list(direction_ls):
    """
    move the first direction to the end of the list of directions
    :param direction_ls: current list of directions
    :return: updated list of directions
    """
    ...


def determine_smallest_rectangle(elf_position_ls):
    """
    given the position of all elves, determines the coordinates of the smallest rectangle that contains all elves
    :param elf_position_ls: position of each elf
    :return: list containing the coordinates of the smallest bounding rectangle as defined by [NE, NW, SW, SE] corners
    """
    ...


def count_empty_ground_tiles(elf_position_ls):
    """
    given the positions of all elves, determines the number of empty ground tiles in the smallest rectangle that countains all the elves
    :param elf_position_ls:
    :return: number of empty ground tiles
    """
    ...


def visualize_elf_positions(elf_position_ls):
    """
    determines the smallest rectangle that contains all the elves and visualizes all the elf postions
    :param elf_position_ls: position of all elves
    :return: list for printing
    """
    ...


def print_elf_positions(visualized_elves_ls):
    """
    print the current position of all elves
    :param visualized_elves_ls: list of mapped elf positions
    :return: None
    """
    ...


def main(raw_data, num_rounds):
    """
    main function
    :param num_rounds: number of rounds to simulate
    :param raw_data:raw puzzle input
    :return: number of empty ground tiles
    """
    ...


if __name__ == '__main__':
    print(f"{data[4]}")
