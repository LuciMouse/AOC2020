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

        Day18.add_adjacent_cube_sides(
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
                    'exposed-exterior',
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
                    'exposed-exterior',
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

        Day18.add_adjacent_cube_sides(
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
                ((1, 2), 2, 2): shared_side,
            }
        )
        cubes_dict = {cube.coordinates: cube for cube in existing_cubes_ls + [lava_cube] + [adjacent_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        # make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        sides_dict_copy = deepcopy(sides_dict)

        adjacent_side_cube_coord = (1, 2, 2)
        Day18.add_adjacent_cube_sides(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (same as old side)
        sides_dict_copy[(1,2,(1,2))].side_type = 'exposed-exterior'
        adjacent_cube_copy.sides_dict[(1,2,(1,2))] = sides_dict_copy[(1,2,(1,2))]
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
                ((1, 2), 2, 2): shared_side,
            }
        )
        cubes_dict = {cube.coordinates: cube for cube in existing_cubes_ls + [lava_cube] + [adjacent_cube]}
        sides_dict = {side.coordinates: side for side in existing_sides_ls + [shared_side]}

        # make a deep copy since the originals are going to be mutated
        adjacent_cube_copy = deepcopy(adjacent_cube)
        sides_dict_copy = deepcopy(sides_dict)

        adjacent_side_cube_coord = (1, 2, 2)
        Day18.add_adjacent_cube_sides(
            adjacent_cube,
            adjacent_side_cube_coord,
            shared_side_coord,
            max_bounds_tuple,
            cubes_dict,
            sides_dict
        )
        # new side (same as old side)
        sides_dict_copy[(1, 2, (1, 2))].side_type = 'covered'
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

class TestAddAdjacentCube(unittest.TestCase):
    def test_add_adjacent_cube(self):
        self.assertEqual(
            True,
            False
        )
class TestAddLavaCube(unittest.TestCase):
    def test_add_lava_cube(self):
        self.assertEqual(
            True,
            False
        )

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


if __name__ == '__main__':
    unittest.main()
