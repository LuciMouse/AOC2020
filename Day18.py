from aocd import data


def is_adjacent(cube1, cube2):
    """
    determines if the two cubes share a face
    :param cube1: cube defined as (x,y,z) coordinates
    :param cube2: cube defined as (x,y,z) coordinates
    :return: True if cubes share a face, otherwise false

    >>> is_adjacent((1,1,1),(2,1,1))
    True

    >>> is_adjacent((1,1,1),(2,2,2))
    False

    >>> is_adjacent((1,2,2),(2,2,2))
    True

    >>> is_adjacent((2,2,1),(2,2,2))
    True

    >>> is_adjacent((2,1,2),(2,2,2))
    True

    >>> is_adjacent((1,1,1),(3,1,1))
    False
    """
    # to share a face, two of the three coordinates need to be the same, and the third needs to be only one different
    shared_coordinates = [cube1[0] == cube2[0], cube1[1] == cube2[1], cube1[2] == cube2[2]]
    if sum(shared_coordinates) == 2:
        # determine different side
        diff_index = shared_coordinates.index(False)
        if abs(cube1[diff_index] - cube2[diff_index]) == 1:
            return True
    return False


def calculate_exposed_surfaces(cubes_ls):
    """
    given a list of cubes, calculates the surface area
    :param cubes_ls: list of cube coordinates
    :return: surface area of droplet

    >>> calculate_exposed_surfaces([(1,1,1),(2,1,1)])
    10
    """
    max_exposed_surfaces = len(cubes_ls) * 6
    surface_area = max_exposed_surfaces
    for cube in cubes_ls:
        adjacent_cubes_ls = [x for x in [y for y in cubes_ls if y != cube] if is_adjacent(x, cube)]
        surface_area -= len(adjacent_cubes_ls)
    return surface_area


def find_surface_area(raw_input):
    """
    determines the surface area of a doplet given an array of its component cubes
    :param raw_input: raw puzzle input
    :return: surface area
    """
    cubes_ls = list(map(lambda x:[int(y) for y in x], [row.split(',') for row in raw_input.split('\n')]))
    surace_area = calculate_exposed_surfaces(cubes_ls)
    return surace_area
if __name__ == '__main__':
    print(f"part1 surface area is {find_surface_area(data)}")
