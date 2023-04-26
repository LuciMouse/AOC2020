from aocd import data
import re


def parse_input(raw_input):
    """
    splits input data into the map and directions
    :param raw_input: raw puzzle input
    :return: list of map configuration and directions
    """
    split_data = raw_input.splitlines()
    map_ls = split_data[:-2]
    max_length = max(len(row) for row in map_ls)
    map_ls = [row + " " * (max_length - len(row)) for row in map_ls]
    split_directions = split_data[-1]
    directions_ls = [(int(d), dict(R=1, L=-1).get(r, 0)) for d, r in re.findall("(\d+)(R|L)?", split_directions)]
    return map_ls, directions_ls


def first_tile_x(map_ls, row_index):
    """
    identifies the first tile in the given row
    :param map_ls: list of map configuration with each list representing a row
    :param row_index: index of row that we need to analyze
    :return: index of the first tile
    """
    curr_row = map_ls[row_index]
    index = [x == " " for x in curr_row].index(False)
    return index


def last_tile_x(map_ls, row_index):
    """
        identifies the last tile in the given row
        :param map_ls: list of map configuration with each list representing a row
        :param row_index: index of row that we need to analyze
        :return: index of the last tile
        """
    curr_row = map_ls[row_index][::-1]
    index = [x == " " for x in curr_row].index(False)
    return len(curr_row) - index - 1


def first_tile_y(map_ls, col_index):
    """
        identifies the first tile in the given column
        :param map_ls: list of map configuration with each list representing a row
        :param col_index: index of col that we need to analyze
        :return: index of the first tile
        """
    curr_col = [row[col_index] for row in map_ls]
    index = [x == " " for x in curr_col].index(False)
    return index


def last_tile_y(map_ls, col_index):
    """
            identifies the last tile in the given column
            :param map_ls: list of map configuration with each list representing a row
            :param col_index: index of col that we need to analyze
            :return: index of the last tile
            """
    curr_col = [row[col_index] for row in map_ls][::-1]
    index = [x == " " for x in curr_col].index(False)
    return len(curr_col) - index - 1


def new_facing(curr_facing, turn_dir):
    """
    given the current facing and the turn_dir, determines the new facing
    :param curr_facing: one of [0,1,2,3] (right, down, left, right)
    :param turn_dir: one of [1,-1] (clockwise, counter-clockwise)
    :return: new facing
    """
    result = curr_facing + turn_dir
    if result < 0:
        return 3
    elif result > 3:
        return 0
    else:
        return result


def parse_next_posn(path_ls, next_posn, next_posn_value):
    """
    determines if the next postion is open (.) or a wall (#) and updates the path accordingly
    :param path_ls: sequence of visited positions so far
    :param next_posn: next position to consider
    :param next_posn_value: value of next position
    :return: updated path_ls
    """
    if next_posn_value == "#":
        return True, path_ls
    elif next_posn_value == ".":
        return False, path_ls + [next_posn]
    else:
        raise Exception("next position not defined")


def take_step(map_ls, path_ls):
    """
    processes a single step of the instruction
    :param map_ls: list of map configuration with each list representing a row
    :param path_ls: sequence of visited positions so far
    :return: updated path_ls
    """
    curr_posn, curr_facing = path_ls[-1]
    if curr_facing == 0:  # right
        new_x = curr_posn[1] + 1
        if new_x == len(map_ls[0]):
            new_x = first_tile_x(map_ls, curr_posn[0])
        next_posn = (curr_posn[0], new_x)
        next_posn_value = map_ls[next_posn[0]][next_posn[1]]
        if next_posn_value == ' ':  # wrap off right
            new_x = first_tile_x(map_ls, curr_posn[0])
            next_posn = (curr_posn[0], new_x)
            next_posn_value = map_ls[next_posn[0]][next_posn[1]]
    elif curr_facing == 2:  # left
        new_x = curr_posn[1] - 1
        if new_x < 0:
            new_x = last_tile_x(map_ls, curr_posn[0])
        next_posn = (curr_posn[0], new_x)
        next_posn_value = map_ls[next_posn[0]][next_posn[1]]
        if next_posn_value == ' ':  # wrap off left
            new_x = last_tile_x(map_ls, curr_posn[0])
            next_posn = (curr_posn[0], new_x)
            next_posn_value = map_ls[next_posn[0]][next_posn[1]]
    elif curr_facing == 1:  # down
        new_y = curr_posn[0] + 1
        if new_y == len(map_ls):
            new_y = first_tile_y(map_ls, curr_posn[1])
        next_posn = (new_y, curr_posn[1])
        next_posn_value = map_ls[next_posn[0]][next_posn[1]]
        if next_posn_value == ' ':  # wrap off bottom
            new_y = first_tile_y(map_ls, curr_posn[1])
            next_posn = (new_y, curr_posn[1])
            next_posn_value = map_ls[next_posn[0]][next_posn[1]]
    elif curr_facing == 3:  # up
        new_y = curr_posn[0] - 1
        if new_y < 0:
            new_y = last_tile_y(map_ls, curr_posn[1])
        next_posn = (new_y, curr_posn[1])
        next_posn_value = map_ls[next_posn[0]][next_posn[1]]
        if next_posn_value == ' ':  # wrap off bottom
            new_y = last_tile_y(map_ls, curr_posn[1])
            next_posn = (new_y, curr_posn[1])
            next_posn_value = map_ls[next_posn[0]][next_posn[1]]

    return parse_next_posn(path_ls, (next_posn, curr_facing), next_posn_value)


def implement_instruction(path_ls, map_ls, instruction):
    """
    Implements a single instruction (# steps + 1 turn)
    :param path_ls: sequence of visited positions so far
    :param map_ls: list of map configuration with each list representing a row
    :param instruction: instruction to proccess
    :return: updated path_ls
    """
    num_steps = instruction[0]
    blocked = False
    # move
    while (num_steps > 0) & (not blocked):
        blocked, path_ls = take_step(
            map_ls,
            path_ls
        )
        num_steps -= 1
    # rotate
    last_step = path_ls[-1]
    path_ls[-1] = (last_step[0], new_facing(last_step[1], instruction[1]))

    return path_ls


def print_path(map_ls, path_ls):
    """
    helper function to visualize path_ls
    :param sequence of visited positions so far
    :param map_ls: list of map configuration with each list representing a row
    :return: printable map
    """
    working_map_ls = [[*row] for row in map_ls]
    facing_dict = {0: ">", 1: "V", 2: "<", 3: "^"}
    for node in path_ls:
        working_map_ls[node[0][0]][node[0][1]] = facing_dict[node[1]]
    working_map_ls = ["".join(row) for row in working_map_ls]
    for row in working_map_ls:
        print(row)
    print("\n\n")
    return working_map_ls


def calculate_password(position):
    """
    given the final location, calculates the password
    :param position: final position as ((row,col), facing)
    :return: password
    """
    row = position[0][0] + 1
    col = position[0][1] + 1
    facing = position[1]

    return (1000 * row) + (4 * col) + facing


def monkey_map_1(raw_input):
    """
    calculates the password given part1 parameters
    :param raw_input: raw puzzle input
    :return: password
    """
    map_ls, directions_ls = parse_input(raw_input)
    facing = 0
    curr_index = first_tile_x(map_ls, 0)
    curr_posn = (0, curr_index)
    path_ls = [(curr_posn, facing)]

    for curr_instruction in directions_ls:
        path_ls = implement_instruction(path_ls, map_ls, curr_instruction)
        #print_path(map_ls, path_ls)
    password = calculate_password(path_ls[-1])
    return password


if __name__ == '__main__':
    print(f"part1:{monkey_map_1(data)}")
