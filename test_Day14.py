import unittest
import Day14

class TestDiagramRockPath(unittest.TestCase):
    def test_diagram_rock_path_no_floor(self):
        self.assertEqual(
            ([
                [*'......+...'],
                [*'..........'],
                [*'..........'],
                [*'..........'],
                [*'....#...##'],
                [*'....#...#.'],
                [*'..###...#.'],
                [*'........#.'],
                [*'........#.'],
                [*'#########.'],
            ],
                494),

            Day14.diagram_rock_path([
                [[498, 4], [498, 6], [496, 6]],
                [[503, 4], [502, 4], [502, 9], [494, 9]]
            ],
                (500, 0),
                False,
            )
        )

    def test_diagram_rock_path_with_floor(self):
        self.assertEqual(
            ([
                 [*'......+...'],
                 [*'..........'],
                 [*'..........'],
                 [*'..........'],
                 [*'....#...##'],
                 [*'....#...#.'],
                 [*'..###...#.'],
                 [*'........#.'],
                 [*'........#.'],
                 [*'#########.'],
                 [*'..........'],
                 [*'##########'],
             ],
             494),

            Day14.diagram_rock_path([
                [[498, 4], [498, 6], [496, 6]],
                [[503, 4], [502, 4], [502, 9], [494, 9]]
            ],
                (500, 0),
                True,
            )
        )
class TestDropSand(unittest.TestCase):
    def test_drop_sand(self):
        self.assertEqual(
            ((500, 8), False),
            Day14.drop_sand(
                [
                    [*'......+...'],
                    [*'..........'],
                    [*'..........'],
                    [*'..........'],
                    [*'....#...##'],
                    [*'....#...#.'],
                    [*'..###...#.'],
                    [*'........#.'],
                    [*'........#.'],
                    [*'#########.'],
                ],
                (500,0),
                494
            )
        )

class TestAddSand(unittest.TestCase):
    def test_add_sand_nofloor(self):
        self.assertEqual(
            24,
            Day14.add_sand(
                [
                    [*'......+...'],
                    [*'..........'],
                    [*'..........'],
                    [*'..........'],
                    [*'....#...##'],
                    [*'....#...#.'],
                    [*'..###...#.'],
                    [*'........#.'],
                    [*'........#.'],
                    [*'#########.'],
                ],
                (500,0),
                494,
                False
            )
        )
    def test_add_sand_withfloor(self):
        self.assertEqual(
            93,
            Day14.add_sand(
                [
                    [*'......+...'],
                    [*'..........'],
                    [*'..........'],
                    [*'..........'],
                    [*'....#...##'],
                    [*'....#...#.'],
                    [*'..###...#.'],
                    [*'........#.'],
                    [*'........#.'],
                    [*'#########.'],
                ],
                (500,0),
                494,
                True
            )
        )

class TestSandCounter(unittest.TestCase):
    def test_sand_counter_no_floor(self):
        with open("Day14_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            24,
            Day14.sand_counter(raw_data, False)
        )

    def test_sand_counter_floor(self):
        with open("Day14_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            93,
            Day14.sand_counter(raw_data, True)
        )

if __name__ == '__main__':
    unittest.main()
