import unittest
import pandas as pd
import Day8


class test_is_visible(unittest.TestCase):
    def test_location(self):
        with open("Day8_test_input.txt") as input_file:
            split_data = [y for y in input_file.read().split("\n")]

        grid_df = pd.DataFrame([[*x] for x in split_data]).applymap(lambda x: int(x))
        coord_list = [(x,y) for x in range(1,grid_df.index.size-1) for y in range(1,grid_df.columns.size-1)]
        self.assertEqual(
            list(map(lambda x: Day8.is_visible(grid_df,x),coord_list)),
            [True, True, False, True, False, True, False, True, False]
        )

class test_num_visible(unittest.TestCase):
    def test_num_visible_1(self):
        with open("Day8_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            Day8.num_visible(raw_data),
            21
        )

class test_calculate_scenic_score(unittest.TestCase):
    def test_calculate_scenic_score_1(self):
        with open("Day8_test_input.txt") as input_file:
            split_data = [y for y in input_file.read().split("\n")]

        grid_df = pd.DataFrame([[*x] for x in split_data]).applymap(lambda x: int(x))
        self.assertEqual(
            [
                Day8.calculate_scenic_score(grid_df,(1,2)),
                Day8.calculate_scenic_score(grid_df,(3,2)),
                Day8.calculate_scenic_score(grid_df, (0, 2)),
                Day8.calculate_scenic_score(grid_df, (1, 4)),
                Day8.calculate_scenic_score(grid_df, (4, 2)),
                Day8.calculate_scenic_score(grid_df, (1, 0)),
            ],
            [
                4,
                8,
                0,
                0,
                0,
                0,
            ]
        )
class test_max_scenic_score(unittest.TestCase):
    def test_max_scenic_score_1(self):
        with open("Day8_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            Day8.max_scenic_score(raw_data),
            8
        )
if __name__ == '__main__':
    unittest.main()
