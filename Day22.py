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


def inital_index(map_ls):
    top_row = map_ls[0]
    index = top_row.index(".")
    return index


def new_facing(curr_facing, turn_dir):
    result = curr_facing + turn_dir
    if result < 0:
        return 3
    elif result > 3:
        return 0
    else:
        return result

def implement_instruction(path_ls, map_ls, instruction):
    curr_posn = path_ls[-1][0]
    num_steps = instruction[0]


def monkey_map_1(raw_input):
    map_ls, directions_ls = parse_input(raw_input)
    facing = 0
    curr_index = inital_index(map_ls)
    curr_posn = (0, curr_index)
    path_ls = [(curr_posn, facing)]

    for curr_instruction in directions_ls:
        implement_instruction(path_ls, map_ls, curr_instruction)
    ...


if __name__ == '__main__':
    print(f"{data[4]}")
