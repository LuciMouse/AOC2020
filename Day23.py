from aocd import data


def parse_input(raw_data):
    """
    takes the raw puzzle input and transforms it into an array representing the positions of all the elves
    0,0 is the lower left (SW) corner of the defined rectangle
    :param raw_data: raw puzzle input
    :return: array of elf locations
    """
    ...


def find_surrounding_elves(curr_index, elf_position_ls):
    """
    deterimes the number and positions of elves in the eight surrounding positions

    postion_array is is the following order:
    [N,NE,E,SE,S,SW,W,NW]

    :param curr_index:
    :param elf_position_ls: the postion of the central elf
    :return: array of positions of elves in surrounding positions
    """
    ...


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
    :param elf_position_ls: current postions of each elf
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
    :return: list containing the coordinates of the smallest bounding rectangle
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
