import unittest
import Day14

class TestDiagramRockPath(unittest.TestCase):
    def test_diagram_rock_path(self):
        self.assertEqual(
            ({
                 "origin node":set((500,0)),
                 "rock_nodes": {
                     (498, 4),
                     (498, 5),
                     (498, 6),
                     (497, 6),
                     (496, 6),
                     (503, 4),
                     (502, 4),
                     (502, 5),
                     (502, 6),
                     (502, 7),
                     (502, 8),
                     (502, 9),
                     (501, 9),
                     (500, 9),
                     (499, 9),
                     (498, 9),
                     (497, 9),
                     (496, 9),
                     (495, 9),
                     (494, 9),
                 }
             },
                {
                    "min_x":494,
                    "max_x":503,
                    "max_y":9
                }),

            Day14.diagram_rock_path([
                [[498, 4], [498, 6], [496, 6]],
                [[503, 4], [502, 4], [502, 9], [494, 9]]
            ],
                (500, 0),
            )
        )


class TestDropSand(unittest.TestCase):
    def test_drop_sand(self):
        self.assertEqual(
            ((500, 8), False),
            Day14.drop_sand(
                {
                    "origin_node": set([(500, 0)]),
                    "rock_nodes": {
                        (498, 4),
                        (498, 5),
                        (498, 6),
                        (497, 6),
                        (496, 6),
                        (503, 4),
                        (502, 4),
                        (502, 5),
                        (502, 6),
                        (502, 7),
                        (502, 8),
                        (502, 9),
                        (501, 9),
                        (500, 9),
                        (499, 9),
                        (498, 9),
                        (497, 9),
                        (496, 9),
                        (495, 9),
                        (494, 9),
                    },
                    "sand_nodes":set()
                },
                (500,0),
                {
                    "min_x": 494,
                    "max_x": 503,
                    "max_y": 9
                }
            )
        )

class TestAddSand(unittest.TestCase):
    def test_add_sand_nofloor(self):
        self.assertEqual(
            24,
            Day14.add_sand(
                {
                    "origin_node": set([(500, 0)]),
                    "rock_nodes": {
                        (498, 4),
                        (498, 5),
                        (498, 6),
                        (497, 6),
                        (496, 6),
                        (503, 4),
                        (502, 4),
                        (502, 5),
                        (502, 6),
                        (502, 7),
                        (502, 8),
                        (502, 9),
                        (501, 9),
                        (500, 9),
                        (499, 9),
                        (498, 9),
                        (497, 9),
                        (496, 9),
                        (495, 9),
                        (494, 9),
                    },
                    "sand_nodes": set()
                },
                (500,0),
                {
                    "min_x": 494,
                    "max_x": 503,
                    "max_y": 9
                },
                False
            )
        )
    def test_add_sand_withfloor(self):
        self.assertEqual(
            93,
            Day14.add_sand(
                {
                    "origin_node": set([(500, 0)]),
                    "rock_nodes": {
                        (498, 4),
                        (498, 5),
                        (498, 6),
                        (497, 6),
                        (496, 6),
                        (503, 4),
                        (502, 4),
                        (502, 5),
                        (502, 6),
                        (502, 7),
                        (502, 8),
                        (502, 9),
                        (501, 9),
                        (500, 9),
                        (499, 9),
                        (498, 9),
                        (497, 9),
                        (496, 9),
                        (495, 9),
                        (494, 9),
                    },
                    "sand_nodes": set()
                },
                (500, 0),
                {
                    "min_x": 494,
                    "max_x": 503,
                    "max_y": 9
                },
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
