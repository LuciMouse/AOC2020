import unittest
import Day9


class test_is_touching(unittest.TestCase):
    def test_is_touching_overlapping(self):
        self.assertTrue(
            Day9.is_touching((1, 1), (1, 1))
        )

    def test_is_touching_horiz(self):
        self.assertEqual(
            [
                True,
                True,
            ],
            [
                Day9.is_touching((2, 1), (1, 1)),
                Day9.is_touching((2, 1), (3, 1))

            ]

        )

    def test_is_touching_vert(self):
        self.assertEqual(
            [
                True,
                True,

            ],
            [
                Day9.is_touching((2, 1), (2, 0)),
                Day9.is_touching((2, 1), (2, 2))
            ]

        )

    def test_is_touching_diag(self):
        self.assertEqual(
            [
                True,
                True,
                True,
                True,

            ],
            [
                Day9.is_touching((1, 2), (0, 1)),
                Day9.is_touching((1, 2), (2, 1)),
                Day9.is_touching((1, 2), (2, 3)),
                Day9.is_touching((1, 2), (0, 3))
            ]

        )


class test_move_head(unittest.TestCase):
    def test_move_head(self):
        self.assertEqual(
            [
                Day9.move_head((1, 1), "U"),
                Day9.move_head((1, 1), "D"),
                Day9.move_head((1, 1), "R"),
                Day9.move_head((1, 1), "L"),
            ],
            [
                (1, 2),
                (1, 0),
                (2, 1),
                (0, 1),

            ]
        )


class test_move_tail(unittest.TestCase):
    def test_move_tail(self):
        self.assertEqual(
            [
                Day9.move_tail((3, 1), (1, 1)),
                Day9.move_tail((1, 1), (1, 3)),
                Day9.move_tail((2, 3), (1, 1)),
                Day9.move_tail((3, 2), (1, 1))
            ],
            [
                (2, 1),
                (1, 2),
                (2, 2),
                (2, 2)
            ]
        )


class test_execute_motion(unittest.TestCase):
    def test_execute_mottion(self):
        self.assertEqual(
            [
                Day9.execute_motion(
                    (0, 0), (0, 0), {(0, 0)}, "R 4"),
                Day9.execute_motion((4, 0), (3, 0), {(0, 0), (1, 0), (2, 0), (3, 0)}, "U 4"),
                Day9.execute_motion((4, 4), (4, 3), {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3)}, "L 3"),
                Day9.execute_motion((1, 4), (2, 4),
                                    {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4)}, "D 1"),
                Day9.execute_motion(
                    (1, 3),
                    (2, 4),
                    {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4)},
                    "R 4"),
                Day9.execute_motion((5, 3), (4, 3),
                                    {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (3, 3),
                                     (4, 3)}, "D 1"),
                Day9.execute_motion((5, 2), (4, 3),
                                    {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (3, 3),
                                     (4, 3)}, "L 5"),
                Day9.execute_motion((0, 2), (1, 2),
                                    {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (3, 3),
                                     (4, 3), (3, 2),
                                     (2, 2), (1, 2)}, "R 2")
            ],
            [
                ((4, 0), (3, 0), {(0, 0), (1, 0), (2, 0), (3, 0)}),
                ((4, 4), (4, 3), {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3)}),
                ((1, 4), (2, 4), {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4)}),
                ((1, 3), (2, 4), {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4)}),
                ((5, 3), (4, 3),
                 {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (3, 3), (4, 3)}),
                ((5, 2), (4, 3),
                 {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (3, 3), (4, 3)}),
                ((0, 2), (1, 2),
                 {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (3, 3), (4, 3), (3, 2),
                  (2, 2), (1, 2)}),
                ((2, 2), (1, 2),
                 {(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (4, 3), (3, 4), (2, 4), (3, 3), (4, 3), (3, 2),
                  (2, 2), (1, 2)}),
            ]
        )


class test_execute_motion_ten_knots(unittest.TestCase):
    def test_execute_motion_ten_knots(self):
        self.assertEqual(
            [
                Day9.execute_motion_ten_knots(
                    [(0, 0) for x in range(10)],
                    {(0, 0)},
                    ["R", "4"]
                ),
                Day9.execute_motion_ten_knots(
                    [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)},
                    ["U","4"],
                ),
                Day9.execute_motion_ten_knots(
                    [(4, 4), (4, 3), (4, 2), (3, 2), (2, 2), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)},
                    ["L","3"]
                ),
                Day9.execute_motion_ten_knots(
                    [(1, 4), (2, 4), (3, 3), (3, 2), (2, 2), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)},
                    ["D","1"]
                ),
                Day9.execute_motion_ten_knots(
                    [(1, 3), (2, 4), (3, 3), (3, 2), (2, 2), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)},
                    ["R","4"]
                ),
                Day9.execute_motion_ten_knots(
                    [(0, 0) for x in range(10)],
                    {(0, 0)},
                    ["R", "5"]
                ),
                Day9.execute_motion_ten_knots(
                    [(5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)},
                    ["U","8"]
                ),
                Day9.execute_motion_ten_knots(
                    [(5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)],
                    {(0, 0)},
                    ["L", "8"]
                ),
                Day9.execute_motion_ten_knots(
                    [(-3, 8), (-2, 8), (-1, 8), (0, 8), (1, 8), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3)],
                    {(0, 0), (1, 1), (2, 2), (1, 3)},
                    ["D","3"]
                ),
                Day9.execute_motion_ten_knots(
                [(-3, 5), (-3, 6), (-2, 7), (-1, 7), (0, 7), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3)],
                {(0, 0), (1, 1), (2, 2), (1, 3)},
                    ["R","17"]
                )
            ],
            [
                (
                    [(4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)}
                ),
                (
                    [(4, 4), (4, 3), (4, 2), (3, 2), (2, 2), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)}
                ),
                (
                    [(1, 4), (2, 4), (3, 3), (3, 2), (2, 2), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)}
                ),
                (
                    [(1, 3), (2, 4), (3, 3), (3, 2), (2, 2), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)}
                ),
                (
                    [(5, 3), (4, 3), (3, 3), (3, 2), (2, 2), (1, 1), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)}
                ),
                (
                    [(5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
                    {(0, 0)}
                ),
                (
                    [(5, 8), (5, 7), (5, 6), (5, 5), (5, 4), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)],
                    {(0, 0)}
                ),
                (
                    [(-3, 8), (-2, 8), (-1, 8), (0, 8), (1, 8), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3)],
                    {(0, 0),(1,1),(2,2),(1,3)}
                ),
                (
                    [(-3, 5), (-3, 6), (-2, 7), (-1, 7), (0, 7), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3)],
                    {(0, 0), (1, 1), (2, 2), (1, 3)}
                ),
                (
                    [(14, 5), (13, 5), (12, 5), (11, 5), (10, 5), (9, 5), (8, 5), (7, 5), (6, 5), (5, 5)],
                    {(0, 0), (1, 1), (2, 2), (1, 3),(2,4),(3,5),(4,5),(5,5)}
                ),
            ]
        )


class test_find_tail_positions(unittest.TestCase):
    def test_find_tail_positions(self):
        with open("Day9_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            Day9.find_tail_positions(raw_data),
            13
        )

class test_find_ten_tail_positions(unittest.TestCase):
    def test_find_ten_tail_positions_1(self):
        with open("Day9_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            Day9.find_ten_tail_positions(raw_data),
            1
        )
    def test_find_ten_tail_positions_2(self):
        with open("Day9_test_input_2.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            Day9.find_ten_tail_positions(raw_data),
            36
        )
if __name__ == '__main__':
    unittest.main()
