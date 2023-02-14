from aocd import data


def parse_location(curr_loc_string):
    """
    takes in a single location (either sensor or beacon) and returns the location as a tuple
    :param curr_loc_string: string in the format "Sensor at x=9, y=16"
    :return: tuple of location

    >>> parse_location("Sensor at x=9, y=16")
    (9, 16)

    >>> parse_location("closest beacon is at x=10, y=16")
    (10, 16)
    """
    loc_ls = curr_loc_string.split("at ")[1].split(", ")
    loc_tuple = tuple([int(x.split("=")[1]) for x in loc_ls])
    return loc_tuple


def parse_row(curr_string):
    """
    takes in a string and extracts the sensor/beacon location pair
    :param curr_string: raw input string in the format "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"
    :return: tuple of sensor/beacon locations

    example usage:
    >>> parse_row("Sensor at x=2, y=18: closest beacon is at x=-2, y=15")
    ((2, 18), (-2, 15))

    """
    split_row = curr_string.split(": ")
    sensor_beacon_loc_tuple = tuple(map(parse_location, split_row))

    return sensor_beacon_loc_tuple


def parse_input(raw_input):
    """
    takes in the raw data and returns as tuples of sensor/beacon locations
    :param raw_input: raw_input
    :return: tuple of tuples of sensor/beacon locations
    """
    split_input = raw_input.split("\n")
    locations_tuple = tuple(map(parse_row, split_input))
    return locations_tuple


def find_manhattan_distance(sensor_tuple, beacon_tuple):
    """
    given a pair of locations, calculates the manhattan distance between them
    :param sensor_tuple: location of the sensor
    :param beacon_tuple: location of the beacon
    :return: manhattan distance between the two locations

    >>> find_manhattan_distance((8,7),(2,10))
    9

    >>> find_manhattan_distance((0,11),(2,10))
    3
    """
    manhattan_distance = abs(sensor_tuple[0] - beacon_tuple[0]) + abs(sensor_tuple[1] - beacon_tuple[1])
    return manhattan_distance


def excluded_row_positions(center_posn, horiz_distance, max_value=None):
    """
    Finds the excluded positions in a row given the center position and the distance from the center
    :param max_value: maximum acceptable x value.  also sets the minimum value ot 0.  If omitted, allows all values
    :param center_posn: center position of the row
    :param horiz_distance: distance from the center to exclude
    :return: set of excluded positions in the row

    >>> excluded_row_positions((0,8),0)
    {(0, 8)}

    >>> excluded_row_positions((0,10), 2) == {(-2, 10),(-1, 10),(0, 10),(1, 10), (2, 10) }
    True

    >>> excluded_row_positions((0,10), 2, 1) == {(0, 10),(1, 10)}
    True

    """
    center_x_posn = center_posn[0]
    center_y_posn = center_posn[1]

    excluded_positions_set = set()

    if max_value:
        range_min = 0 if center_x_posn - horiz_distance < 0 else center_x_posn - horiz_distance
        range_max = max_value + 1 if center_x_posn + horiz_distance + 1 > max_value else center_x_posn + horiz_distance + 1
        for x_posn in range(range_min, range_max):
            excluded_positions_set.add((x_posn, center_y_posn))
    else:
        for x_posn in range(center_x_posn - horiz_distance, center_x_posn + horiz_distance + 1):
            excluded_positions_set.add((x_posn, center_y_posn))

    return excluded_positions_set


def find_excluded_positions(sensor_tuple, manhattan_distance, y_row):
    """
    given a sensor locations, returns the set of all positions that are within a specified distance from it
    :param sensor_tuple: location of sensor
    :param manhattan_distance: distance from sensor
    :return: set of all positions within manhattan_distance from sensor_tuple

    >>> find_excluded_positions((0,11),3,10) == { (-2, 10),(-1, 10),(0, 10),(1, 10),(2, 10)}
    True
    """

    sensor_x = sensor_tuple[0]
    sensor_y = sensor_tuple[1]

    # calculate distance between y_row and sensor
    y_dist = abs(sensor_y - y_row)

    excluded_positions_set = excluded_row_positions(
        (sensor_x, y_row),
        manhattan_distance - y_dist
    )

    return excluded_positions_set


def exclude_positions(location_tuple, y_row):
    """
    given a sensor/beacon location, determines all positions that cannot contain a beacon that are within y_row
    :param y_row: row to limit positions to
    :param location_tuple: location to analyze
    :param excluded_positions_set: current set of excluded positions
    :return: updated excluded_positions_set

    >>> exclude_positions(((0,11),(2,10)),set(),10) ==  { (-2, 10),(-1, 10),(0, 10),(1, 10),(2, 10)}
    True
    """
    sensor_tuple = location_tuple[0]
    beacon_tuple = location_tuple[1]

    manhattan_distance = find_manhattan_distance(sensor_tuple, beacon_tuple)
    excluded_positions_set = find_excluded_positions(sensor_tuple, manhattan_distance, y_row)

    return excluded_positions_set


def is_crossing(curr_tuple, y_row):
    """
    does the current sensor/beacon tuple cross y_row?
    :param curr_tuple: sensor/beacon tuple
    :param y_row: horizontal row that needs to be crossed
    :return: bool if the curr_tuple crosses y_row

    >>> is_crossing(((2, 18), (-2, 15)), 10)
    False
    >>> is_crossing(((9, 16), (10, 16)), 10)
    False
    >>> is_crossing(((13, 2), (15, 3)), 10)
    False
    >>> is_crossing(((12, 14), (10, 16)), 10)
    True
    >>> is_crossing(((10, 20), (10, 16)), 10)
    False
    >>> is_crossing(((14, 17), (10, 16)), 10)
    False
    >>> is_crossing(((8, 7), (2, 10)), 10)
    True
    >>> is_crossing(((2, 0), (2, 10)), 10)
    True
    >>> is_crossing(((0, 11), (2, 10)), 10)
    True
    >>> is_crossing(((20, 14), (25, 17)), 10)
    True
    >>> is_crossing(((17, 20), (21, 22)), 10)
    False
    >>> is_crossing(((16, 7), (15, 3)), 10)
    True
    >>> is_crossing(((14, 3), (15, 3)), 10)
    False
    >>> is_crossing(((20, 1), (15, 3)), 10)
    False
    """

    sensor_tuple_y = curr_tuple[0][1]
    beacon_tuple_y = curr_tuple[1][1]

    if (sensor_tuple_y == y_row) or (beacon_tuple_y == y_row):  # if either beacon or sensor is on y_row
        return True
    elif (
            (sensor_tuple_y < y_row) and (beacon_tuple_y > y_row) or
            (sensor_tuple_y > y_row) and (beacon_tuple_y < y_row)
    ):  # y_row is between the sensor and beacon rows
        return True
    else:
        manhattan_distance = find_manhattan_distance(*curr_tuple)
        if (sensor_tuple_y - manhattan_distance <= y_row) and (
                sensor_tuple_y + manhattan_distance >= y_row):  # y_row is within manhattan_distance from the sensor
            return True
        else:  # sensor pair does not cross y_row
            return False


def crossing_locations(locations_tuple, y_row):
    """
    given a tuple of locations, determines how many of them cross the given y-location
    :param locations_tuple: list of sensor/beacon locations
    :param y_row: y-row to investigate
    :return: tuple of locations that cross y_row

    >>> crossing_locations((((2, 18), (-2, 15)),((9, 16), (10, 16)), ((13, 2), (15, 3)),((12, 14), (10, 16)),((10, 20), (10, 16)),((14, 17), (10, 16)),((8, 7), (2, 10)),((2, 0), (2, 10)),((0, 11), (2, 10)),((20, 14), (25, 17)),((17, 20), (21, 22)),((16, 7), (15, 3)),((14, 3), (15, 3)),((20, 1), (15, 3))),10)
    (((12, 14), (10, 16)), ((8, 7), (2, 10)), ((2, 0), (2, 10)), ((0, 11), (2, 10)), ((20, 14), (25, 17)), ((16, 7), (15, 3)))
    """
    crossing_locations_tuple = tuple([x for x in locations_tuple if is_crossing(x, y_row)])
    return crossing_locations_tuple


def beacon_exclusion(raw_input, y_row):
    """
    takes the raw data and determines how many positions in a given row cannot have a beacon
    :param y_row: row to investigate
    :param raw_input: raw input of sensor and beacon locations
    :return: number of positions in y_row that cannot contain a beacon
    """
    locations_tuple = parse_input(raw_input)

    row_locations_tuple = crossing_locations(locations_tuple, y_row)  # limit to only postions that cross y_row

    excluded_positions_set = set()

    for curr_position in row_locations_tuple:
        excluded_positions_set = excluded_positions_set.union(
            exclude_positions(curr_position, y_row)
        )

    return len(excluded_positions_set) - 1


def find_tuning_frequency(raw_input, max_value):
    """
    given
    :param max_value: maximum value for either x or y coordinate
    :param raw_input: raw input of sensor and beacon locations
    :return: tuning frequency
    """
    locations_tuple = parse_input(raw_input)

    # check each row
    for row_num in range(max_value + 1):
        row_locations_tuple = crossing_locations(locations_tuple, row_num)
        excluded_positions_set = set()
        for curr_position in row_locations_tuple:
            excluded_positions_set = excluded_positions_set.union(
                exclude_positions(curr_position, row_num)
            )
        filtered_exclusion_position_set = {position for position in excluded_positions_set if
                                           ((position[0] <= max_value) and (position[1] <= max_value) and (
                                                   position[0] >= 0) and (position[1]) >= 0)}
        if len(filtered_exclusion_position_set) <= max_value:  # there's a position missing from the set
            x_posn = list(
                {x for x in range(max_value + 1)}.difference(
                    {position[0] for position in filtered_exclusion_position_set})
            )[0]
            tuning_frequency = (x_posn * 4000000) + row_num
            return tuning_frequency


if __name__ == '__main__':
    print(f"There are {beacon_exclusion(data, 2000000)} positions on row y=2000000 that cannot contain a beacon")
    print(f"The tuning frequency of the distress beacon is {find_tuning_frequency(data, 4000000)}")
