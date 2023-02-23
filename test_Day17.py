import unittest
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
class TestAnalyzeCycle(unittest.TestCase):
    def test_new_list(self):
        cycle_rock_nodes_ls = [
            {(2, 1), (2, 5), (3, 3)},
            {(2, 2), (1, 1), (3, 2)},
            {(4, 2), (1, 0), (3, 5), (2, 7)},
            {(4, 18), (1, 17), (2, 1), (3, 11), (6, 2)}
        ]
        cycle_nodes = {(2, 2), (1, 1), (3, 2)}

        fingerprint_ls = []

        fingerprint_zero_cycle_index = None

        num_full_cycles = 0

        Day17.analyze_cycle(
            curr_step,
            cycle_nodes,
            cycle_rock_nodes_ls,
            fingerprint_ls,
            fingerprint_zero_cycle_index,
            num_full_cycles,
            cycle_height_ls,
            top_point,
            step_height_ls,
            cycle_length,
            num_rocks,
            total_height,
        )

class TestModelFallingRocks(unittest.TestCase):
    def test_model_falling_rocks_part1(self):
        with open("Day17_test_input.txt") as input_file:
            raw_input = input_file.read()

        self.assertEqual(
            3068,
            Day17.model_falling_rocks(raw_input, 2022)
        )
    def test_model_falling_rocks_part2(self):
        with open("Day17_test_input.txt") as input_file:
            raw_input = input_file.read()

        self.assertEqual(
            1514285714288,
            Day17.model_falling_rocks(raw_input, 1000000000000)
        )


if __name__ == '__main__':
    unittest.main()
