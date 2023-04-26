import unittest
import Day22


class TestParseInput(unittest.TestCase):
    def test_parse_input(self):
        raw_input = "        ...#\n       .#..\n\n10R5L5"
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        directions_ls = [(10, 1), (5, -1), (5, 0)]
        self.assertEqual(
            (map_ls, directions_ls),
            Day22.parse_input(raw_input)
        )


class TestFirstOpenTileX(unittest.TestCase):
    def test_first_open_tile_x_1(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        self.assertEqual(
            8,
            Day22.first_tile_x(map_ls, 0)
        )
    def test_first_open_tile_x_2(self):
        map_ls = [
            "        ...#",
            "        #.. ",
        ]
        self.assertEqual(
            8,
            Day22.first_tile_x(map_ls, 1)
        )


class TestLastOpenTileX(unittest.TestCase):
    def test_last_open_tile_x_1(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        self.assertEqual(
            10,
            Day22.last_tile_x(map_ls, 1)
        )
    def test_last_open_tile_x_2(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        self.assertEqual(
            11,
            Day22.last_tile_x(map_ls, 0)
        )


class TestFirstOpenTileY(unittest.TestCase):
    def test_first_open_tile_y_1(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        self.assertEqual(
            1,
            Day22.first_tile_y(map_ls, 7)
        )

    def test_first_open_tile_y_2(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        self.assertEqual(
            0,
            Day22.first_tile_y(map_ls, 9)
        )

    def test_first_open_tile_y_3(self):
        map_ls = [
            "        ...#",
            "       .#...",
        ]
        self.assertEqual(
            0,
            Day22.first_tile_y(map_ls, 10)
        )


class TestLastOpenTileY(unittest.TestCase):
    def test_last_open_tile_y_1(self):
        map_ls = [
            "        ...#",
            "      .#..  ",
        ]
        self.assertEqual(
            0,
            Day22.last_tile_y(map_ls, 10)
        )

    def test_last_open_tile_y_2(self):
        map_ls = [
            "        ...#",
            "      .#..  ",
        ]
        self.assertEqual(
            1,
            Day22.last_tile_y(map_ls, 9)
        )

    def test_last_open_tile_y_3(self):
        map_ls = [
            "       ....#",
            "      .#..  ",
        ]
        self.assertEqual(
            1,
            Day22.last_tile_y(map_ls, 7)
        )


class TestNewFacing(unittest.TestCase):
    def test_new_facing_R(self):
        self.assertEqual(
            1,
            Day22.new_facing(0, 1)
        )

    def test_new_facing_L(self):
        self.assertEqual(
            2,
            Day22.new_facing(3, -1)
        )

    def test_new_facing_R_wrap(self):
        self.assertEqual(
            0,
            Day22.new_facing(3, 1)
        )

    def test_new_facing_L_wrap(self):
        self.assertEqual(
            3,
            Day22.new_facing(0, -1)
        )

    def test_new_facing_0(self):
        self.assertEqual(
            3,
            Day22.new_facing(3, 0)
        )


class TestTakeStep(unittest.TestCase):
    def test_take_step_simple_horiz_R(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((0, 8), 0)]

        self.assertEqual(
            (False, [((0, 8), 0), ((0, 9), 0)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_simple_horiz_L(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((0, 9), 2)]

        self.assertEqual(
            (False, [((0, 9), 2), ((0, 8), 2)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_horiz_R_block(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((1, 7), 0)]

        self.assertEqual(
            (True, [((1, 7), 0)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_horiz_L_block(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((1, 9), 2)]

        self.assertEqual(
            (True, [((1, 9), 2)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_horiz_R_index_wrap(self):
        map_ls = [
            "        ...#",
            "       ..#..",
        ]
        path_ls = [((1, 11), 0)]

        self.assertEqual(
            (False, [((1, 11), 0), ((1, 7), 0)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_horiz_L_index_wrap(self):
        map_ls = [
            "        ...#",
            ".#..        ",
        ]
        path_ls = [((1, 0), 2)]

        self.assertEqual(
            (False, [((1, 0), 2), ((1, 3), 2)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_horiz_R_space_wrap(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((1, 10), 0)]

        self.assertEqual(
            (False, [((1, 10), 0), ((1, 7), 0)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_horiz_L_space_wrap(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((1, 7), 2)]

        self.assertEqual(
            (False, [((1, 7), 2), ((1, 10), 2)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_simple_vert_U(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((1, 9), 3)]

        self.assertEqual(
            (False, [((1, 9), 3), ((0, 9), 3)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_simple_vert_D(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((0, 9), 1)]

        self.assertEqual(
            (False, [((0, 9), 1), ((1, 9), 1)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_vert_U_block(self):
        map_ls = [
            "        ...#",
            "       .#...",
        ]
        path_ls = [((1, 11), 3)]

        self.assertEqual(
            (True, [((1, 11), 3)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_vert_D_block(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((0, 8), 1)]

        self.assertEqual(
            (True, [((0, 8), 1)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_vert_U_index_wrap(self):
        map_ls = [
            "        ...#",
            "       ..#. ",
        ]
        path_ls = [((0, 10), 3)]

        self.assertEqual(
            (False, [((0, 10), 3), ((1, 10), 3)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_vert_D_index_wrap(self):
        map_ls = [
            "        ...#",
            "       ..#. ",
        ]
        path_ls = [((1, 10), 1)]

        self.assertEqual(
            (False, [((1, 10), 1), ((0, 10), 1)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_vert_U_space_wrap(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [((1, 7), 3)]

        self.assertEqual(
            (False, [((1, 7), 3), ((2, 7), 3)]),
            Day22.take_step(map_ls, path_ls)
        )

    def test_take_step_vert_D_space_wrap(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
            "       .#.  ",
        ]
        path_ls = [((1, 10), 1)]

        self.assertEqual(
            (False, [((1, 10), 1), ((0, 10), 1)]),
            Day22.take_step(map_ls, path_ls)
        )


class TestImplementInstruction(unittest.TestCase):
    def test_implement_instruction_simple_horiz_R(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((0, 8), 0)]
        instruction = (2, 1)

        self.assertEqual(
            [((0, 8), 0), ((0, 9), 0), ((0, 10), 1)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_simple_horiz_L(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((0, 10), 2)]
        instruction = (2, -1)

        self.assertEqual(
            [((0, 10), 2), ((0, 9), 2), ((0, 8), 1)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_simple_vert_U(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [((2, 10), 3)]
        instruction = (2, -1)

        self.assertEqual(
            [((2, 10), 3), ((1, 10), 3), ((0, 10), 2)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_simple_vert_D(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [((0, 10), 1)]
        instruction = (2, 1)

        self.assertEqual(
            [((0, 10), 1), ((1, 10), 1), ((2, 10), 2)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_block_horiz_R(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((0, 9), 0)]
        instruction = (2, -1)

        self.assertEqual(
            [((0, 9), 0), ((0, 10), 3)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_block_horiz_L(self):
        map_ls = [
            "        ...#",
            "      .#... ",
        ]
        path_ls = [((1, 10), 2)]
        instruction = (3, -1)

        self.assertEqual(
            [((1, 10), 2), ((1, 9), 2), ((1, 8), 1)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_block_vert_U(self):
        map_ls = [
            "        ..#.",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [((2, 10), 3)]
        instruction = (2, 1)

        self.assertEqual(
            [((2, 10), 3), ((1, 10), 0)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_block_vert_D(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [((0, 8), 1)]
        instruction = (2, 1)

        self.assertEqual(
            [((0, 8), 2)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_index_wrap_horiz_R(self):
        map_ls = [
            "        ...#",
            "       .#...",
        ]
        path_ls = [((1, 9), 0)]
        instruction = (3, -1)

        self.assertEqual(
            [((1, 9), 0), ((1, 10), 0), ((1, 11), 0), ((1, 7), 3)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_index_wrap_horiz_L(self):
        map_ls = [
            "        ...#",
            "..#...      ",
        ]
        path_ls = [((1, 1), 2)]
        instruction = (3, -1)

        self.assertEqual(
            [((1, 1), 2), ((1, 0), 2), ((1, 5), 2), ((1, 4), 1)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_index_wrap_vert_U(self):
        map_ls = [
            "        ..#.",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [((1, 9), 3)]
        instruction = (2, 1)

        self.assertEqual(
            [((1, 9), 3), ((0, 9), 3), ((2, 9), 0)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_index_wrap_vert_D(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [((0, 9), 1)]
        instruction = (3, 1)

        self.assertEqual(
            [((0, 9), 1), ((1, 9), 1), ((2, 9), 1), ((0, 9), 2)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_space_wrap_horiz_R(self):
        map_ls = [
            "        ...#",
            "     .#.... ",
        ]
        path_ls = [((1, 9), 0)]
        instruction = (3, -1)

        self.assertEqual(
            [((1, 9), 0), ((1, 10), 0), ((1, 5), 3)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_space_wrap_horiz_L(self):
        map_ls = [
            "        ...#",
            "      .#... ",
        ]
        path_ls = [((1, 6), 2)]
        instruction = (3, -1)

        self.assertEqual(
            [((1, 6), 2), ((1, 10), 2), ((1, 9), 2), ((1, 8), 1)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_space_wrap_vert_U(self):
        map_ls = [
            "        ..#.",
            "       .#.. ",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [((1, 7), 3)]
        instruction = (2, 1)

        self.assertEqual(
            [((1, 7), 3), ((3, 7), 3), ((2, 7), 0)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_space_wrap_vert_D(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
            "     .#..   ",
        ]
        path_ls = [((0, 9), 1)]
        instruction = (2, 1)

        self.assertEqual(
            [((0, 9), 1), ((1, 9), 1), ((0, 9), 2)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )

    def test_implement_instruction_1(self):
        map_ls = [
            '        ...#    ',
            '        .#..    ',
            '        #...    ',
            '        ....    ',
            '...#.......#    ',
            '........#...    ',
            '..#....#....    ',
            '..........#.    ',
            '        ...#....',
            '        .....#..',
            '        .#......',
            '        ......#.'
        ]
        path_ls = [((5, 3), 1)]
        instruction = (10, -1)

        self.assertEqual(
            [((5, 3), 1), ((6, 3), 1), ((7, 3), 0)],
            Day22.implement_instruction(
                path_ls,
                map_ls,
                instruction
            )
        )


class TestPrintPath(unittest.TestCase):
    def test_print_path(self):
        map_ls = [
            "        ..#.",
            "       .#.. ",
            "       .#.. ",
            "       .#.. ",
        ]
        path_ls = [
            ((0, 8), 0), ((0, 9), 1),
            ((1, 9), 1), ((2, 9), 1), ((3, 9), 0),
            ((3, 10), 0), ((3, 7), 3),
            ((2, 7), 3)
        ]
        path_diagram_ls = [
            "        >V#.",
            "       .#V. ",
            "       ^#V. ",
            "       ^#>> ",
        ]
        self.assertEqual(
            path_diagram_ls,
            Day22.print_path(
                map_ls,
                path_ls
            )
        )


class TestCalculatePassword(unittest.TestCase):
    def test_calculate_password(self):
        postion = ((5, 7), 0)
        self.assertEqual(
            6032,
            Day22.calculate_password(postion)
        )


class TestMonkeyMap1(unittest.TestCase):
    def test_monkey_map_1(self):
        with open("Day22_test_input.txt", "r") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            6032,
            Day22.monkey_map_1(raw_input))


if __name__ == '__main__':
    unittest.main()
