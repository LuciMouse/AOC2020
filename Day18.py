from aocd import data


class Cube:
    def __init__(self, cube_type, coordinates, sides_dict=None):
        if sides_dict is None:
            sides_dict = {}
        self.cube_type = cube_type  # 'lava' 'air'
        self.coordinates = coordinates
        self.sides_dict = sides_dict


class Side:
    def __init__(self, coordinates, side_type, flanking_cube_coordinates=None):
        """
        :param coordinates: 
        :param side_type: type of interface of the side
            covered: lava to lava
            exposed-interior: lava to air, trapped
            exposed-exterior: lava to air, exterior
            exposed-unknown: lava to air, unknown if trapped or exterior
            air-exterior: air to air, exterior or air to boundary (guaranteed exterior)
            air-interior: air to air, trapped
            air-unknown: air to air, unknown if trapped or exterior
            unknown: at least one side of interface is unknown
        :param flanking_cube_coordinates: set of coordinates of the two cubes flanking this side
        """
        if flanking_cube_coordinates is None:
            flanking_cube_coordinates = set()
        self.coordinates = coordinates
        self.side_type = side_type
        self.flanking_cube_coordinates = flanking_cube_coordinates


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


def find_shared_side(cube1, cube2):
    """
    given two adjacent cubes, gives the coordinate of the shared side
    :param cube1: cube defined as (x,y,z) coordinates
    :param cube2: cube defined as (x,y,z) coordinates
    :return: coordinates of shared side as (x,(y1,y2),z) coordinates (if the shared side was along the y-axis)

    >>> find_shared_side((1,1,2),(1,1,1))
    (1, 1, (1, 2))

    >>> find_shared_side((1,2,2),(2,2,2))
    ((1, 2), 2, 2)

    >>> find_shared_side((2,2,1),(2,2,2))
    (2, 2, (1, 2))

    >>> find_shared_side((2,1,2),(2,2,2))
    (2, (1, 2), 2)

    """
    shared_coordinates = [cube1[0] == cube2[0], cube1[1] == cube2[1], cube1[2] == cube2[2]]
    diff_index = shared_coordinates.index(False)
    shared_side = tuple(sorted((cube1[diff_index], cube2[diff_index])))
    side_coord = tuple([shared_side if index == diff_index else cube1[index] for index in range(3)])
    return side_coord


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

    # subtract shared faces from maximum
    for cube in cubes_ls:
        adjacent_cubes_ls = [x for x in [y for y in cubes_ls if y != cube] if is_adjacent(x, cube)]
        surface_area -= len(adjacent_cubes_ls)
        # could also do set math by generating set of six adjacent cubes and subtracting the ones that are in the cube_ls
    return surface_area


def adjacent_cube_generator(center_cube_coordinates):
    """
    generates coordinates of six adjacent cubes to the current cube
    :param center_cube_coordinates: coordinates of defining cube
    :return:
    """
    x, y, z = center_cube_coordinates
    adjacent_cubes_ls = [
        (x, y, z - 1),
        (x, y, z + 1),
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z)
    ]

    for cube in adjacent_cubes_ls:
        yield cube


def add_adjacent_cube_side(adjacent_cube, adjacent_side_cube_coord, shared_side_coord, max_bounds_tuple, min_bounds_tuple, cubes_dict,
                           sides_dict):
    """
    defines a side of the adjacent cube.  We only define the Side object and not the Cube object (adjacent_side_cube_coord)
    so that we don't end up recursing endlessly.
    :param adjacent_cube: Cube object we're defining a side for
    :param adjacent_side_cube_coord: coordinate of the flanking cube for the Side we're defining
    :param shared_side_coord: shared side between the lava_cube and the adjacent_cube (already defined)
    :param max_bounds_tuple: maximum allowable values for x, y, z
    :param cubes_dict: dictionary of all Cube objects
    :param sides_dict: dictionary of all Side objects
    :return:
    """
    adjacent_side_coord = find_shared_side(adjacent_cube.coordinates, adjacent_side_cube_coord)

    if adjacent_side_coord != shared_side_coord:  # not the side we just processed
        if adjacent_side_coord in sides_dict:  # exists in dictionary
            adjacent_side = sides_dict[adjacent_side_coord]
            adjacent_cube.sides_dict[adjacent_side_coord] = adjacent_side
            # can we define the side type?
            flanking_cubes_ls = [value for index, value in cubes_dict.items() if
                                 index in adjacent_side.flanking_cube_coordinates]
            if len(flanking_cubes_ls) > 1:  # both cubes defined
                cube_1_type = flanking_cubes_ls[0].cube_type
                cube_2_type = flanking_cubes_ls[1].cube_type

                # if either are air cubes, need to examine the sides
                cube_1_sides = flanking_cubes_ls[0].sides_dict.values()
                cube_1_side_types_set = set([side.side_type for side in cube_1_sides])
                cube_2_sides = flanking_cubes_ls[1].sides_dict.values()
                cube_2_side_types_set = set([side.side_type for side in cube_2_sides])

                # make sure cube_types are ok
                cube_type_check_ls = [cube_types not in {'air', 'lava'} for cube_types in [cube_1_type, cube_2_type]]
                if sum(cube_type_check_ls) > 0:
                    problem_cube_index = cube_type_check_ls.index(True)
                    raise Exception(f"cube{problem_cube_index + 1} type not defined")

                if cube_1_type == cube_2_type:
                    if cube_1_type == 'lava':
                        adjacent_side.side_type = 'covered'
                    elif cube_1_type == 'air':
                        # need to look at both air cubes
                        if len(
                                {'air-exterior', 'exposed-exterior'}.intersection(
                                    cube_1_side_types_set.union(cube_2_side_types_set)
                                )
                        ) > 0:
                            adjacent_side.side_type = 'air-exterior'
                        elif len(
                                {'air-interior', 'exposed-interior'}.intersection(
                                    cube_1_side_types_set.union(cube_2_side_types_set)
                                )
                        ) > 0:
                            adjacent_side.side_type = 'air-interior'
                        else:
                            adjacent_side.side_type = 'air-unknown'
                        # should't be able to have both, but catch it
                        if (
                                len(
                                    {'air-exterior', 'exposed-exterior'}.intersection(
                                        cube_1_side_types_set.union(cube_2_side_types_set)
                                    )
                                ) > 0) and (
                                len(
                                    {'air-interior', 'exposed-interior'}.intersection(
                                        cube_1_side_types_set.union(cube_2_side_types_set)
                                    )
                                ) > 0):
                            raise Exception("both types should not exist on the same cube")
                else:  # one of each exposed
                    if cube_1_type == 'air':
                        air_cube_side_types_set = cube_1_side_types_set
                    else:  # cube_2 is the air cube
                        air_cube_side_types_set = cube_2_side_types_set

                    if len({'air-exterior', 'exposed-exterior'}.intersection(air_cube_side_types_set)) > 0:
                        adjacent_side.side_type = 'exposed-exterior'
                    elif len({'air-interior', 'exposed-interior'}.intersection(air_cube_side_types_set)) > 0:
                        adjacent_side.side_type = 'exposed-interior'
                    else:
                        adjacent_side.side_type = 'exposed-unknown'

                    # should't be able to have both, but catch it
                    if (
                            len({'air-exterior', 'exposed-exterior'}.intersection(air_cube_side_types_set)) > 0) and (
                            len({'air-interior', 'exposed-interior'}.intersection(air_cube_side_types_set)) > 0):
                        raise Exception("both types should not exist on the same cube")

        else:
            # does this side touch the edge (i.e. the adjacent_side_cube_coord is out of bounds?
            is_edge_cube = sum(
                [(adjacent_side_cube_coord[index] > max_bounds_tuple[index]) or (adjacent_side_cube_coord[index] < min_bounds_tuple[index])
                 for index in range(3)]) > 0  # out of bounds
            # define the side type
            if is_edge_cube:  # assumes adjacent_side_cube to be cube_type 'air'
                if adjacent_cube.cube_type == 'lava':
                    side_type = 'exposed-exterior'
                else:
                    side_type = 'air-exterior'  # if adjacent_side_cube turns out to be 'lava' (i.e. this side_type should be 'covered'), this will get set properly upon defininition of the other cube
            else:
                side_type = 'unknown'  # will define this when we define the other flanking_cube of the side
            adjacent_side = Side(
                coordinates=adjacent_side_coord,
                side_type=side_type,
                flanking_cube_coordinates={adjacent_cube.coordinates, adjacent_side_cube_coord}
            )
            sides_dict[adjacent_side_coord] = adjacent_side
            adjacent_cube.sides_dict[adjacent_side_coord] = adjacent_side


def add_adjacent_cube(adjacent_cube_coord, center_cube, lava_cubes_ls, max_bounds_tuple, min_bounds_tuple, cubes_dict, sides_dict):
    if adjacent_cube_coord in cubes_dict:
        adjacent_cube = cubes_dict[adjacent_cube_coord]
    else:
        adjacent_cube = Cube(
            coordinates=adjacent_cube_coord,
            cube_type="lava" if adjacent_cube_coord in lava_cubes_ls else "air"
        )
        cubes_dict[adjacent_cube_coord] = adjacent_cube
    # define shared side
    shared_side_coord = find_shared_side(center_cube.coordinates, adjacent_cube_coord)
    if center_cube.cube_type=='lava':
        shared_side_type = 'covered' if adjacent_cube.cube_type == 'lava' else 'exposed-unknown'
    elif center_cube.cube_type=='air':
        shared_side_type = 'exposed-unknown' if adjacent_cube.cube_type == 'lava' else 'air-unknown'
    else:
        raise Exception("center cube type not defined")
    if shared_side_coord in sides_dict:
        shared_side = sides_dict[shared_side_coord]
        if shared_side.side_type == 'unknown':
            shared_side.side_type = shared_side_type
    else:
        shared_side = Side(
            coordinates=shared_side_coord,
            side_type=shared_side_type,
            flanking_cube_coordinates={center_cube.coordinates, adjacent_cube_coord}
        )
        sides_dict[shared_side_coord] = shared_side
    center_cube.sides_dict[shared_side_coord] = shared_side
    adjacent_cube.sides_dict[shared_side_coord] = shared_side

    # define other sides of adjacent_cube, but only define the sides, not the cubes
    for adjacent_side_cube_coord in adjacent_cube_generator(adjacent_cube_coord):
        add_adjacent_cube_side(adjacent_cube, adjacent_side_cube_coord, shared_side_coord, max_bounds_tuple, min_bounds_tuple,
                               cubes_dict, sides_dict)


def add_lava_cube(lava_cube_coord, lava_cubes_ls, max_bounds_tuple, min_bounds_tuple, cubes_dict, sides_dict):
    if lava_cube_coord in cubes_dict:
        lava_cube = cubes_dict[lava_cube_coord]
    else:
        lava_cube = Cube(
            coordinates=lava_cube_coord,
            cube_type='lava'
        )
        cubes_dict[lava_cube_coord] = lava_cube

    for adjacent_cube_coord in adjacent_cube_generator(lava_cube_coord):
        if sum([((adjacent_cube_coord[index] > max_bounds_tuple[index]) or (adjacent_cube_coord[index] < min_bounds_tuple[index])) for index
                in
                range(3)]) == 0:  # not out of bound
            add_adjacent_cube(adjacent_cube_coord, lava_cube, lava_cubes_ls, max_bounds_tuple, min_bounds_tuple, cubes_dict,
                              sides_dict)
        else:  # still need to create the side of lava_cube
            shared_side_coord = find_shared_side(lava_cube.coordinates, adjacent_cube_coord)
            if shared_side_coord in sides_dict:
                shared_side = sides_dict[shared_side_coord]
            else:
                shared_side = Side(
                    coordinates=shared_side_coord,
                    side_type='exposed-exterior',
                    flanking_cube_coordinates={lava_cube.coordinates, adjacent_cube_coord}
                )
            sides_dict[shared_side_coord] = shared_side
            lava_cube.sides_dict[shared_side_coord] = shared_side


def visualize_drop_lava(lava_cubes_ls, max_bounds_tuple, min_bounds_tuple,):
    # create empty arrays
    droplet_ls = [
        [
            [
                "." for x in range(max_bounds_tuple[0]-min_bounds_tuple[0]+1)
            ] for y in range(max_bounds_tuple[1]-min_bounds_tuple[1]+1)
        ] for z in range(max_bounds_tuple[2]-min_bounds_tuple[2]+1)
    ]
    for lava_cube_coord in lava_cubes_ls:
        x_coord, y_coord, z_coord = lava_cube_coord
        droplet_ls[z_coord-min_bounds_tuple[2]][y_coord-min_bounds_tuple[1]][x_coord-min_bounds_tuple[0]] = 'L'
    return droplet_ls

def visualize_drop_lava_air(cubes_dict, max_bounds_tuple, min_bounds_tuple):
    # create empty arrays
    droplet_ls = [
        [
            [
                "." for x in range(max_bounds_tuple[0]-min_bounds_tuple[0]+1)
            ] for y in range(max_bounds_tuple[1]-min_bounds_tuple[1]+1)
        ] for z in range(max_bounds_tuple[2]-min_bounds_tuple[2]+1)
    ]
    for cube in cubes_dict.values():
        x_coord, y_coord, z_coord = cube.coordinates
        if cube.cube_type == 'lava':
            droplet_ls[z_coord-min_bounds_tuple[2]][y_coord-min_bounds_tuple[1]][x_coord-min_bounds_tuple[0]] = 'L'
        else:#air cube
            #is it internal or external?
            cube_sides = cube.sides_dict.values()
            cube_side_types_set = set([side.side_type for side in cube_sides])
            if len({'air-exterior', 'exposed-exterior'}.intersection(cube_side_types_set)) > 0:
                droplet_ls[z_coord-min_bounds_tuple[2]][y_coord-min_bounds_tuple[1]][x_coord-min_bounds_tuple[0]] = '+'
            elif len({'air-interior', 'exposed-interior'}.intersection(cube_side_types_set)) > 0:
                droplet_ls[z_coord-min_bounds_tuple[2]][y_coord-min_bounds_tuple[1]][x_coord-min_bounds_tuple[0]] = '*'
            else:
                droplet_ls[z_coord-min_bounds_tuple[2]][y_coord-min_bounds_tuple[1]][x_coord-min_bounds_tuple[0]] = '?'

    return droplet_ls


def update_single_air_cubes(
        cubes_dict
):
    """
    defines single air cubes
    :param cubes_dict: dictionary of cube objects
    :return: none
    """
    # find all single air cubes

    air_cubes_ls = [cube for cube_coord, cube in cubes_dict.items() if cube.cube_type == 'air']
    single_air_cubes_ls = []

    for curr_cube in air_cubes_ls:
        curr_sides = curr_cube.sides_dict.values()
        flanking_cubes_set = frozenset().union(
            *[frozenset(side.flanking_cube_coordinates) for side in curr_sides]).difference({curr_cube.coordinates})
        flanking_cube_coord_type_ls = [
            cubes_dict[cube_coord].cube_type if cube_coord in cubes_dict else None for cube_coord in flanking_cubes_set
        ]
        if sum([cube_type == 'lava' for cube_type in flanking_cube_coord_type_ls]) == 6:
            single_air_cubes_ls.append(curr_cube)
    for curr_cube in single_air_cubes_ls:
        for side in curr_cube.sides_dict.values():
            side.side_type = 'exposed-interior'


def update_unknown_sides(sides_dict, cubes_dict, unknown_sides_ls):
    """
        defines all unknown sides.
        first, looks at the flanking cubes and sees if any of them are definitely exterior
        then defines all other sides as "interior" since they don't touch an "exterior" cube
        :param sides_dict: dictionary of side objects
        :param cubes_dict: dictionary of cube objects
        :param unknown_sides_ls: list of sides of side_type 'unknown'
        :return:
        """
    updated_side = True

    while updated_side:
        updated_side = False
        for curr_side in unknown_sides_ls:
            # are both flanking_cubes in cubes_dict?
            flanking_cube_coord_ls = [cube_coord for cube_coord in curr_side.flanking_cube_coordinates if
                                      cube_coord in cubes_dict]
            flanking_cube_type_set = {cubes_dict[cube_coord].cube_type for cube_coord in flanking_cube_coord_ls}
            if flanking_cube_type_set == {'air'}:
                flanking_cube_side_types_set = set().union(
                    *[set([side.side_type for side in value.sides_dict.values()]) for key, value in
                      cubes_dict.items()
                      if
                      key in curr_side.flanking_cube_coordinates])

                if len(
                        {'air-exterior', 'exposed-exterior'}.intersection(
                            flanking_cube_side_types_set
                        )
                ) > 0:
                    curr_side.side_type = 'air-exterior'
                    updated_side = True
                elif len(
                        {'air-interior', 'exposed-interior'}.intersection(
                            flanking_cube_side_types_set
                        )
                ) > 0:
                    curr_side.side_type = 'air-interior'
                    updated_side = True
                else:  # can't define right now
                    curr_side.side_type = 'air-unknown'

                # should't be able to have both, but catch it
                if (
                        len(
                            {'air-exterior', 'exposed-exterior'}.intersection(
                                flanking_cube_side_types_set
                            )
                        ) > 0) and (
                        len(
                            {'air-interior', 'exposed-interior'}.intersection(
                                flanking_cube_side_types_set
                            )
                        ) > 0):
                    raise Exception("both types should not exist on the same cube")
            elif flanking_cube_type_set == {'lava'}:
                curr_side.side_type = 'covered'
            elif flanking_cube_type_set == {'air', 'lava'}:
                # look at side types in flanking cubes
                flanking_cube_side_types_set = set().union(
                    *[set([side.side_type for side in value.sides_dict.values()]) for key, value in
                      cubes_dict.items()
                      if
                      key in curr_side.flanking_cube_coordinates])

                if len(
                        {'air-exterior', 'exposed-exterior'}.intersection(
                            flanking_cube_side_types_set
                        )
                ) > 0:
                    curr_side.side_type = 'exposed-exterior'
                    updated_side = True
                elif len(
                        {'air-interior', 'exposed-interior'}.intersection(
                            flanking_cube_side_types_set
                        )
                ) > 0:
                    curr_side.side_type = 'exposed-interior'
                    updated_side = True
                else:  # can't define right now
                    curr_side.side_type = 'exposed-unknown'
                # should't be able to have both, but catch it
                if (
                        len(
                            {'air-exterior', 'exposed-exterior'}.intersection(
                                flanking_cube_side_types_set
                            )
                        ) > 0) and (
                        len(
                            {'air-interior', 'exposed-interior'}.intersection(
                                flanking_cube_side_types_set
                            )
                        ) > 0):
                    raise Exception("both types should not exist on the same cube")
        unknown_sides_ls = [value for key, value in sides_dict.items() if value.side_type[:7] == 'unknown']


def update_air_sides(sides_dict, cubes_dict, unknown_air_sides_ls, max_bounds_tuple, min_bounds_tuple, lava_cubes_ls):
    """
    defines all unknown air-air sides.
    first, looks at the flanking cubes and sees if any of them are definitely exterior
    then defines all other sides as "interior" since they don't touch an "exterior" cube
    :param sides_dict: dictionary of side objects
    :param cubes_dict: dictionary of cube objects
    :param unknown_air_sides_ls: list of sides of side_type 'air-unknown'
    :return:
    """
    updated_side = True  # variable to track if we changed a side
    while updated_side:
        updated_side = False
        for curr_side in unknown_air_sides_ls:
            # if a flanking_cube is on the edge, then that is an exterior air cube
            flanking_cubes_coord_ls = list(curr_side.flanking_cube_coordinates)
            is_edge_cube = sum([
                ((
                         flanking_cubes_coord_ls[0][index] == max_bounds_tuple[index]
                 ) or (
                         flanking_cubes_coord_ls[1][index] == max_bounds_tuple[index]
                 ) or (
                         flanking_cubes_coord_ls[0][index] == 1
                 ) or (
                         flanking_cubes_coord_ls[1][index] == 1
                 )) for index in range(3)
            ]) > 0
            if is_edge_cube:
                curr_side.side_type = 'air-exterior'
                updated_side = True
            else:
                # if there are no lava cubes between this side and the edge, then it's an exterior air cube
                axis_index = [isinstance(coord, tuple) for coord in curr_side.coordinates].index(
                    True)  # index that corresponds with the axis the side is on
                stable_indices = [index for index in range(3) if index != axis_index]
                smaller_lava_cubes_ls = [cube_coordinates for cube_coordinates in lava_cubes_ls if (
                        (cube_coordinates[stable_indices[0]] == curr_side.coordinates[stable_indices[0]]) and
                        (cube_coordinates[stable_indices[1]] == curr_side.coordinates[stable_indices[1]]) and
                        (cube_coordinates[axis_index] < min(curr_side.coordinates[axis_index]))
                )
                                         ]
                if not smaller_lava_cubes_ls: #no smaller lava cubes on this axis
                    curr_side.side_type = 'air-exterior'
                    updated_side = True
                else:
                    larger_lava_cubes_ls = [cube_coordinates for cube_coordinates in lava_cubes_ls if (
                            (cube_coordinates[stable_indices[0]] == curr_side.coordinates[stable_indices[0]]) and
                            (cube_coordinates[stable_indices[1]] == curr_side.coordinates[stable_indices[1]]) and
                            (cube_coordinates[axis_index] > max(curr_side.coordinates[axis_index]))
                    )
                                             ]
                    if not larger_lava_cubes_ls:  # no larger lava cubes on this axis
                        curr_side.side_type = 'air-exterior'
                        updated_side = True
                    else:

                        # look at side types in flanking cubes
                        flanking_cube_side_types_set = set().union(
                            *[set([side.side_type for side in value.sides_dict.values()]) for key, value in cubes_dict.items()
                              if
                              key in curr_side.flanking_cube_coordinates])

                        if len(
                                {'air-exterior'}.intersection(
                                    flanking_cube_side_types_set
                                )
                        ) > 0:
                            curr_side.side_type = 'air-exterior'
                            updated_side = True
                        elif len(
                                {'air-interior'}.intersection(
                                    flanking_cube_side_types_set
                                )
                        ) > 0:
                            curr_side.side_type = 'air-interior'
                            updated_side = True
                        else:
                            #is only one flanking cube defined in cubes_dict? if so, define adjacent cubes to the existing cube
                            defined_flanking_cubes_ls = [cube for cube in flanking_cubes_coord_ls if cube in cubes_dict]
                            if len(defined_flanking_cubes_ls) == 1:
                                existing_cube_coord = defined_flanking_cubes_ls[0]
                                undefined_adjacent_cube_coords = set(adjacent_cube_generator(existing_cube_coord)).difference(set(cubes_dict))
                                for adjacent_cube_coord in undefined_adjacent_cube_coords:
                                    add_adjacent_cube(
                                        adjacent_cube_coord,
                                        cubes_dict[existing_cube_coord],
                                        lava_cubes_ls,
                                        max_bounds_tuple,
                                        min_bounds_tuple,
                                        cubes_dict,
                                        sides_dict,
                                    )
                                updated_side = True



                        # should't be able to have both, but catch it
                        if (
                                len(
                                    {'air-exterior', 'exposed-exterior'}.intersection(
                                        flanking_cube_side_types_set
                                    )
                                ) > 0) and (
                                len(
                                    {'air-interior', 'exposed-interior'}.intersection(
                                        flanking_cube_side_types_set
                                    )
                                ) > 0):
                            raise Exception("both types should not exist on the same cube")
        unknown_air_sides_ls = [value for key, value in sides_dict.items() if value.side_type == 'air-unknown']
    # if we can't define them, they must be internal
    for curr_side in unknown_air_sides_ls:
        curr_side.side_type = 'air-interior'


def update_exposed_sides(sides_dict, cubes_dict, unknown_exposed_sides_ls):
    """
    defines all unknown air-lava sides.
    first, looks at the flanking cubes and sees if any of them are definitely exterior
    then defines all other sides as "interior" since they don't touch an "exterior" cube
    :param sides_dict: dictionary of side objects
    :param cubes_dict: dictionary of cube objects
    :param unknown_exposed_sides_ls: list of sides of side_type 'exposed-unknown'
    :return:
    """
    updated_side = True  # variable to track if we changed a side
    while updated_side:
        updated_side = False
        for curr_side in unknown_exposed_sides_ls:
            # look at side types in flanking cubes
            flanking_cube_side_types_set = set().union(
                *[set([side.side_type for side in value.sides_dict.values()]) for key, value in cubes_dict.items() if
                  key in curr_side.flanking_cube_coordinates])

            if len(
                    {'air-exterior'}.intersection(
                        flanking_cube_side_types_set
                    )
            ) > 0:
                curr_side.side_type = 'exposed-exterior'
                updated_side = True
            elif len(
                    {'air-interior'}.intersection(
                        flanking_cube_side_types_set
                    )
            ) > 0:
                curr_side.side_type = 'exposed-interior'
                updated_side = True

            # should't be able to have both, but catch it
            if (
                    len(
                        {'air-exterior'}.intersection(
                            flanking_cube_side_types_set
                        )
                    ) > 0) and (
                    len(
                        {'air-interior'}.intersection(
                            flanking_cube_side_types_set
                        )
                    ) > 0):
                raise Exception("both types should not exist on the same cube")
        unknown_exposed_sides_ls = [value for key, value in sides_dict.items() if value.side_type == 'exposed-unknown']
    return unknown_exposed_sides_ls


def calculate_external_surface_area(lava_cubes_ls):
    """
    given a list of cubes, calculates the external surface area (i.e. removes surface area to inner air pockets)
    :param lava_cubes_ls: list of cube coordinates
    :return: external surface area of droplet
    """
    # dictionary to hold cubes
    cubes_dict = {}
    # dictionary to hold sides
    sides_dict = {}

    # what's the minimum value for x, y, z?
    min_x = min([cube[0] for cube in lava_cubes_ls])
    min_y = min([cube[1] for cube in lava_cubes_ls])
    min_z = min([cube[2] for cube in lava_cubes_ls])

    min_bounds_tuple = (min_x, min_y, min_z)

    # what's the maximum value for x, y, z?
    max_x = max([cube[0] for cube in lava_cubes_ls])
    max_y = max([cube[1] for cube in lava_cubes_ls])
    max_z = max([cube[2] for cube in lava_cubes_ls])

    max_bounds_tuple = (max_x, max_y, max_z)
    # for each stone cube, create 6 cubes around it
    for lava_cube_coord in lava_cubes_ls:
        add_lava_cube(
            lava_cube_coord, lava_cubes_ls, max_bounds_tuple, min_bounds_tuple, cubes_dict, sides_dict
        )
    # go through sides and see if we can define more sides

    # single air cubes that are completely surrounded by lava cubes are always 'exposed-internal'
    update_single_air_cubes(
        cubes_dict
    )

    unknown_sides_ls = [value for key, value in sides_dict.items() if value.side_type == 'unknown']
    if len(unknown_sides_ls):
        update_unknown_sides(
            sides_dict,
            cubes_dict,
            unknown_sides_ls
        )
    # look at the air:air sides that are undefined
    unknown_air_sides_ls = [value for key, value in sides_dict.items() if value.side_type == 'air-unknown']
    if len(unknown_air_sides_ls):
        update_air_sides(
            sides_dict,
            cubes_dict,
            unknown_air_sides_ls,
            max_bounds_tuple,
            min_bounds_tuple,
            lava_cubes_ls
        )
    # look at the lava:air sides that are undefined
    unknown_exposed_sides_ls = [value for key, value in sides_dict.items() if value.side_type == 'exposed-unknown']
    if len(unknown_exposed_sides_ls):
        update_exposed_sides(
            sides_dict,
            cubes_dict,
            unknown_exposed_sides_ls
        )
    all_sides_ls = [value for key, value in sides_dict.items() if value.side_type[:7] == 'exposed']
    covered_sides_ls = [value for key, value in sides_dict.items() if value.side_type == 'covered']
    external_sides_ls = [value for key, value in sides_dict.items() if value.side_type == 'exposed-exterior']
    internal_sides_ls = [value for key, value in sides_dict.items() if value.side_type == 'exposed-interior']

    internal_air_cubes_ls = sorted([cube.coordinates for cube in cubes_dict.values() if (set(cube.sides_dict).intersection(set([side.coordinates for side in internal_sides_ls])) and cube.cube_type=='air')],key = lambda x: x[2])
    return len(external_sides_ls)


def find_surface_area(raw_input, external_only):
    """
    determines the surface area of a droplet given an array of its component cubes
    :param external_only: only calculate external (part 2) surfaces
    :param raw_input: raw puzzle input
    :return: surface area
    """
    lava_cubes_ls = list(map(lambda x: tuple([int(y) for y in x]), [row.split(',') for row in raw_input.split('\n')]))
    if external_only:
        surface_area = calculate_external_surface_area(lava_cubes_ls)
    else:
        surface_area = calculate_exposed_surfaces(lava_cubes_ls)
    return surface_area


if __name__ == '__main__':
    # print(f"part1 surface area is {find_surface_area(data, False)}")
    print(f"part2 surface area is {find_surface_area(data, True)}")
