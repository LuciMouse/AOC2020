from aocd import data


def diagram_rock_path(rock_path_ls, sand_source_coord):
    """
    makes a diagram of the initial cave structure
    :param sand_source_coord: coordinate where the stand starts from
    :param rock_path_ls: list of rock paths
    :return: list describing cave structure
    """
    # get the max and min column and row values

    row_values = set()
    col_values = set()

    for path in rock_path_ls:
        for node in path:
            row_values.add(node[1])
            col_values.add(node[0])
    sorted_row_values_ls = list(row_values)
    sorted_row_values_ls.sort()
    sorted_col_values_ls = list(col_values)
    sorted_col_values_ls.sort()
    # how many rows do we need
    num_rows = sorted_row_values_ls[-1] + 1

    # how many columns do we need
    num_cols = sorted_col_values_ls[-1] - sorted_col_values_ls[0] + 1

    # what col value correspponds to index 0
    zero_index_value = sorted_col_values_ls[0]

    sand_diagram_ls = [['.' for cols in range(num_cols)] for rows in range(num_rows)]

    # add rock paths
    for path in rock_path_ls:
        # write first node of path
        sand_diagram_ls[path[0][1]][path[0][0] - zero_index_value] = '#'
        for index in range(len(path) - 1):
            # is it a vertical or a horizontal line?
            start_node = path[index]
            end_node = path[index + 1]
            if start_node[0] == end_node[0]:  # vertical
                if start_node[1] < end_node[1]:
                    start = start_node[1] + 1
                    end = end_node[1] + 1
                else:
                    start = end_node[1] + 1
                    end = start_node[1] + 1
                x_coord = start_node[0] - zero_index_value
                for y_coord in range(start, end):
                    sand_diagram_ls[y_coord][x_coord] = '#'
            elif start_node[1] == end_node[1]:
                # horizontal
                if start_node[0] < end_node[0]:
                    start = start_node[0] + 1 - zero_index_value
                    end = end_node[0] + 1 - zero_index_value
                else:
                    start = end_node[0] - zero_index_value
                    end = start_node[0] - zero_index_value
                y_coord = start_node[1]
                for x_coord in range(start, end):
                    sand_diagram_ls[y_coord][x_coord] = '#'
    # write sand source
    sand_diagram_ls[sand_source_coord[1]][sand_source_coord[0] - zero_index_value] = '+'
    return sand_diagram_ls, zero_index_value


def drop_sand(sand_diagram_ls, sand_coord, zero_index_value):
    """
    adds a single unit of sand and determines where it lands
    :param sand_diagram_ls: diagram of cave structure
    :param sand_coord: coordinate where the sand starts from
    :param zero_index_value: value of the 0 point of the x array
    :return: final resting position of the unit of sand and whether the cave is full
    """

    down_space = True

    while down_space:  # drop down as far as possible
        drop_coord = (sand_coord[0], sand_coord[1] + 1)
        if (
                (drop_coord[0] - zero_index_value >= len(sand_diagram_ls[0])) or
                (drop_coord[0] - zero_index_value < 0) or
                (drop_coord[1] > len(sand_diagram_ls) - 1)
        ):  # off the grid, cave is full
            return (-1, -1), True
        if sand_diagram_ls[drop_coord[1]][drop_coord[0] - zero_index_value] == '.':
            sand_coord = drop_coord
        elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - zero_index_value] in {'#', 'o'}:  # hits rock or sand
            down_space = False

    # try down and to the left
    drop_coord = (sand_coord[0] - 1, sand_coord[1] + 1)
    if (
            (drop_coord[0] - zero_index_value >= len(sand_diagram_ls[0])) or
            (drop_coord[0] - zero_index_value < 0) or
            (drop_coord[1] > len(sand_diagram_ls) - 1)
    ):  # off the grid, cave is full
        return (-1, -1), True
    elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - zero_index_value] == '.':  # drop down one spot
        return drop_sand(sand_diagram_ls, drop_coord, zero_index_value)  # and remodel
    elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - zero_index_value] in {'#', 'o'}:  # hits rock or sand
        drop_coord = (sand_coord[0] + 1, sand_coord[1] + 1)  # try down and to the right
        if (
                (drop_coord[0] - zero_index_value >= len(sand_diagram_ls[0])) or
                (drop_coord[0] - zero_index_value < 0) or
                (drop_coord[1] > len(sand_diagram_ls) - 1)
        ):  # off the grid, cave is full
            return (-1, -1), True
        elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - zero_index_value] == '.':  # drop down one spot
            return drop_sand(sand_diagram_ls, drop_coord, zero_index_value)  # and remodel
        elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - zero_index_value] in {'#', 'o'}:  # hits rock or sand
            return sand_coord, False  # rests here


def add_sand(sand_diagram_ls, sand_source_coord, zero_index_value):
    """
    adds sand into sand diagram until it's full
    :param sand_diagram_ls: diagram of cave structure
    :param sand_source_coord: coordinate where the sand starts from
    :param zero_index_value: value of the 0 point of the x array
    :return: amount of sand needed to fill cave
    """
    full = False
    sand_count = 0

    while not full:
        if sand_count==1136:
            print("foo")
        try:
            rest_posn, full = drop_sand(sand_diagram_ls, sand_source_coord, zero_index_value)
        except IndexError:
            print (sand_count)
        if not full:
            sand_diagram_ls[rest_posn[1]][rest_posn[0] - zero_index_value] = 'o'
            sand_count += 1
    return sand_count


def sand_counter(raw_data):
    rock_path_ls = [[[int(x) for x in node.split(',')] for node in path.split(' -> ')] for path in raw_data.split('\n')]
    sand_source_coord = (500, 0)
    sand_diagram_ls, zero_index_value = diagram_rock_path(rock_path_ls, sand_source_coord)

    sand_count = add_sand(sand_diagram_ls, sand_source_coord, zero_index_value)
    return sand_count


if __name__ == '__main__':
    print(f"sand count = {sand_counter(data)}")
