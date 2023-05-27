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
        expected_elf_location_map = Day23.ElfLocationMap(
            elf_position_ls=elf_position_ls,
            bounding_rectangle_ls=[(0, 0), (0, 5), (6, 5), (6, 0)]
        )
        actual_elf_location_map = Day23.parse_input(raw_data)

        self.assertEqual(
            [expected_elf_location_map.elf_position_ls, expected_elf_location_map.bounding_rectangle_ls],
            [actual_elf_location_map.elf_position_ls, actual_elf_location_map.bounding_rectangle_ls],
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
