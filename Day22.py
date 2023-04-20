from aocd import data
import re


def parse_input(raw_input):
    split_data = raw_input.splitlines()
    map_ls = split_data[:-2]
    max_length = max(len(row) for row in map_ls)
    map_ls = [row + " " * (max_length-len(row)) for row in map_ls]
    split_directions = split_data[-1]
    directions_ls = [(int(d), r) for d, r in re.findall("(\d+)(R|L)?", split_directions)]
    return map_ls, directions_ls


def monkey_map_1(raw_input):
    map_ls, directions_ls = parse_input(raw_input)

    ...


if __name__ == '__main__':
    print(f"{data[4]}")
