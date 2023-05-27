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


def find_surrounding_elves(curr_elf_position, elf_position_ls):
    """
    determines the number and positions of elves in the eight surrounding positions

    position_array is is the following order:
    [N,NE,E,SE,S,SW,W,NW]

    :param curr_elf_position: position of current elf
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

    surrounding_elves_ls = []
    for curr_position_diff in position_array:
        surrounding_position = (
            curr_elf_position[0] + curr_position_diff[0],
            curr_elf_position[1] + curr_position_diff[1]
        )
        if surrounding_position in elf_position_ls:
            surrounding_elves_ls.append(1)
        else:
            surrounding_elves_ls.append(0)
    return surrounding_elves_ls


def determine_proposed_move(curr_elf_position, surrounding_elves_ls, direction_ls):
    """
    given the list of surrounding elves, determines the proposed move for the elf
    :param curr_elf_position: position of current elf
    :param direction_ls: order of index directions to consider. in (index, diff) tuple where index are the
    indices that correspond with that direction (e.g. N -> N, NE, NW) and diff is the corresponding adjustment in position
    :param surrounding_elves_ls: list of surrounding elves
    :return: proposed move for the current elf
    """

    for curr_direction in direction_ls:
        if sum([surrounding_elves_ls[index] for index in curr_direction[0]]) == 0:
            return curr_elf_position[0] + curr_direction[1][0], curr_elf_position[1] + curr_direction[1][1]
    return curr_elf_position


def move_elves(elf_position_ls, directions_ls):
    """
    given the list of proposed moves for each elf, updates position of each elf
    :param elf_position_ls: current positions of each elf
    :param directions_ls: order of index directions to consider. in (index, diff) tuple where index are the
    indices that correspond with that direction (e.g. N -> N, NE, NW) and diff is the corresponding adjustment in position
    :return: updated elf_position_ls
    """
    proposed_moves_ls = [None for x in range(len(elf_position_ls))]
    updated_elf_positions_ls = [None for x in range(len(elf_position_ls))]
    conflicting_positions_ls = []

    for curr_index in range(len(elf_position_ls)):
        curr_position = elf_position_ls[curr_index]
        surrounding_elves_ls = find_surrounding_elves(curr_position, elf_position_ls)
        if sum(surrounding_elves_ls) > 0:
            proposed_move = determine_proposed_move(
                elf_position_ls[curr_index],
                surrounding_elves_ls,
                directions_ls,
            )
            if proposed_move in conflicting_positions_ls:  # already defined conflicting position
                updated_elf_positions_ls[curr_index] = curr_position
            else:
                try:
                    conflicting_index = proposed_moves_ls.index(proposed_move)
                    updated_elf_positions_ls[conflicting_index] = elf_position_ls[conflicting_index]
                    updated_elf_positions_ls[curr_index] = curr_position
                    conflicting_positions_ls.append(proposed_move)
                except ValueError:
                    proposed_moves_ls[curr_index] = proposed_move
                    updated_elf_positions_ls[curr_index] = proposed_move
        else:
            updated_elf_positions_ls[curr_index] = curr_position

    return updated_elf_positions_ls


def update_direction_list(direction_ls):
    """
    move the first direction to the end of the list of directions
    :param direction_ls: current list of directions
    :return: updated list of directions

    >>> update_direction_list([((7, 0, 1), (-1, 0)),((3, 4, 5), (1, 0)),((5, 6, 7), (0, 1)),((1, 2, 3), (0, -1))])
    [((3, 4, 5), (1, 0)), ((5, 6, 7), (0, 1)), ((1, 2, 3), (0, -1)), ((7, 0, 1), (-1, 0))]
    """
    return direction_ls[1:] + direction_ls[:1]


def determine_smallest_rectangle(elf_position_ls):
    """
    given the position of all elves, determines the coordinates of the smallest rectangle that contains all elves
    :param elf_position_ls: position of each elf
    :return: list containing the coordinates of the smallest bounding rectangle as defined by [NE, NW, SW, SE] corners
    """
    row_values = []
    col_values = []

    for position in elf_position_ls:
        col_values.append(position[0])
        row_values.append(position[1])
    return [
        (min(col_values), min(row_values)),
        (min(col_values), max(row_values)),
        (max(col_values), max(row_values)),
        (max(col_values), min(row_values)),
    ]


def count_empty_ground_tiles(elf_position_ls):
    """
    given the positions of all elves, determines the number of empty ground tiles in the smallest rectangle that countains all the elves
    :param elf_position_ls:
    :return: number of empty ground tiles
    """
    smallest_rectangle_ls = determine_smallest_rectangle(elf_position_ls)
    rectangle_area = (smallest_rectangle_ls[2][0] - smallest_rectangle_ls[0][0] + 1) * (
            smallest_rectangle_ls[2][1] - smallest_rectangle_ls[0][1] + 1)
    return rectangle_area - len(elf_position_ls)


def visualize_elf_positions(elf_position_map):
    """
    determines the smallest rectangle that contains all the elves and visualizes all the elf positions
    :param elf_position_map: position of all elves
    :return: list for printing
    """
    bounding_rectangle = elf_position_map.bounding_rectangle_ls
    elf_position_ls = elf_position_map.elf_position_ls

    num_cols = (bounding_rectangle[2][1] - bounding_rectangle[0][1])
    num_rows = (bounding_rectangle[2][0] - bounding_rectangle[0][0])

    visualized_elves_ls = []
    for curr_row in range(num_rows):
        row = ""
        for curr_col in range(num_cols):
            if (curr_row, curr_col) in elf_position_ls:
                row += "#"
            else:
                row += "."
        visualized_elves_ls.append(row)
    return visualized_elves_ls


def print_elf_positions(elf_position_map):
    """
    print the current position of all elves
    :param elf_position_map: position of all elves
    :return: None
    """
    visualized_elves_ls = visualize_elf_positions(elf_position_map)
    for row in visualized_elves_ls:
        print(row)
    print("\n\n")

def main(raw_data, num_rounds):
    """
    main function
    :param num_rounds: number of rounds to simulate, 0 = simulate to end of process
    :param raw_data:raw puzzle input
    :return: number of empty ground tiles
    """
    elf_position_map = parse_input(raw_data)
    #print_elf_positions(elf_position_map)
    directions_ls = [
        ((7, 0, 1), (-1, 0)),
        ((3, 4, 5), (1, 0)),
        ((5, 6, 7), (0, -1)),
        ((1, 2, 3), (0, 1))
    ]
    if num_rounds > 0:
        for curr_round in range(num_rounds):
            elf_position_map.elf_position_ls = move_elves(elf_position_map.elf_position_ls, directions_ls)
            directions_ls = update_direction_list(directions_ls)
            #print_elf_positions(elf_position_map)
    else:
        ...

    return count_empty_ground_tiles(elf_position_map.elf_position_ls)


if __name__ == '__main__':
    print(f"part 1:{main(data,10)}")
