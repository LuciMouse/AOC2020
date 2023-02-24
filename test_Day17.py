import unittest
from aocd import data
import Day17


class TestMakeJetPatternGenerator(unittest.TestCase):
    def test_make_jet_pattern_generator(self):
        with open("Day17_test_input.txt") as input_file:
            raw_input = input_file.read()
        jet_pattern_gen = Day17.make_jet_pattern_generator(raw_input)
        # this is an infinite generator, so test just past the repeat point 43
        i = 0
        output_str = ""
        while i < 43:
            output_str += next(jet_pattern_gen)
            i += 1
        self.assertEqual(
            ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>>>>",
            output_str
        )


class TestMakeRockGenerator(unittest.TestCase):
    def test_make_rock_generator(self):
        rock_gen = Day17.make_rock_generator()

        i = 0
        output_str = ""
        while i < 12:
            output_str += next(rock_gen).name
            i += 1
        self.assertEqual(
            "-+LI.-+LI.-+",
            output_str
        )


class TestDrawChamber(unittest.TestCase):
    def test_draw_chamber(self):
        curr_rock = Day17.FallingRock(
            '-',
            {
                (2, 3),
                (3, 3),
                (4, 3),
                (5, 3),
            }
        )
        top_layer = {(x, -1) for x in range(7)}  # points that form the "path" of blocking rock
        chamber_ls = Day17.draw_chamber(curr_rock, top_layer)
        for row in chamber_ls:
            print(row)
        self.assertEqual(
            [
                '..@@@@.',
                '.......',
                '.......',
                '.......',
                '-------',

            ],
            chamber_ls
        )

class TestNewCycle(unittest.TestCase):
    def test_new_cycle(self):
        """
        creates a new cycle
        :return:
        """
        curr_step = 4
        step_nodes = {(2, 2), (1, 1), (3, 2)}
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
        ]
        start_index = step_rock_nodes_ls.index(step_nodes)
        top_point = 30
        step_height_all_ls = [
            17,
            20,
            23,
            25,
        ]
        self.assertEqual(
            [
                (
                    1,
                    1,
                    3,
                    1,
                    [20, 30],
                    [20, 23, 25]
                )
            ],
            Day17.new_cycle(
                start_index,
                curr_step,
                top_point,
                step_height_all_ls
            )
        )
class TestBrokenCycle(unittest.TestCase):
    def test_broken_cycle_existing(self):
        """with existing step_nodes"""
        curr_step = 5
        step_nodes = {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)}
        curr_cycle = (
            1,
            1,
            3,
            1,
            [20, 30],
            [20, 23, 25]
        )
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
        ]
        top_point = 35
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
        ]
        self.assertEqual(
            [
                (
                    1,
                    5,
                    5,
                    1,
                    [20, 30],
                    [20, 23, 25, 30, 35]
                ),
                (
                    3,
                    3,
                    4,
                    1,
                    [25, 35],
                    [25, 30]
                )
            ]
            ,
            Day17.broken_cycle(
                curr_step,
                step_nodes,
                curr_cycle,
                step_rock_nodes_ls,
                top_point,
                step_height_all_ls
            )
        )
    def test_broken_cycle_new(self):
        """where step_nodes does not exist in step_rock_nodes"""
        curr_step = 7
        step_nodes = {(3, 1), (2, 7), (3, 5)},
        curr_cycle = (
            1,
            3,
            3,
            1,
            [20, 30],
            [20, 23, 25]
        )
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},

        ]
        top_point = 38
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
            33,
            35,
        ]
        self.assertEqual(
            [
                (
                    1,
                    7,
                    7,
                    1,
                    [20, 30],
                    [20, 23, 25, 30, 33, 35, 38]
                )
            ]
            ,
            Day17.broken_cycle(
                curr_step,
                step_nodes,
                curr_cycle,
                step_rock_nodes_ls,
                top_point,
                step_height_all_ls
            )
        )

class TestSingleCycle(unittest.TestCase):
    def test_try_single_cycle_complete_cycle(self):
        # define end of cycle
        curr_step = 7
        step_nodes = {(2, 2), (1, 1), (3, 2)}
        curr_cycle = (
            1,
            3,
            3,
            1,
            [20, 30],
            [20, 23, 25]
        )
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            ]

        top_point = 40
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
            33,
            35,
        ]
        self.assertEqual(
            [
                (
                    1,
                    1,
                    3,
                    2,
                    [20, 30, 40],
                    [20, 23, 25]
                )
            ],
            Day17.try_single_cycle(
                curr_step,
                step_nodes,
                curr_cycle,
                step_rock_nodes_ls,
                top_point,
                step_height_all_ls,
            )
        )
    def test_try_single_cycle_extend(self):
        curr_step = 5
        step_nodes = {(4, 2), (1, 0), (3, 5), (2, 7)}
        curr_cycle = (
                        1,
                        1,
                        3,
                        1,
                        [20, 30],
                        [20, 23, 25],
                    )
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
        ]
        top_point = 33
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
        ]
        self.assertEqual(
            [
                (
                    1,
                    2,
                    3,
                    1,
                    [20, 30],
                    [20, 23, 25]
                )
            ]
            ,
            Day17.try_single_cycle(
                curr_step,
                step_nodes,
                curr_cycle,
                step_rock_nodes_ls,
                top_point,
                step_height_all_ls
            )
        )
    def test_try_single_cycle_break(self):
        # break pattern in the middle of the cycle
        # cycle was assumed to be ABC but is not.  Try ABCAC and CA as potential cycles
        curr_step = 5
        step_nodes = {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)}
        curr_cycle = (
                        1,
                        1,
                        3,
                        1,
                        [20, 30],
                        [20, 23, 25]
                    )
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
        ]
        top_point = 35
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
        ]
        self.assertEqual(
            [
                (
                    1,
                    5,
                    5,
                    1,
                    [20, 30],
                    [20, 23, 25, 30, 35]
                ),
                (
                    3,
                    3,
                    4,
                    1,
                    [25, 35],
                    [25, 30]
                )
            ]
            ,
            Day17.try_single_cycle(
                curr_step,
                step_nodes,
                curr_cycle,
                step_rock_nodes_ls,
                top_point,
                step_height_all_ls
            )
        )
    def test_try_single_cycle_break_cycle_new(self):
        # break the pattern at the end of the second cycle
        # The cycle is naively assumed to be ABC but is actually ABCABCD
        # This is the first appearance of 'D'
        curr_step = 7
        step_nodes = {(3, 1), (2, 7), (3, 5)},
        curr_cycle = (
                        1,
                        3,
                        3,
                        1,
                        [20, 30],
                        [20, 23, 25]
                    )
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},

        ]
        top_point = 38
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
            33,
            35,
        ]
        self.assertEqual(
            [
                (
                    1,
                    7,
                    7,
                    1,
                    [20, 30],
                    [20, 23, 25, 30, 33, 35, 38]
                )
            ]
            ,
            Day17.try_single_cycle(
                curr_step,
                step_nodes,
                curr_cycle,
                step_rock_nodes_ls,
                top_point,
                step_height_all_ls
            )
        )

    def test_try_single_cycle_break_cycle_existing(self):
        # break the pattern at the end of the second cycle
        # The cycle is naively assumed to be BCD breaks could be ABCDBCD or BCDBCDA
        # The "real" cycle includes the originally omitted node "A" as opposed to the last test that introdduced a new node so this test triggers a cycle earlier
        curr_step = 7
        step_nodes = {(2, 1), (2, 5), (3, 3)}
        curr_cycle = (
                        1,
                        3,
                        3,
                        1,
                        [20, 30],
                        [20, 23, 25]
                    )
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
        ]
        top_point = 37
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
            33,
            35,
        ]
        self.assertEqual(
            [
                (
                    1,
                    7,
                    7,
                    1,
                    [20, 30],
                    [20, 23, 25, 30, 33, 35, 37]
                ),
                (
                    0,
                    0,
                    6,
                    1,
                    [17, 37],
                    [17, 20, 23, 25, 30, 33, 35]
                )
            ]
            ,
            Day17.try_single_cycle(
                curr_step,
                step_nodes,
                curr_cycle,
                step_rock_nodes_ls,
                top_point,
                step_height_all_ls
            )
        )
class TestAnalyzeCycle(unittest.TestCase):

    def test_extend_cycle(self):
        """
        define a three step cycle
        extend the cycle
        :return:
        """
        curr_step = 5
        step_nodes = {(4, 2), (1, 0), (3, 5), (2, 7)}
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
        ]
        potential_cycles_ls = [
            (
                1,
                1,
                None,
                0,
                [20, 30],
                [20, 23, 25],
            )
        ]

        top_point = 30
        num_rocks = 100
        total_height = None
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
        ]
        num_cycles = 3

        self.assertEqual(
            (
                [
                    (
                        1,
                        2,
                        None,
                        0,
                        [20, 30],
                        [20, 23, 25]
                    )
                ],
                None,
            ),
            Day17.analyze_cycle(
                curr_step,
                step_nodes,
                step_rock_nodes_ls,
                potential_cycles_ls,
                top_point,
                num_rocks,
                total_height,
                num_cycles,
                step_height_all_ls,
            )
        )

    def test_complete_cycle(self):
        """
        define a three step cycle
        complete the cycle
        :return:
        """
        curr_step = 7
        step_nodes = {(2, 2), (1, 1), (3, 2)}
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
        ]
        potential_cycles_ls = [
            (
                1,
                3,
                3,
                1,
                [20, 30],
                [20, 23, 25]
            )
        ]
        top_point = 40
        num_rocks = 100
        total_height = None
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
            33,
            35,
        ]
        num_cycles = 3

        self.assertEqual(
            (
                [
                    (
                        1,
                        1,
                        3,
                        2,
                        [20, 30, 40],
                        [20, 23, 25]
                    )
                ],
                None,
            ),
            Day17.analyze_cycle(
                curr_step,
                step_nodes,
                step_rock_nodes_ls,
                potential_cycles_ls,
                top_point,
                num_rocks,
                total_height,
                num_cycles,
                step_height_all_ls,
            )
        )

    def test_break_cycle(self):
        """
        define a three step cycle ABC
        break the cycle in middle of cycle. ABCAC or CA as potential new cycles
        :return:
        """
        curr_step = 5
        step_nodes = {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)}
        potential_cycles_ls = [(
            1,
            1,
            3,
            1,
            [20, 30],
            [20, 23, 25]
        )]
        step_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)},
            {(2, 2), (1, 1), (3, 2)},
        ]
        top_point = 35
        num_rocks = 100
        total_height = None
        step_height_all_ls = [
            17,
            20,
            23,
            25,
            30,
        ]
        num_cycles = 3

        self.assertEqual(
            (
                [
                    (
                        1,
                        5,
                        5,
                        1,
                        [20, 30],
                        [20, 23, 25, 30, 35]
                    ),
                    (
                        3,
                        3,
                        4,
                        1,
                        [25, 35],
                        [25, 30]
                    )
                ],
                None
            ),
            Day17.analyze_cycle(
                curr_step,
                step_nodes,
                step_rock_nodes_ls,
                potential_cycles_ls,
                top_point,
                num_rocks,
                total_height,
                step_height_all_ls,
                num_cycles
            )
        )

class TestModelFallingRocks(unittest.TestCase):
    def test_model_falling_rocks_part1(self):
        with open("Day17_test_input.txt") as input_file:
            raw_input = input_file.read()

        self.assertEqual(
            3068,
            Day17.model_falling_rocks(raw_input, 2022, 3)
        )
    def test_model_falling_rocks_full_data_part1(self):
        self.assertEqual(
            3153,
            Day17.model_falling_rocks(data, 2022, 3)
        )
    def test_model_falling_rocks_part2(self):
        with open("Day17_test_input.txt") as input_file:
            raw_input = input_file.read()

        self.assertEqual(
            1514285714288,
            Day17.model_falling_rocks(raw_input, 1000000000000, 3)
        )


if __name__ == '__main__':
    unittest.main()
