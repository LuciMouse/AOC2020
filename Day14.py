from aocd import data


def diagram_rock_path(rock_path_ls, sand_source_coord):
    """
    makes a set containing all the "rock" nodes of the cave structure and adds to a dictionary of defined nodes
    :param sand_source_coord: coordinate where the stand starts from
    :param rock_path_ls: list of rock paths
    :return: dictionary of defined nodes
    """

    rock_nodes_set = set()
    defined_nodes_dict = {}
    # parse rock paths
    for path in rock_path_ls:
        for index in range(len(path) - 1):
            # is it a vertical or a horizontal line?
            start_node = path[index]
            end_node = path[index + 1]
            if start_node[0] == end_node[0]:  # vertical
                if start_node[1] < end_node[1]:
                    start = start_node[1]
                    end = end_node[1] + 1
                else:
                    start = end_node[1]
                    end = start_node[1] + 1
                x_coord = start_node[0]
                for y_coord in range(start, end):
                    rock_nodes_set.add((x_coord, y_coord))
            elif start_node[1] == end_node[1]:
                # horizontal
                if start_node[0] < end_node[0]:
                    start = start_node[0]
                    end = end_node[0] + 1
                else:
                    start = end_node[0]
                    end = start_node[0] + 1
                y_coord = start_node[1]
                for x_coord in range(start, end):
                    rock_nodes_set.add((x_coord, y_coord))
    defined_nodes_dict["rock_nodes"] = rock_nodes_set
    # write sand source
    defined_nodes_dict["origin node"] = set(sand_source_coord)
    defined_nodes_dict["sand_nodes"] = set()
    # what col value corresponds to index 0
    index_values_dict = {}
    index_values_dict["min_x"] = min({value[0] for value in rock_nodes_set})
    index_values_dict["max_x"] = max({value[0] for value in rock_nodes_set})
    index_values_dict["max_y"] = max({value[1] for value in rock_nodes_set})

    return defined_nodes_dict, index_values_dict


def drop_sand(defined_nodes_dict, sand_coord, index_values_dict):
    """
    adds a single unit of sand and determines where it lands
    :param defined_nodes_dict: diagram of cave structure
    :param sand_coord: coordinate where the sand starts from
    :param index_values_dict: value of the 0 point of the x array
    :return: final resting position of the unit of sand and whether the cave is full
    """

    down_space = True

    while down_space:  # drop down as far as possible
        drop_coord = (sand_coord[0], sand_coord[1] + 1)
        if (drop_coord[1] > index_values_dict["max_y"]):
            # off the grid, cave is full
            return (-1, -1), True
        if drop_coord in defined_nodes_dict["rock_nodes"].union(defined_nodes_dict["sand_nodes"]):  # hits rock or sand
            down_space = False  # try diagonal directions
        else:
            sand_coord = drop_coord

            # try down and to the left
    drop_coord = (sand_coord[0] - 1, sand_coord[1] + 1)
    if (
            (drop_coord[0] >= index_values_dict["max_x"]) or
            (drop_coord[0] < index_values_dict["min_x"]) or
            (drop_coord[1] > index_values_dict["max_y"])
    ):  # off the grid, cave is full
        return (-1, -1), True
    elif drop_coord not in defined_nodes_dict["rock_nodes"].union(
            defined_nodes_dict["sand_nodes"]):  # drop down one spot
        return drop_sand(defined_nodes_dict, drop_coord, index_values_dict)  # and remodel
    else:  # hits rock or sand
        drop_coord = (sand_coord[0] + 1, sand_coord[1] + 1)  # try down and to the right
        if (
                (drop_coord[0] >= index_values_dict["max_x"]) or
                (drop_coord[0] < index_values_dict["min_x"]) or
                (drop_coord[1] > index_values_dict["max_y"])
        ):  # off the grid, cave is full
            return (-1, -1), True
        elif drop_coord not in defined_nodes_dict["rock_nodes"].union(
                defined_nodes_dict["sand_nodes"]):  # drop down one spot
            return drop_sand(defined_nodes_dict, drop_coord, index_values_dict)  # and remodel
        else:  # hits rock or sand
            return sand_coord, False  # rests here


def drop_sand_floor(sand_diagram_ls, sand_coord, index_values_dict):
    """
    adds a single unit of sand and determines where it lands. assumes infinite floor
    :param sand_diagram_ls: diagram of cave structure
    :param sand_coord: coordinate where the sand starts from
    :param index_values_dict: value of the 0 point of the x array
    :return: final resting position of the unit of sand and whether the cave is full
    """

    down_space = True

    while down_space:  # drop down as far as possible
        drop_coord = (sand_coord[0], sand_coord[1] + 1)
        if (
                (drop_coord[0] - index_values_dict >= len(sand_diagram_ls[0])) or
                (drop_coord[0] - index_values_dict < 0) or
                (drop_coord[1] > len(sand_diagram_ls) - 1)
        ):  # off the grid, cave is full
            return (-1, -1), True
        if sand_diagram_ls[drop_coord[1]][drop_coord[0] - index_values_dict] == '.':
            sand_coord = drop_coord
        elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - index_values_dict] in {'#', 'o'}:  # hits rock or sand
            down_space = False

    # try down and to the left
    drop_coord = (sand_coord[0] - 1, sand_coord[1] + 1)
    if (
            (drop_coord[0] - index_values_dict >= len(sand_diagram_ls[0])) or
            (drop_coord[0] - index_values_dict < 0) or
            (drop_coord[1] > len(sand_diagram_ls) - 1)
    ):  # off the grid, cave is full
        return (-1, -1), True
    elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - index_values_dict] == '.':  # drop down one spot
        return drop_sand(sand_diagram_ls, drop_coord, index_values_dict)  # and remodel
    elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - index_values_dict] in {'#', 'o'}:  # hits rock or sand
        drop_coord = (sand_coord[0] + 1, sand_coord[1] + 1)  # try down and to the right
        if (
                (drop_coord[0] - index_values_dict >= len(sand_diagram_ls[0])) or
                (drop_coord[0] - index_values_dict < 0) or
                (drop_coord[1] > len(sand_diagram_ls) - 1)
        ):  # off the grid, cave is full
            return (-1, -1), True
        elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - index_values_dict] == '.':  # drop down one spot
            return drop_sand(sand_diagram_ls, drop_coord, index_values_dict)  # and remodel
        elif sand_diagram_ls[drop_coord[1]][drop_coord[0] - index_values_dict] in {'#', 'o'}:  # hits rock or sand
            # rests here
            if sand_coord == (500, 0):
                return sand_coord, True
            else:
                return sand_coord, False


def add_sand(defined_nodes_dict, sand_source_coord, index_values_dict, has_floor):
    """
    adds sand into sand diagram until it's full
    :param defined_nodes_dict: dictionary of defined nodes
    :param has_floor: whether the cave has a floor
    :param sand_source_coord: coordinate where the sand starts from
    :param index_values_dict: value of the 0 point of the x array
    :return: amount of sand needed to fill cave
    """

    sand_count = 0
    full = False


    if has_floor == False:

        while not full:
            if sand_count == 1330:
                print("foo")
            try:
                rest_posn, full = drop_sand(defined_nodes_dict, sand_source_coord, index_values_dict)
            except IndexError:
                print(sand_count)
            if not full:
                defined_nodes_dict["sand_nodes"].add(rest_posn)
                sand_count += 1
        return sand_count

    else:
        while not full:
            try:
                rest_posn, full = drop_sand_floor(defined_nodes_dict, sand_source_coord, index_values_dict)
            except IndexError:
                print(sand_count)
            if not full:
                defined_nodes_dict["sand_nodes"].add(rest_posn)
                sand_count += 1
        return sand_count


def sand_counter(raw_data, has_floor):
    rock_path_ls = [[[int(x) for x in node.split(',')] for node in path.split(' -> ')] for path in raw_data.split('\n')]
    sand_source_coord = (500, 0)
    defined_nodes_dict, zero_index_value = diagram_rock_path(rock_path_ls, sand_source_coord)

    sand_count = add_sand(defined_nodes_dict, sand_source_coord, zero_index_value, has_floor)
    return sand_count


if __name__ == '__main__':
    print(f"sand count = {sand_counter(data, False)}")
