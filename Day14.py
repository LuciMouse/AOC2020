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
            print("foo")

    return sand_diagram_ls, zero_index_value


def sand_counter(raw_data):
    rock_path_ls = [[[int(x) for x in node.split(',')] for node in path.split(' -> ')] for path in raw_data.split('\n')]
    sand_source_coord = (500, 0)
    sand_diagram_ls, zero_index_value = diagram_rock_path(rock_path_ls, sand_source_coord)
    return sand_count


if __name__ == '__main__':
    print(f"{data[4]}")
