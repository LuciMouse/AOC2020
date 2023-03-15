import unittest
from copy import deepcopy
import Day18


class AddAdjacentCubeSides(unittest.TestCase):
    def test_add_side_unknown_edge_side(self):
        """
        initial lava cube, initial adjacent cube, initial side (edge air cube, but air undefined)
        """
        shared_side_coord = ((1, 2), 2, 2)
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='covered',
            flanking_cube_coordinates={
                (2, 2, 2),
                (1, 2, 2)
            }
        )
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 2),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): shared_side,
            }
        )

        adjacent_side_cube_coord = (1, 2, 1)

        max_bounds_tuple = (3, 3, 6)

        cubes_dict = {
            (2, 2, 2): lava_cube,
            (1, 2, 2): adjacent_cube
        }
        sides_dict = {
            ((1, 2), 2, 2): shared_side
        }

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # check sides_dict
        self.assertEqual(
            [
                (
                    ((1, 2), 2, 2),
                    ((1, 2), 2, 2),
                    'covered',
                    frozenset({
                        (2, 2, 2),
                        (1, 2, 2)
                    })

                ),
                (
                    (1, 2, (1, 2)),
                    (1, 2, (1, 2)),
                    'unknown',
                    frozenset({
                        (1, 2, 1),
                        (1, 2, 2)
                    })
                )
            ],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [
                (
                    ((1, 2), 2, 2),
                    ((1, 2), 2, 2),
                    'covered',
                    frozenset({
                        (2, 2, 2),
                        (1, 2, 2)
                    })

                ),
                (
                    (1, 2, (1, 2)),
                    (1, 2, (1, 2)),
                    'unknown',
                    frozenset({
                        (1, 2, 1),
                        (1, 2, 2)
                    })
                )
            ],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

    def test_add_side_edge(self):
        """
            add second side, this one is an edge side
        """
        shared_side_coord = ((1, 2), 2, 2)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='covered',
            flanking_cube_coordinates={
                (2, 2, 2),
                (1, 2, 2)
            }
        )
        adjacent_cube_side1 = Day18.Side(
            coordinates=(1, 2, (1, 2)),
            side_type='exposed-exterior',
            flanking_cube_coordinates={
                (1, 2, 1),
                (1, 2, 2)
            }
        )

        # cube objects
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 2),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): shared_side,
                (1, 2, (1, 2)): adjacent_cube_side1
            }
        )
        cubes_dict = {
            (2, 2, 2): lava_cube,
            (1, 2, 2): adjacent_cube
        }
        sides_dict = {
            ((1, 2), 2, 2): shared_side,
            (1, 2, (1, 2)): adjacent_cube_side1
        }

        adjacent_side_cube_coord = (0, 2, 2)

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side
        adjacent_cube_side2 = Day18.Side(
            coordinates=((0, 1), 2, 2),
            side_type='exposed-exterior',
            flanking_cube_coordinates={
                (0, 2, 2),
                (1, 2, 2)
            }
        )
        # check sides_dict
        self.assertEqual(
            [
                (
                    ((1, 2), 2, 2),
                    ((1, 2), 2, 2),
                    'covered',
                    frozenset({
                        (2, 2, 2),
                        (1, 2, 2)
                    })

                ),
                (
                    (1, 2, (1, 2)),
                    (1, 2, (1, 2)),
                    'exposed-exterior',
                    frozenset({
                        (1, 2, 1),
                        (1, 2, 2)
                    })
                ),
                (
                    ((0, 1), 2, 2),
                    ((0, 1), 2, 2),
                    'exposed-exterior',
                    frozenset({
                        (0, 2, 2),
                        (1, 2, 2)
                    })
                ),

            ],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [
                (
                    ((1, 2), 2, 2),
                    ((1, 2), 2, 2),
                    'covered',
                    frozenset({
                        (2, 2, 2),
                        (1, 2, 2)
                    })

                ),
                (
                    (1, 2, (1, 2)),
                    (1, 2, (1, 2)),
                    'exposed-exterior',
                    frozenset({
                        (1, 2, 1),
                        (1, 2, 2)
                    })
                ),
                (
                    ((0, 1), 2, 2),
                    ((0, 1), 2, 2),
                    'exposed-exterior',
                    frozenset({
                        (0, 2, 2),
                        (1, 2, 2)
                    })
                ),
            ],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

    def test_add_side_second_cube_air(self):
        """
            cube on other side of Side defined in test_add_side_unknown_edge_side() if it's air (only changes adjacent_cube)
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

            Day18.Cube(
                coordinates=(1, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                    (1, 2, (1, 2)): existing_sides_ls[1]
                }
            )
        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )
        cubes_dict = {cube.coordinates: cube for cube in existing_cubes_ls + [lava_cube] + [adjacent_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        # make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        sides_dict_copy = deepcopy(sides_dict)

        adjacent_side_cube_coord = (1, 2, 2)
        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (same as old side)
        sides_dict_copy[(1, 2, (1, 2))].side_type = 'exposed-exterior'
        adjacent_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]
        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

    def test_add_side_second_cube_lava(self):
        """
            cube on other side of Side defined in test_add_side_unknown_edge_side() if it's lava (changes both sides and adjacent_cube)
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

            Day18.Cube(
                coordinates=(1, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                    (1, 2, (1, 2)): existing_sides_ls[1]
                }
            )
        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )
        cubes_dict = {cube.coordinates: cube for cube in existing_cubes_ls + [lava_cube] + [adjacent_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (1, 2, 2)

        flanking_cube = cubes_dict[adjacent_side_cube_coord]

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        flanking_cube_copy = deepcopy(flanking_cube)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (changed side type)
        sides_dict_copy[(1, 2, (1, 2))].side_type = 'covered'
        adjacent_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]
        # this is needed in the test because the deepcopy means that the Side object in sides_dict_copy is no
        # longer the same object that is in flanking_cube_copy (In contrast, it is the same object in sides_dict and flanking_cube)
        flanking_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]
        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

        # check the cube on the other side of the target side (flanking cube)
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube.sides_dict.items()]
        )

    """
    Test all the permutations of sides to add
    """

    # Both sides defined
    def test_add_side_both_defined_lava_lava(self):
        """
            test all permutations where both cubes flanking the target Side (flanking_cube and adjacent_cube) are defined
            both cubes are lava
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )

        flanking_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
                (1, 2, (1, 2)): existing_sides_ls[1]
            }
        )

        cubes_dict = {cube.coordinates: cube for cube in
                      existing_cubes_ls + [lava_cube] + [adjacent_cube] + [flanking_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (1, 2, 2)

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        flanking_cube_copy = deepcopy(flanking_cube)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (changed side type)
        target_side = sides_dict_copy[(1, 2, (1, 2))]
        target_side.side_type = 'covered'
        adjacent_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]

        # this is needed in the test because the deepcopy means that the Side object in sides_dict_copy is no
        # longer the same object that is in flanking_cube_copy (In contrast, it is the same object in sides_dict and flanking_cube)
        flanking_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]
        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

        # check the cube on the other side of the target side (flanking cube)
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube.sides_dict.items()]
        )

    def test_add_side_both_defined_lava_air(self):
        """
            test all permutations where both cubes flanking the target Side (flanking_cube and adjacent_cube) are defined
           one lava one air
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )

        flanking_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
                (1, 2, (1, 2)): existing_sides_ls[1]
            }
        )

        cubes_dict = {cube.coordinates: cube for cube in
                      existing_cubes_ls + [lava_cube] + [adjacent_cube] + [flanking_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (1, 2, 2)

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        flanking_cube_copy = deepcopy(flanking_cube)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (changed side type)
        target_side = sides_dict_copy[(1, 2, (1, 2))]
        target_side.side_type = 'exposed-exterior'
        adjacent_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]

        # this is needed in the test because the deepcopy means that the Side object in sides_dict_copy is no
        # longer the same object that is in flanking_cube_copy (In contrast, it is the same object in sides_dict and flanking_cube)
        flanking_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]
        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

        # check the cube on the other side of the target side (flanking cube)
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube.sides_dict.items()]
        )

    def test_add_side_both_defined_air_lava(self):
        """
            test all permutations where both cubes flanking the target Side (flanking_cube and adjacent_cube) are defined
            both cubes are lava
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )

        flanking_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
                (1, 2, (1, 2)): existing_sides_ls[1]
            }
        )

        cubes_dict = {cube.coordinates: cube for cube in
                      existing_cubes_ls + [lava_cube] + [adjacent_cube] + [flanking_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (1, 2, 2)

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        flanking_cube_copy = deepcopy(flanking_cube)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (changed side type)
        target_side = sides_dict_copy[(1, 2, (1, 2))]
        target_side.side_type = 'exposed-exterior'
        adjacent_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]

        # this is needed in the test because the deepcopy means that the Side object in sides_dict_copy is no
        # longer the same object that is in flanking_cube_copy (In contrast, it is the same object in sides_dict and flanking_cube)
        flanking_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]
        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

        # check the cube on the other side of the target side (flanking cube)
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube.sides_dict.items()]
        )

    def test_add_side_both_defined_air_air_exterior(self):
        """
            test all permutations where both cubes flanking the target Side (flanking_cube and adjacent_cube) are defined
            both cubes are air
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )

        flanking_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
                (1, 2, (1, 2)): existing_sides_ls[1]
            }
        )

        cubes_dict = {cube.coordinates: cube for cube in
                      existing_cubes_ls + [lava_cube] + [adjacent_cube] + [flanking_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (1, 2, 2)

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        flanking_cube_copy = deepcopy(flanking_cube)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (changed side type)
        target_side = sides_dict_copy[(1, 2, (1, 2))]
        target_side.side_type = 'air-exterior'
        adjacent_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]

        # this is needed in the test because the deepcopy means that the Side object in sides_dict_copy is no
        # longer the same object that is in flanking_cube_copy (In contrast, it is the same object in sides_dict and flanking_cube)
        flanking_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]
        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

        # check the cube on the other side of the target side (flanking cube)
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube.sides_dict.items()]
        )

    def test_add_side_both_defined_air_air_interior(self):
        """
            test all permutations where both cubes flanking the target Side (flanking_cube and adjacent_cube) are defined
            both cubes are air
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-interior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )

        flanking_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
                (1, 2, (1, 2)): existing_sides_ls[1]
            }
        )

        cubes_dict = {cube.coordinates: cube for cube in
                      existing_cubes_ls + [lava_cube] + [adjacent_cube] + [flanking_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (1, 2, 2)

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        flanking_cube_copy = deepcopy(flanking_cube)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (changed side type)
        target_side = sides_dict_copy[(1, 2, (1, 2))]
        target_side.side_type = 'air-interior'
        adjacent_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]

        # this is needed in the test because the deepcopy means that the Side object in sides_dict_copy is no
        # longer the same object that is in flanking_cube_copy (In contrast, it is the same object in sides_dict and flanking_cube)
        flanking_cube_copy.sides_dict[(1, 2, (1, 2))] = sides_dict_copy[(1, 2, (1, 2))]
        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

        # check the cube on the other side of the target side (flanking cube)
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             flanking_cube.sides_dict.items()]
        )

    # only one side defined
    def test_add_side_one_defined_not_edge(self):
        """
            test all permutations where only one cube flanking the target Side (adjacent_cube) is defined
            adjacent_side_cube is not an edge cube
        """
        shared_side_coord = (2, 2, (2, 3))
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='covered',
            flanking_cube_coordinates={
                (2, 2, 2),
                (2, 2, 3)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-interior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),
            Day18.Cube(
                coordinates=(1, 2, 2),
                cube_type='lava',
                sides_dict={
                    side.coordinates: side for side in existing_sides_ls
                }
            ),

        ]

        adjacent_cube = Day18.Cube(
            coordinates=(2, 2, 3),
            cube_type='lava',
            sides_dict={
                (2, 2, (2, 3)): shared_side
            }
        )

        cubes_dict = {cube.coordinates: cube for cube in existing_cubes_ls + [adjacent_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (2, 2, 4)

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube_side(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (changed side type)
        adjacent_side_coord = (2, 2, (3, 4))

        target_side = Day18.Side(
            coordinates=adjacent_side_coord,
            side_type='unknown',
            flanking_cube_coordinates={
                (2, 2, 3),
                (2, 2, 4)
            }
        )
        sides_dict_copy[adjacent_side_coord] = target_side
        adjacent_cube_copy.sides_dict[adjacent_side_coord] = target_side

        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )

        # check the adjacent_cube object
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube_copy.sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             adjacent_cube.sides_dict.items()]
        )

    def test_add_side_cube_type_error(self):
        """
            cube type out of permitted values should throw error
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )

        flanking_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='foo',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
                (1, 2, (1, 2)): existing_sides_ls[1]
            }
        )

        cubes_dict = {cube.coordinates: cube for cube in
                      existing_cubes_ls + [lava_cube] + [adjacent_cube] + [flanking_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (1, 2, 2)

        with self.assertRaises(Exception) as context:
            Day18.add_adjacent_cube_side(
                adjacent_cube,
                adjacent_side_cube_coord,
                shared_side_coord,
                max_bounds_tuple,
                cubes_dict,
                sides_dict
            )
        self.assertTrue("cube2 type not defined" in str(context.exception))

    def test_add_side_both_defined_both_type_error(self):
        """
            test all permutations where both cubes flanking the target Side (flanking_cube and adjacent_cube) are defined
            having both types on a cube should throw error
        """
        shared_side_coord = ((1, 2), 2, 1)
        max_bounds_tuple = (3, 3, 6)

        # side objects
        shared_side = Day18.Side(
            coordinates=shared_side_coord,
            side_type='exposed-unknown',
            flanking_cube_coordinates={
                (2, 2, 1),
                (1, 2, 1)
            }
        )
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='exposed-interior',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (1, 2, 2)
                }
            ),

            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            )
        ]
        # cube objects

        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    ((1, 2), 2, 2): existing_sides_ls[0],
                }
            ),

        ]
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 1),
            cube_type='lava',
            sides_dict={
                ((1, 2), 2, 1): shared_side,
            }
        )

        adjacent_cube = Day18.Cube(
            coordinates=(1, 2, 1),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 2): existing_sides_ls[0],
            }
        )

        flanking_cube = Day18.Cube(
            coordinates=(1, 2, 2),
            cube_type='air',
            sides_dict={
                ((1, 2), 2, 1): existing_sides_ls[0],
                (1, 2, (1, 2)): existing_sides_ls[1]
            }
        )

        cubes_dict = {cube.coordinates: cube for cube in
                      existing_cubes_ls + [lava_cube] + [adjacent_cube] + [flanking_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        adjacent_side_cube_coord = (1, 2, 2)

        with self.assertRaises(Exception) as context:
            Day18.add_adjacent_cube_side(
                adjacent_cube,
                adjacent_side_cube_coord,
                shared_side_coord,
                max_bounds_tuple,
                cubes_dict,
                sides_dict
            )
        self.assertTrue("both types should not exist on the same cube" in str(context.exception))


class TestAddAdjacentCube(unittest.TestCase):
    def test_add_first_adjacent_cube(self):
        """
            add first adjacent cube
        """
        max_bounds_tuple = (3, 3, 6)

        # cube objects
        lava_cube = Day18.Cube(
            coordinates=(2, 2, 2),
            cube_type='lava',
            sides_dict={}
        )
        adjacent_cube_coord = (1, 2, 2)
        lava_cubes_ls = [(2, 2, 2), (1, 2, 2), (3, 2, 2), (2, 1, 2), (2, 3, 2), (2, 2, 1), (2, 2, 3), (2, 2, 4),
                         (2, 2, 6), (1, 2, 5), (3, 2, 5), (2, 1, 5), (2, 3, 5)]
        cubes_dict = {cube.coordinates: cube for cube in [lava_cube]}
        sides_dict = {}

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        lava_cube_copy = deepcopy(lava_cube)
        cubes_dict_copy = deepcopy(cubes_dict)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube(
            adjacent_cube_coord,
            lava_cube,
            lava_cubes_ls,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # six new sides
        new_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (1, 2, 2),
                    (2, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(1, 2, (2, 3)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 2),
                    (1, 2, 3)
                }
            ),
            Day18.Side(
                coordinates=((0, 1), 2, 2),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (0, 2, 2),
                    (1, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(1, (1, 2), 2),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 1, 2),
                    (1, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(1, (2, 3), 2),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 2),
                    (1, 3, 2)
                }
            ),
        ]

        # one new cube
        adjacent_cube = Day18.Cube(
            coordinates=adjacent_cube_coord,
            cube_type='lava',
            sides_dict={
                side.coordinates: side for side in new_sides_ls
            }
        )
        # new side (changed side type)
        lava_cube_copy.sides_dict[((1, 2), 2, 2)] = new_sides_ls[0]
        cubes_dict_copy[adjacent_cube_coord] = adjacent_cube
        cubes_dict_copy[lava_cube_copy.coordinates] = lava_cube_copy  # because the deepcopy unlinked these
        sides_dict_copy = {**sides_dict_copy, **{side.coordinates: side for side in new_sides_ls}}

        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )
        # check the lava_cube object sides_dict

        self.assertEqual(
            [
                (
                    cube.coordinates,
                    cube.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube.sides_dict.items()]
                ) for cube in [lava_cube_copy]
            ],
            [
                (
                    cube.coordinates,
                    cube.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube.sides_dict.items()]
                ) for cube in [lava_cube]
            ]
        )
        # check the cubes_dict

        self.assertEqual(
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict_copy.items()],
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict.items()
            ]
        )

    def test_add_second_adjacent_cube(self):
        """
            add second adjacent cube. non-edge
        """
        max_bounds_tuple = (3, 3, 6)
        # Side objects
        existing_sides_ls = [
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='covered',
                flanking_cube_coordinates={
                    (1, 2, 2),
                    (2, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(1, 2, (2, 3)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 2),
                    (1, 2, 3)
                }
            ),
            Day18.Side(
                coordinates=((0, 1), 2, 2),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (0, 2, 2),
                    (1, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(1, (1, 2), 2),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 1, 2),
                    (1, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(1, (2, 3), 2),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 2),
                    (1, 3, 2)
                }
            ),
        ]

        # cube objects
        existing_cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={side.coordinates: side for side in existing_sides_ls[:1]}
            ),
            Day18.Cube(
                coordinates=(1, 2, 2),
                cube_type='lava',
                sides_dict={
                    side.coordinates: side for side in existing_sides_ls
                }
            ),

        ]

        lava_cube = existing_cubes_ls[0]
        adjacent_cube_coord = (2, 2, 3)
        lava_cubes_ls = [(2, 2, 2), (1, 2, 2), (3, 2, 2), (2, 1, 2), (2, 3, 2), (2, 2, 1), (2, 2, 3), (2, 2, 4),
                         (2, 2, 6), (1, 2, 5), (3, 2, 5), (2, 1, 5), (2, 3, 5)]
        cubes_dict = {cube.coordinates: cube for cube in existing_cubes_ls}
        sides_dict = {side.coordinates: side for side in existing_sides_ls}

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        lava_cube_copy = deepcopy(lava_cube)
        cubes_dict_copy = deepcopy(cubes_dict)
        sides_dict_copy = deepcopy(sides_dict)

        Day18.add_adjacent_cube(
            adjacent_cube_coord,
            lava_cube,
            lava_cubes_ls,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # six new sides
        new_sides_ls = [
            Day18.Side(
                coordinates=(2, 2, (2, 3)),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (2, 2, 3)
                }
            ),
            Day18.Side(
                coordinates=(2, 2, (3, 4)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 2, 3),
                    (2, 2, 4)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 2, 3),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 3),
                    (2, 2, 3)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 2, 3),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 2, 3),
                    (3, 2, 3)
                }
            ),
            Day18.Side(
                coordinates=(2, (1, 2), 3),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 1, 3),
                    (2, 2, 3)
                }
            ),
            Day18.Side(
                coordinates=(2, (2, 3), 3),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 2, 3),
                    (2, 3, 3)
                }
            ),
        ]

        # one new cube
        adjacent_cube = Day18.Cube(
            coordinates=adjacent_cube_coord,
            cube_type='lava',
            sides_dict={
                side.coordinates: side for side in new_sides_ls
            }
        )
        # new side (changed side type)
        lava_cube_copy.sides_dict[(2, 2, (2, 3))] = new_sides_ls[0]
        cubes_dict_copy[adjacent_cube_coord] = adjacent_cube
        cubes_dict_copy[lava_cube_copy.coordinates] = lava_cube_copy  # because the deepcopy unlinked these
        sides_dict_copy = {**sides_dict_copy, **{side.coordinates: side for side in new_sides_ls}}

        # check sides_dict
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()]
        )
        # check the lava_cube object sides_dict

        self.assertEqual(
            [
                (
                    cube.coordinates,
                    cube.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube.sides_dict.items()]
                ) for cube in [lava_cube_copy]
            ],
            [
                (
                    cube.coordinates,
                    cube.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube.sides_dict.items()]
                ) for cube in [lava_cube]
            ]
        )
        # check the cubes_dict

        self.assertEqual(
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict_copy.items()],
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict.items()
            ]
        )


class TestAddLavaCube(unittest.TestCase):
    def test_add_first_lava_cube(self):
        lava_cube_coord = (2, 2, 1)
        lava_cubes_ls = [(2, 2, 2), (1, 2, 2), (3, 2, 2), (2, 1, 2), (2, 3, 2), (2, 2, 1), (2, 2, 3), (2, 2, 4),
                         (2, 2, 6), (1, 2, 5), (3, 2, 5), (2, 1, 5), (2, 3, 5)]
        max_bounds_tuple = (3, 3, 6)
        cubes_dict = {}
        sides_dict = {}

        Day18.add_lava_cube(
            lava_cube_coord,
            lava_cubes_ls,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        sides_ls = [
            Day18.Side(
                coordinates=(2, 2, (0, 1)),
                side_type='exposed-exterior',
                flanking_cube_coordinates={
                    (2, 2, 0),
                    (2, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, 2, (1, 2)),
                side_type='covered',
                flanking_cube_coordinates={
                    (2, 2, 1),
                    (2, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(2, 2, (2, 3)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (2, 2, 3)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 2),
                    (2, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 2, 2),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (3, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(2, (1, 2), 2),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 1, 2),
                    (2, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(2, (2, 3), 2),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (2, 3, 2)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 2, 1),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (2, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(1, 2, (0, 1)),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (1, 2, 0),
                    (1, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=((0, 1), 2, 1),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (0, 2, 1),
                    (1, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(1, (1, 2), 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 1, 1)
                }
            ),
            Day18.Side(
                coordinates=(1, (2, 3), 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 3, 1)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 2, 1),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 1),
                    (3, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(3, 2, (0, 1)),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (3, 2, 0),
                    (3, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(3, 2, (1, 2)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (3, 2, 1),
                    (3, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=((3, 4), 2, 1),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (3, 2, 1),
                    (4, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(3, (1, 2), 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (3, 1, 1),
                    (3, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(3, (2, 3), 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (3, 2, 1),
                    (3, 3, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, (1, 2), 1),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 1, 1),
                    (2, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, 1, (0, 1)),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (2, 1, 0),
                    (2, 1, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, 1, (1, 2)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 1, 1),
                    (2, 1, 2)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 1, 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 1, 1),
                    (2, 1, 1)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 1, 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 1, 1),
                    (3, 1, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, (0, 1), 1),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (2, 0, 1),
                    (2, 1, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, (2, 3), 1),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 1),
                    (2, 3, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, 3, (0, 1)),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (2, 3, 0),
                    (2, 3, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, 3, (1, 2)),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 3, 1),
                    (2, 3, 2)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 3, 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 3, 1),
                    (2, 3, 1)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 3, 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (2, 3, 1),
                    (3, 3, 1)
                }
            ),
            Day18.Side(
                coordinates=(2, (3, 4), 1),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (2, 3, 1),
                    (2, 4, 1)
                }
            ),
        ]
        new_sides_dict = {side.coordinates: side for side in sides_ls}

        cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 1),
                cube_type='lava',
                sides_dict={
                    (2, 2, (0, 1)): new_sides_dict[(2, 2, (0, 1))],
                    (2, 2, (1, 2)): new_sides_dict[(2, 2, (1, 2))],
                    ((1, 2), 2, 1): new_sides_dict[((1, 2), 2, 1)],
                    ((2, 3), 2, 1): new_sides_dict[((2, 3), 2, 1)],
                    (2, (1, 2), 1): new_sides_dict[(2, (1, 2), 1)],
                    (2, (2, 3), 1): new_sides_dict[(2, (2, 3), 1)],
                }
            ),
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='lava',
                sides_dict={
                    (2, 2, (1, 2)): new_sides_dict[(2, 2, (1, 2))],
                    (2, 2, (2, 3)): new_sides_dict[(2, 2, (2, 3))],
                    ((1, 2), 2, 2): new_sides_dict[((1, 2), 2, 2)],
                    ((2, 3), 2, 2): new_sides_dict[((2, 3), 2, 2)],
                    (2, (1, 2), 2): new_sides_dict[(2, (1, 2), 2)],
                    (2, (2, 3), 2): new_sides_dict[(2, (2, 3), 2)],
                }
            ),
            Day18.Cube(
                coordinates=(1, 2, 1),
                cube_type='air',
                sides_dict={
                    coord: new_sides_dict[coord] for coord in [
                        ((1, 2), 2, 1),
                        (1, 2, (0, 1)),
                        (1, 2, (1, 2)),
                        ((0, 1), 2, 1),
                        (1, (1, 2), 1),
                        (1, (2, 3), 1)
                    ]
                }
            ),
            Day18.Cube(
                coordinates=(3, 2, 1),
                cube_type='air',
                sides_dict={
                    coord: new_sides_dict[coord] for coord in [
                        ((2, 3), 2, 1),
                        (3, 2, (0, 1)),
                        (3, 2, (1, 2)),
                        ((3, 4), 2, 1),
                        (3, (1, 2), 1),
                        (3, (2, 3), 1),
                    ]
                }
            ),
            Day18.Cube(
                coordinates=(2, 1, 1),
                cube_type='air',
                sides_dict={
                    coord: new_sides_dict[coord] for coord in [
                        (2, (1, 2), 1),
                        (2, 1, (0, 1)),
                        (2, 1, (1, 2)),
                        ((1, 2), 1, 1),
                        ((2, 3), 1, 1),
                        (2, (0, 1), 1),

                    ]
                }
            ),
            Day18.Cube(
                coordinates=(2, 3, 1),
                cube_type='air',
                sides_dict={
                    coord: new_sides_dict[coord] for coord in [
                        (2, (2, 3), 1),
                        (2, 3, (0, 1)),
                        (2, 3, (1, 2)),
                        ((1, 2), 3, 1),
                        ((2, 3), 3, 1),
                        (2, (3, 4), 1),
                    ]
                }
            ),
        ]
        new_cubes_dict = {cube.coordinates: cube for cube in cubes_ls}

        # check sides_dict

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             new_sides_dict.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()])

        # check cubes_dict

        self.assertEqual(
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in new_cubes_dict.items()
            ],
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict.items()
            ]
        )


class TestUpdateSingleAirCubes(unittest.TestCase):
    def test_update_single_air_cube_single_cube(self):
        """
        one enclosed single air cube
        :return:
        """
        sides_ls = [
            Day18.Side(
                coordinates=(2, 2, (1, 2)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 1),
                    (2, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(2, 2, (2, 3)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (2, 2, 3)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 2, 2),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (1, 2, 2),
                    (2, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 2, 2),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (3, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(2, (1, 2), 2),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 1, 2),
                    (2, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=(2, (2, 3), 2),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 2),
                    (2, 3, 2)
                }
            )
        ]
        sides_dict = {
            side.coordinates: side for side in sides_ls
        }

        cubes_ls = [
            Day18.Cube(
                coordinates=(2, 2, 2),
                cube_type='air',
                sides_dict=sides_dict
            ),
            Day18.Cube(
                coordinates=(2, 2, 1),
                cube_type='lava',
                sides_dict={}
            ),
            Day18.Cube(
                coordinates=(2, 2, 3),
                cube_type='lava',
                sides_dict={}
            ),
            Day18.Cube(
                coordinates=(1, 2, 2),
                cube_type='lava',
                sides_dict={}
            ),
            Day18.Cube(
                coordinates=(3, 2, 2),
                cube_type='lava',
                sides_dict={}
            ),
            Day18.Cube(
                coordinates=(2, 1, 2),
                cube_type='lava',
                sides_dict={}
            ),
            Day18.Cube(
                coordinates=(2, 3, 2),
                cube_type='lava',
                sides_dict={}
            )
        ]
        cubes_dict = {
            cube.coordinates: cube for cube in cubes_ls
        }

        sides_dict_copy = deepcopy(sides_dict)
        cubes_dict_copy = deepcopy(cubes_dict)

        Day18.update_single_air_cubes(cubes_dict)

        for side in sides_dict_copy.values():
            side.side_type = 'exposed-interior'

        for cube in cubes_dict_copy.values():
            for side in cube.sides_dict.values():
                side.side_type = 'exposed-inteior'
        self.assertEqual(
            [(side_coord, side.coordinates, side.side_type, side.flanking_cube_coordinates) for side_coord, side in
             sides_dict_copy.items()],
            [(side_coord, side.coordinates, side.side_type, side.flanking_cube_coordinates) for side_coord, side in
             sides_dict.items()]
        )
        self.assertEqual(
            [(
                cube_coord, cube.coordinates, cube.cube_type,
                [side_coord for side_coord, side in cube.sides_dict.items()])
                for cube_coord, cube in cubes_dict_copy.items()],
            [(
                cube_coord, cube.coordinates, cube.cube_type,
                [side_coord for side_coord, side in cube.sides_dict.items()])
                for cube_coord, cube in cubes_dict.items()]
        )


class TestUpdateUnknownSides(unittest.TestCase):
    def test_update_unknown_sides_single_defined_cube(self):
        """
        only one of the flanking cubes are in cubes_dict
        """
        side_ls = [
            Day18.Side(
                coordinates=(1, 2, (0, 1)),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (1, 2, 0),
                    (1, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(1, 2, (1, 2)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 2, 2)
                }
            ),
            Day18.Side(
                coordinates=((0, 1), 2, 1),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (0, 2, 1),
                    (1, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 2, 1),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (2, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(1, (1, 2), 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 1, 1),
                    (1, 2, 1)
                }
            ),
            Day18.Side(
                coordinates=(1, (2, 3), 1),
                side_type='unknown',
                flanking_cube_coordinates={
                    (1, 2, 1),
                    (1, 3, 1)
                }
            ),
        ]
        sides_dict = sides_dict = {side.coordinates: side for side in side_ls}
        cube_ls = [
            Day18.Cube(
                coordinates=(1, 2, 1),
                cube_type='air',
                sides_dict={
                    side_coord: sides_dict[side_coord] for side_coord in [
                        ((0, 1), 2, 1),
                        ((1, 2), 2, 1),
                        (1, (1, 2), 1),
                        (1, (2, 3), 1),
                        (1, 2, (0, 1)),
                        (1, 2, (1, 2)),
                    ]
                }
            ),

        ]
        cubes_dict = {cube.coordinates: cube for cube in cube_ls}

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        cubes_dict_copy = deepcopy(cubes_dict)
        sides_dict_copy = deepcopy(sides_dict)

        unknown_side_coord_ls = [
            (1, (1, 2), 1),
            (1, (2, 3), 1),
        ]

        Day18.update_unknown_sides(
            sides_dict,
            cubes_dict,
            [value for key, value in sides_dict.items() if key in unknown_side_coord_ls]
        )
        for unknown_air_side_coord in unknown_side_coord_ls:
            sides_dict_copy[unknown_air_side_coord].side_type = 'air-exterior'
        for key, cube in cubes_dict_copy.items():
            for unknown_air_side_coord in unknown_side_coord_ls:
                if unknown_air_side_coord in cube.sides_dict:
                    cube.sides_dict[unknown_air_side_coord].side_type = 'air-exterior'

        # check sides_dict

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()])

        # check cubes_dict

        self.assertEqual(
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict_copy.items()
            ],
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict.items()
            ]
        )


class TestUpdateAirSides(unittest.TestCase):
    def test_update_air_sides_internal(self):
        """
        case where both air cubes flanking the 'air-unknown' face are internal
        """
        side_ls = [
            Day18.Side(
                coordinates=(2, 2, (4, 5)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 4),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, 2, (5, 6)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (2, 2, 6)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 2, 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (1, 2, 5),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 2, 5),
                side_type='air-unknown',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (3, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, (1, 2), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 1, 5),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, (2, 3), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (2, 3, 5)
                }
            ),
            Day18.Side(
                coordinates=(3, 2, (4, 5)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 4),
                    (3, 2, 5),
                }
            ),
            Day18.Side(
                coordinates=(3, 2, (5, 6)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (3, 2, 6)
                }
            ),
            Day18.Side(
                coordinates=((3, 4), 2, 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (4, 2, 5)
                }

            ),
            Day18.Side(
                coordinates=(3, (1, 2), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 1, 5),
                    (3, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(3, (2, 3), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (3, 3, 5)
                }
            )
        ]
        sides_dict = {side.coordinates: side for side in side_ls}
        cube_ls = [
            Day18.Cube(
                coordinates=(2, 2, 5),
                cube_type='air',
                sides_dict={
                    side_coord: sides_dict[side_coord] for side_coord in [
                        (2, 2, (4, 5)),
                        (2, 2, (5, 6)),
                        ((1, 2), 2, 5),
                        ((2, 3), 2, 5),
                        (2, (1, 2), 5),
                        (2, (2, 3), 5)
                    ]
                }
            ),
            Day18.Cube(
                coordinates=(3, 2, 5),
                cube_type='air',
                sides_dict={
                    side_coord: sides_dict[side_coord] for side_coord in [
                        (3, 2, (4, 5)),
                        (3, 2, (5, 6)),
                        ((2, 3), 2, 5),
                        ((3, 4), 2, 5),
                        (3, (1, 2), 5),
                        (3, (2, 3), 5)
                    ]
                }
            )
        ]
        cubes_dict = {cube.coordinates: cube for cube in cube_ls}

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        cubes_dict_copy = deepcopy(cubes_dict)
        sides_dict_copy = deepcopy(sides_dict)

        unknown_air_side_coord = ((2, 3), 2, 5)
        lava_cubes_ls = [(1, 2, 5), (4, 2, 5)] #to prevent the side from being called external

        Day18.update_air_sides(
            sides_dict,
            cubes_dict,
            [sides_dict[unknown_air_side_coord]],
            (5, 3, 6),
            lava_cubes_ls
        )
        sides_dict_copy[unknown_air_side_coord].side_type = 'air-interior'
        for key, cube in cubes_dict_copy.items():
            cube.sides_dict[unknown_air_side_coord].side_type = 'air-interior'

        # check sides_dict

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()])

        # check cubes_dict

        self.assertEqual(
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict_copy.items()
            ],
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict.items()
            ]
        )

    def test_update_air_sides_propagate_external(self):
        """
        case where 'air-external' needs to propagate in from edge. 3 cube system
        """
        side_ls = [
            Day18.Side(
                coordinates=(2, 2, (4, 5)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 4),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, 2, (5, 6)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (2, 2, 6)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 2, 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (1, 2, 5),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 2, 5),
                side_type='air-unknown',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (3, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, (1, 2), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 1, 5),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, (2, 3), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (2, 3, 5)
                }
            ),
            Day18.Side(
                coordinates=(3, 2, (4, 5)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 4),
                    (3, 2, 5),
                }
            ),
            Day18.Side(
                coordinates=(3, 2, (5, 6)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (3, 2, 6)
                }
            ),
            Day18.Side(
                coordinates=((3, 4), 2, 5),
                side_type='air-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (4, 2, 5)
                }

            ),
            Day18.Side(
                coordinates=(3, (1, 2), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 1, 5),
                    (3, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(3, (2, 3), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (3, 3, 5)
                }
            ),
            Day18.Side(
                coordinates=(4, 2, (4, 5)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (4, 2, 4),
                    (4, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(4, 2, (5, 6)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (4, 2, 5),
                    (4, 2, 6)
                }
            ),
            Day18.Side(
                coordinates=((4, 5), 2, 5),
                side_type='air-exterior',
                flanking_cube_coordinates={
                    (4, 2, 5),
                    (5, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(4, (1, 2), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (4, 1, 5),
                    (4, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(4, (2, 3), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (4, 2, 5),
                    (4, 3, 5)
                }
            )
        ]
        sides_dict = {side.coordinates: side for side in side_ls}
        cube_ls = [
            Day18.Cube(
                coordinates=(2, 2, 5),
                cube_type='air',
                sides_dict={
                    side_coord: sides_dict[side_coord] for side_coord in [
                        (2, 2, (4, 5)),
                        (2, 2, (5, 6)),
                        ((1, 2), 2, 5),
                        ((2, 3), 2, 5),
                        (2, (1, 2), 5),
                        (2, (2, 3), 5)
                    ]
                }
            ),
            Day18.Cube(
                coordinates=(3, 2, 5),
                cube_type='air',
                sides_dict={
                    side_coord: sides_dict[side_coord] for side_coord in [
                        (3, 2, (4, 5)),
                        (3, 2, (5, 6)),
                        ((2, 3), 2, 5),
                        ((3, 4), 2, 5),
                        (3, (1, 2), 5),
                        (3, (2, 3), 5)
                    ]
                }
            ),
            Day18.Cube(
                coordinates=(4, 2, 5),
                cube_type='air',
                sides_dict={
                    side_coord: sides_dict[side_coord] for side_coord in [
                        (4, 2, (4, 5)),
                        (4, 2, (5, 6)),
                        ((4, 5), 2, 5),
                        ((3, 4), 2, 5),
                        (4, (1, 2), 5),
                        (4, (2, 3), 5)
                    ]
                }
            )
        ]
        cubes_dict = {cube.coordinates: cube for cube in cube_ls}

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        cubes_dict_copy = deepcopy(cubes_dict)
        sides_dict_copy = deepcopy(sides_dict)

        unknown_air_side_coord_ls = [
            ((2, 3), 2, 5),
            ((3, 4), 2, 5)
        ]
        lava_cubes_ls = [(1, 2, 5), (5, 2, 5)]  # to prevent the side from being called external

        Day18.update_air_sides(
            sides_dict,
            cubes_dict,
            [value for key, value in sides_dict.items() if key in unknown_air_side_coord_ls],
            (5, 3, 6),
            lava_cubes_ls
        )
        for unknown_air_side_coord in unknown_air_side_coord_ls:
            sides_dict_copy[unknown_air_side_coord].side_type = 'air-exterior'
        for key, cube in cubes_dict_copy.items():
            for unknown_air_side_coord in unknown_air_side_coord_ls:
                if unknown_air_side_coord in cube.sides_dict:
                    cube.sides_dict[unknown_air_side_coord].side_type = 'air-exterior'

        # check sides_dict

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()])

        # check cubes_dict

        self.assertEqual(
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict_copy.items()
            ],
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict.items()
            ]
        )


class TestUpdateExposedSides(unittest.TestCase):
    def test_update_exposed_sides_internal(self):
        """
               case where both air cubes flanking the 'air-unknown' face are internal
               """
        side_ls = [
            Day18.Side(
                coordinates=(2, 2, (4, 5)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 4),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, 2, (5, 6)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (2, 2, 6)
                }
            ),
            Day18.Side(
                coordinates=((1, 2), 2, 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (1, 2, 5),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=((2, 3), 2, 5),
                side_type='air-interior',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (3, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, (1, 2), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 1, 5),
                    (2, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(2, (2, 3), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (2, 2, 5),
                    (2, 3, 5)
                }
            ),
            Day18.Side(
                coordinates=(3, 2, (4, 5)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 4),
                    (3, 2, 5),
                }
            ),
            Day18.Side(
                coordinates=(3, 2, (5, 6)),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (3, 2, 6)
                }
            ),
            Day18.Side(
                coordinates=((3, 4), 2, 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (4, 2, 5)
                }

            ),
            Day18.Side(
                coordinates=(3, (1, 2), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 1, 5),
                    (3, 2, 5)
                }
            ),
            Day18.Side(
                coordinates=(3, (2, 3), 5),
                side_type='exposed-unknown',
                flanking_cube_coordinates={
                    (3, 2, 5),
                    (3, 3, 5)
                }
            )
        ]
        sides_dict = {side.coordinates: side for side in side_ls}
        cube_ls = [
            Day18.Cube(
                coordinates=(2, 2, 5),
                cube_type='air',
                sides_dict={
                    side_coord: sides_dict[side_coord] for side_coord in [
                        (2, 2, (4, 5)),
                        (2, 2, (5, 6)),
                        ((1, 2), 2, 5),
                        ((2, 3), 2, 5),
                        (2, (1, 2), 5),
                        (2, (2, 3), 5)
                    ]
                }
            ),
            Day18.Cube(
                coordinates=(3, 2, 5),
                cube_type='air',
                sides_dict={
                    side_coord: sides_dict[side_coord] for side_coord in [
                        (3, 2, (4, 5)),
                        (3, 2, (5, 6)),
                        ((2, 3), 2, 5),
                        ((3, 4), 2, 5),
                        (3, (1, 2), 5),
                        (3, (2, 3), 5)
                    ]
                }
            )
        ]
        cubes_dict = {cube.coordinates: cube for cube in cube_ls}

        # Objects expected to be changed. Make a deep copy since the originals are going to be mutated
        cubes_dict_copy = deepcopy(cubes_dict)
        sides_dict_copy = deepcopy(sides_dict)

        unknown_exposed_side_dict = {key: value for key, value in sides_dict.items() if
                                     value.side_type == 'exposed-unknown'}
        Day18.update_exposed_sides(
            sides_dict,
            cubes_dict,
            unknown_exposed_side_dict.values()
        )
        for unknown_exposed_side_coord in unknown_exposed_side_dict.keys():
            sides_dict_copy[unknown_exposed_side_coord].side_type = 'exposed-interior'
        for key, cube in cubes_dict_copy.items():
            for unknown_air_side_coord in unknown_exposed_side_dict.keys():
                if unknown_air_side_coord in cube.sides_dict:
                    cube.sides_dict[unknown_air_side_coord].side_type = 'exposed-interior'

        # check sides_dict

        self.assertEqual.__self__.maxDiff = None
        self.assertEqual(
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict_copy.items()],
            [(key, value.coordinates, value.side_type, frozenset(value.flanking_cube_coordinates)) for key, value in
             sides_dict.items()])

        # check cubes_dict

        self.assertEqual(
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict_copy.items()
            ],
            [
                (
                    cube_key,
                    cube_value.coordinates,
                    cube_value.cube_type,
                    [
                        (side_key,
                         side_value.coordinates,
                         side_value.side_type,
                         frozenset(side_value.flanking_cube_coordinates)) for side_key, side_value in
                        cube_value.sides_dict.items()]
                ) for cube_key, cube_value in cubes_dict.items()
            ]
        )


class TestVisualizeDropLava(unittest.TestCase):
    def test_visualize_drop_lava_1(self):
        with open("Day18_test_input.txt") as input_file:
            raw_input = input_file.read()
        lava_cubes_ls = list(
            map(lambda x: tuple([int(y) for y in x]), [row.split(',') for row in raw_input.split('\n')]))
        max_x = max([cube[0] for cube in lava_cubes_ls])
        max_y = max([cube[1] for cube in lava_cubes_ls])
        max_z = max([cube[2] for cube in lava_cubes_ls])

        max_bounds_tuple = (max_x, max_y, max_z)

        drop_diagram_ls = Day18.visualize_drop_lava(
            lava_cubes_ls,
            max_bounds_tuple
        )

        self.assertEqual(
            [
                [
                    ['.', '.', '.'],
                    ['.', 'L', '.'],
                    ['.', '.', '.'],
                ],
                [
                    ['.', 'L', '.'],
                    ['L', 'L', 'L'],
                    ['.', 'L', '.'],
                ],
                [
                    ['.', '.', '.'],
                    ['.', 'L', '.'],
                    ['.', '.', '.'],
                ],
                [
                    ['.', '.', '.'],
                    ['.', 'L', '.'],
                    ['.', '.', '.'],
                ],
                [
                    ['.', 'L', '.'],
                    ['L', '.', 'L'],
                    ['.', 'L', '.'],
                ],
                [
                    ['.', '.', '.'],
                    ['.', 'L', '.'],
                    ['.', '.', '.'],
                ],
            ],
            drop_diagram_ls
        )
        for z in drop_diagram_ls:
            z.reverse()
            for y in z:
                print("".join(y))
            print("\n")


class TestFindSurfaceArea(unittest.TestCase):

    def test_find_surface_area(self):
        with open("Day18_test_input.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            64,
            Day18.find_surface_area(raw_input, False)
        )

    def test_find_external_surface_area(self):
        with open("Day18_test_input.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            58,
            Day18.find_surface_area(raw_input, True)
        )

    def test_find_surface_area_2(self):
        with open("Day18_test_input_2.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            80,
            Day18.find_surface_area(raw_input, False)
        )

    def test_find_external_surface_area_2(self):
        with open("Day18_test_input_2.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            70,
            Day18.find_surface_area(raw_input, True)
        )

    def test_find_surface_area_3(self):
        with open("Day18_test_input_3.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            158,
            Day18.find_surface_area(raw_input, False)
        )

    def test_find_external_surface_area_3(self):
        with open("Day18_test_input_3.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            158,
            Day18.find_surface_area(raw_input, True)
        )

    def test_find_surface_area_4(self):
        with open("Day18_test_input_4.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            658,
            Day18.find_surface_area(raw_input, False)
        )

    def test_find_external_surface_area_4(self):
        with open("Day18_test_input_4.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            640,
            Day18.find_surface_area(raw_input, True)
        )


if __name__ == '__main__':
    unittest.main()
