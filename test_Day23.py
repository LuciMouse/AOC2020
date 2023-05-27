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
        expected_elf_position_map = Day23.ElfLocationMap(
            elf_position_ls=elf_position_ls,
            bounding_rectangle_ls=[(0, 0), (0, 5), (6, 5), (6, 0)]
        )
        actual_elf_position_map = Day23.parse_input(raw_data)

        self.assertEqual(
            [expected_elf_position_map.elf_position_ls, expected_elf_position_map.bounding_rectangle_ls],
            [actual_elf_position_map.elf_position_ls, actual_elf_position_map.bounding_rectangle_ls],
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
        elf_location_map = Day23.ElfLocationMap(
            elf_position_ls=elf_position_ls,
            bounding_rectangle_ls=[(0, 0), (0, 5), (6, 5), (6, 0)]
        )
        self.assertEqual(
            [0, 0, 1, 0, 1, 0, 0, 0],
            Day23.find_surrounding_elves(0, elf_location_map)
        )


class TestDetermineProposedMove(unittest.TestCase):
    def test_determine_proposed_move(self):
        curr_elf_position = (1, 2)
        surrounding_elves_ls = [0, 0, 1, 0, 1, 0, 0, 0]
        directions_ls = [
            ((7, 0, 1), (-1, 0)),
            ((3, 4, 5), (1, 0)),
            ((5, 6, 7), (0, 1)),
            ((1, 2, 3), (0, -1))
        ]
        self.assertEqual(
            (0, 2),
            Day23.determine_proposed_move(
                curr_elf_position,
                surrounding_elves_ls,
                directions_ls
            )
        )

class TestMoveElves(unittest.TestCase):
    def test_move_elves(self):
        elf_position_ls = [
            (1, 2),
            (1, 3),
            (2, 2),
            (4, 2),
            (4, 3),
        ]

        proposed_moves_ls = [
            (0, 2),
            (0, 3),
            (3, 2),
            (3, 2),
            (3, 3)
        ]

        updated_elf_position_ls = [
            (0, 2),
            (0, 3),
            (2, 2),
            (4, 2),
            (3, 3)
        ]
        self.assertEqual(
            updated_elf_position_ls,
            Day23.move_elves(
                elf_position_ls,
                proposed_moves_ls
            )
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
