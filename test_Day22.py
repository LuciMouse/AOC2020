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
class TestInitialIndex(unittest.TestCase):
    def test_initail_index_1(self):
        map_ls = [
             "        ...#",
            "       .#.. ",
        ]
        self.assertEqual(
            8,
            Day22.inital_index(map_ls)
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
class TestImplementInstruction(unittest.TestCase):
    def test_implement_instruction_simple_horiz(self):
        map_ls = [
            "        ...#",
            "       .#.. ",
        ]
        path_ls = [((0, 8), 0)]
        instruction = "2R"

        Day22.implement_instruction(
            path_ls,
            map_ls,
            instruction
        )
        self.assertEqual(
            [((0, 8), 0), ((0, 9), 0), ((0, 10), 1)],
            path_ls
        )
class TestMonkeyMap1(unittest.TestCase):
    def test_monkey_map_1(self):
        with open("Day22_test_input.txt","r") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            6032,
            Day22.monkey_map_1(raw_input))


if __name__ == '__main__':
    unittest.main()
