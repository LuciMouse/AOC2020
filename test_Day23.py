import unittest
import Day23


class TestParseInput(unittest.TestCase):
    def test_parse_input_small(self):
        with open("Day23_test_input_small.txt") as input_file:
            raw_data = input_file.read()
        elf_position_ls = [
            (1, 2),
            (1, 3),
            (2, 2),
            (4, 2),
            (4, 3),
        ]
        self.assertEqual(
            elf_position_ls,
            Day23.parse_input(raw_data),
        )


class TestFindSurroundingElves(unittest.TestCase):
    def test_find_surrounding_elves(self):
        elf_position_ls = [
            (1, 2),
            (1, 3),
            (2, 2),
            (4, 2),
            (4, 3),
        ]

        self.assertEqual(
            [0, 0, 1, 0, 1, 0, 0, 0],
            Day23.find_surrounding_elves(0, elf_position_ls)
        )


class TestDetermineSmallestRectangle(unittest.TestCase):
    def test_determine_smallest_rectangle(self):
        elf_position_ls = [
            (1, 2),
            (1, 3),
            (2, 2),
            (4, 2),
            (4, 3),
        ]


if __name__ == '__main__':
    unittest.main()
