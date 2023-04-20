import unittest
import Day22

class TestParseInput(unittest.TestCase):
    def test_parse_input(self):
        raw_input = "        ...#\n       .#..\n\n10R5L"
        map_ls = [
             "        ...#",
            "       .#.. ",
        ]
        directions_ls = [(10, "R"), (5, "L")]
        self.assertEqual(
            (map_ls, directions_ls),
            Day22.parse_input(raw_input)
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
