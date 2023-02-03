import unittest
import Day14

class TestDiagramRockPath(unittest.TestCase):
    def test_diagram_rock_path(self):
        self.assertEqual(
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

            Day14.diagram_rock_path([
                [['498', '4'], ['498', '6'], ['496', '6']],
                [['503', '4'], ['502', '4'], ['502', '9'], ['494', '9']]
            ]
            )
        )

class TestFindDecoderKey(unittest.TestCase):
    def test_sand_counter(self):
        with open("Day14_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            24,
            Day14.sand_counter(raw_data)
        )

if __name__ == '__main__':
    unittest.main()
