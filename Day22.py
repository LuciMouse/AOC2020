from aocd import data
import re


def parse_input(raw_input):
    split_data = raw_input.splitlines()
    map_ls = split_data[:-2]
    max_length = max(len(row) for row in map_ls)
    map_ls = [row + " " * (max_length - len(row)) for row in map_ls]
    split_directions = split_data[-1]
    directions_ls = [(int(d), dict(R=1, L=-1).get(r, 0)) for d, r in re.findall("(\d+)(R|L)?", split_directions)]
    return map_ls, directions_ls


def first_open_tile_x(map_ls, row_index):
    curr_row = map_ls[row_index]
    index = [x == " " for x in curr_row].index(False)
    return index


def last_open_tile_x(map_ls, row_index):
    curr_row = map_ls[row_index][::-1]
    index = [x == " " for x in curr_row].index(False)
    return len(curr_row) - index - 1


def first_open_tile_y(map_ls, col_index):
    curr_col = [row[col_index] for row in map_ls]
    index = [x == " " for x in curr_col].index(False)
    return index


def last_open_tile_y(map_ls, col_index):
    curr_col = [row[col_index] for row in map_ls][::-1]
    index = [x == " " for x in curr_col].index(False)
    return len(curr_col) - index - 1


def new_facing(curr_facing, turn_dir):
    result = curr_facing + turn_dir
    if result < 0:
        return 3
    elif result > 3:
        return 0
    else:
        return result


def parse_next_posn(path_ls, next_posn, next_posn_value):
    if next_posn_value == "#":
        return True, path_ls
    elif next_posn_value == ".":
        return False, path_ls + [next_posn]
    else:
        raise Exception("next position not defined")


def take_step(map_ls, path_ls):
    curr_posn, curr_facing = path_ls[-1]
    if curr_facing == 0:  # right
        new_x = curr_posn[1] + 1
        if new_x == len(map_ls[0]):
            new_x = first_open_tile_x(map_ls, curr_posn[0])
        next_posn = (curr_posn[0], new_x)
        next_posn_value = map_ls[next_posn[0]][next_posn[1]]
        if next_posn_value == ' ':  # wrap off right
            new_x = first_open_tile_x(map_ls, curr_posn[0])
            next_posn = (curr_posn[0], new_x)
            next_posn_value = map_ls[next_posn[0]][next_posn[1]]
    elif curr_facing == 2:  # left
        new_x = curr_posn[1] - 1
        if new_x < 0:
            new_x = last_open_tile_x(map_ls, curr_posn[0])
        next_posn = (curr_posn[0], new_x)
        next_posn_value = map_ls[next_posn[0]][next_posn[1]]
        if next_posn_value == ' ':  # wrap off left
            new_x = last_open_tile_x(map_ls, curr_posn[0])
            next_posn = (curr_posn[0], new_x)
            next_posn_value = map_ls[next_posn[0]][next_posn[1]]
    elif curr_facing == 1:  # down
        new_y = curr_posn[0] + 1
        if new_y == len(map_ls):
            new_y = first_open_tile_y(map_ls, curr_posn[1])
        next_posn = (new_y, curr_posn[1])
        next_posn_value = map_ls[next_posn[0]][next_posn[1]]
        if next_posn_value == ' ':  # wrap off bottom
            new_y = first_open_tile_y(map_ls, curr_posn[1])
            next_posn = (new_y, curr_posn[1])
            next_posn_value = map_ls[next_posn[0]][next_posn[1]]
    elif curr_facing == 3:  # up
        new_y = curr_posn[0] - 1
        if new_y < 0:
            new_y = last_open_tile_y(map_ls, curr_posn[1])
        next_posn = (new_y, curr_posn[1])
        next_posn_value = map_ls[next_posn[0]][next_posn[1]]
        if next_posn_value == ' ':  # wrap off bottom
            new_y = last_open_tile_y(map_ls, curr_posn[1])
            next_posn = (new_y, curr_posn[1])
            next_posn_value = map_ls[next_posn[0]][next_posn[1]]

    return parse_next_posn(path_ls, (next_posn, curr_facing), next_posn_value)


def implement_instruction(path_ls, map_ls, instruction):
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
    row = position[0][0] + 1
    col = position[0][1] + 1
    facing = position[1]

    return (1000 * row) + (4 * col) + facing


def monkey_map_1(raw_input):
    map_ls, directions_ls = parse_input(raw_input)
    facing = 0
    curr_index = first_open_tile_x(map_ls, 0)
    curr_posn = (0, curr_index)
    path_ls = [(curr_posn, facing)]

    for curr_instruction in directions_ls:
        path_ls = implement_instruction(path_ls, map_ls, curr_instruction)
        #print_path(map_ls, path_ls)
    password = calculate_password(path_ls[-1])
    return password


if __name__ == '__main__':
    print(f"part1:{monkey_map_1(data)}")
