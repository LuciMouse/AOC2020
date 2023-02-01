import unittest
import Day11


class TestMonkey(unittest.TestCase):
    def test_new_monkey(self):
        monkey_0 = Day11.monkey(
            0,
            [79, 98],
            "old * 19",
            (23, 1, 3)
        )

        monkey_2 = Day11.monkey(
            2,
            [79, 60, 97],
            "old * old",

        )
        monkey_3 = Day11.monkey(
            3,
            [79, 98],
            "old + 3",

        )
        old = 3

        self.assertEqual(
            [monkey_0.monkey_number, monkey_0.starting_items, eval(monkey_0.operation), monkey_0.test(11)],
            [0, [79, 98], 57, 3])


class TestMakeMonkey(unittest.TestCase):
    def test_make_monkey(self):
        monkey_0 = Day11.monkey(
            0,
            [79, 98],
            "old * 19",
            (23, 2, 3)
        )
        test_monkey = Day11.make_monkey(
            "Monkey 0:\nStarting items: 79, 98\nOperation: new = old * 19\nTest: divisible by 23\nIf true: throw to monkey 2\nIf false: throw to monkey 3"
        )
        self.assertEqual(
            [monkey_0.monkey_number, monkey_0.starting_items, monkey_0.operation, monkey_0.test(11)],
            [test_monkey.monkey_number, test_monkey.starting_items, test_monkey.operation, test_monkey.test(11)]

        )
class TestMonkeyTurn(unittest.TestCase):
    def test_monkey_turn(self):
        monkey_ls = [
            Day11.monkey(
                0,
                [79, 98],
                "old * 19",
                (23, 2, 3)
            ),
            Day11.monkey(
                1,
                [54, 65, 75, 74],
                "old + 6",
                (19, 2, 0)
            ),
            Day11.monkey(
                2,
                [79, 60, 97],
                "old * old",
                (13, 1, 3)
            ),
            Day11.monkey(
                3,
                [74],
                "old + 3",
                (17, 0, 1)
            ),
        ]
        updated_monkey_items = [
            [],
            [54, 65, 75, 74],
            [79, 60, 97],
            [74, 500, 620],
        ]
        self.assertEqual(
            updated_monkey_items,
            [x.starting_items for x in Day11.monkey_turn(0,monkey_ls)]
        )
class TestRoundImplementer(unittest.TestCase):
    def test_round_implementer(self):
        monkey_ls = [
            Day11.monkey(
                0,
                [79, 98],
                "old * 19",
                (23, 2, 3)
            ),
            Day11.monkey(
                1,
                [54, 65, 75, 74],
                "old + 6",
                (19, 2, 0)
            ),
            Day11.monkey(
                2,
                [79, 60, 97],
                "old * old",
                (13, 1, 3)
            ),
            Day11.monkey(
                3,
                [74],
                "old + 3",
                (17, 0, 1)
            ),
        ]
        item_count_ls = [0, 0, 0, 0]
        updated_monkey_items = [
            [20, 23, 27, 26],
            [2080, 25, 167, 207, 401, 1046],
            [],
            [],
        ]
        self.assertEqual(
            updated_monkey_items,
            [x.starting_items for x in Day11.round_implementer(monkey_ls, item_count_ls)[0]]
        )

class TestCalculateMonkeyBusiness(unittest.TestCase):
    def test_calculate_monkey_business(self):
        with open("Day11_test_input.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            2713310158,
            Day11.calculate_monkey_business(raw_input, 20),
        )


if __name__ == '__main__':
    unittest.main()
