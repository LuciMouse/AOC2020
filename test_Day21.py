import unittest
import Day21


class TestMakeMonkeyDict(unittest.TestCase):
    def test_make_raw_monkey_dict(self):
        with open("Day21_test_input.txt", "r") as input_file:
            raw_data = input_file.read()
        raw_monkey_dict = {
            "root": "pppw + sjmn",
            "dbpl": "5",
            "cczh": "sllz + lgvd",
            "zczc": "2",
            "ptdq": "humn - dvpt",
            "dvpt": "3",
            "lfqf": "4",
            "humn": "5",
            "ljgn": "2",
            "sjmn": "drzm * dbpl",
            "sllz": "4",
            "pppw": "cczh / lfqf",
            "lgvd": "ljgn * ptdq",
            "drzm": "hmdt - zczc",
            "hmdt": "32",
        }
        self.assertEqual(
            raw_monkey_dict,
            Day21.make_raw_monkey_dict(raw_data))


class TestParseRawMonkey(unittest.TestCase):
    def test_parse_raw_monkey_int(self):
        raw_monkey_dict = {
            "root": "pppw + sjmn",
            "dbpl": "5",
            "cczh": "sllz + lgvd",
            "zczc": "2",
            "ptdq": "humn - dvpt",
            "dvpt": "3",
            "lfqf": "4",
            "humn": "5",
            "ljgn": "2",
            "sjmn": "drzm * dbpl",
            "sllz": "4",
            "pppw": "cczh / lfqf",
            "lgvd": "ljgn * ptdq",
            "drzm": "hmdt - zczc",
            "hmdt": "32",
        }
        parsed_monkey_dict = {}
        unparsed_monkey_dict = {}
        Day21.parse_raw_monkey(
            raw_monkey_dict,
            parsed_monkey_dict,
            unparsed_monkey_dict,
            "dbpl",
        )
        new_parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            )
        }
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_parsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in parsed_monkey_dict.values()]
        )

    def test_parse_raw_monkey_both_parents(self):
        raw_monkey_dict = {
            "root": "pppw + sjmn",
            "dbpl": "5",
            "cczh": "sllz + lgvd",
            "zczc": "2",
            "ptdq": "humn - dvpt",
            "dvpt": "3",
            "lfqf": "4",
            "humn": "5",
            "ljgn": "2",
            "sjmn": "drzm * dbpl",
            "sllz": "4",
            "pppw": "cczh / lfqf",
            "lgvd": "ljgn * ptdq",
            "drzm": "hmdt - zczc",
            "hmdt": "32",
        }
        parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            ),
            "drzm": Day21.Monkey(
                value=7,
                name="drzm"
            )
        }
        unparsed_monkey_dict = {}
        Day21.parse_raw_monkey(
            raw_monkey_dict,
            parsed_monkey_dict,
            unparsed_monkey_dict,
            "sjmn",
        )
        new_parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            ),
            "drzm": Day21.Monkey(
                value=7,
                name="drzm"
            ),
            "sjmn": Day21.Monkey(
                name="sjmn",
                value=35,
                parents=("dbpl", "drzm")
            )
        }
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_parsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in parsed_monkey_dict.values()]
        )

    def test_parse_raw_monkey_one_parent(self):
        raw_monkey_dict = {
            "root": "pppw + sjmn",
            "dbpl": "5",
            "cczh": "sllz + lgvd",
            "zczc": "2",
            "ptdq": "humn - dvpt",
            "dvpt": "3",
            "lfqf": "4",
            "humn": "5",
            "ljgn": "2",
            "sjmn": "drzm * dbpl",
            "sllz": "4",
            "pppw": "cczh / lfqf",
            "lgvd": "ljgn * ptdq",
            "drzm": "hmdt - zczc",
            "hmdt": "32",
        }
        parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            ),
        }
        unparsed_monkey_dict = {}
        Day21.parse_raw_monkey(
            raw_monkey_dict,
            parsed_monkey_dict,
            unparsed_monkey_dict,
            "sjmn",
        )
        new_parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            ),
        }
        new_unparsed_monkey_dict = {
            "sjmn": Day21.Monkey(
                name="sjmn",
                value="drzm * dbpl",
                parents=("dbpl", "drzm")
            )
        }
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_parsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in parsed_monkey_dict.values()]
        )
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_unparsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in unparsed_monkey_dict.values()]
        )

    def test_parse_raw_monkey_no_parents(self):
        raw_monkey_dict = {
            "root": "pppw + sjmn",
            "dbpl": "5",
            "cczh": "sllz + lgvd",
            "zczc": "2",
            "ptdq": "humn - dvpt",
            "dvpt": "3",
            "lfqf": "4",
            "humn": "5",
            "ljgn": "2",
            "sjmn": "drzm * dbpl",
            "sllz": "4",
            "pppw": "cczh / lfqf",
            "lgvd": "ljgn * ptdq",
            "drzm": "hmdt - zczc",
            "hmdt": "32",
        }
        parsed_monkey_dict = {}
        unparsed_monkey_dict = {}
        Day21.parse_raw_monkey(
            raw_monkey_dict,
            parsed_monkey_dict,
            unparsed_monkey_dict,
            "sjmn",
        )
        new_parsed_monkey_dict = {}
        new_unparsed_monkey_dict = {
            "sjmn": Day21.Monkey(
                name="sjmn",
                parents=("dbpl", "drzm"),
                value="drzm * dbpl",
            )
        }
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_parsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in parsed_monkey_dict.values()]
        )
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_unparsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in unparsed_monkey_dict.values()]
        )
class TestParseMonkey(unittest.TestCase):
    def test_parse_monkey_both_parents(self):
        parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            ),
            "drzm": Day21.Monkey(
                value=7,
                name="drzm"
            )
        }
        unparsed_monkey_dict = {
            "sjmn": Day21.Monkey(
                name="sjmn",
                parents=("dbpl", "drzm"),
                value="drzm * dbpl",
            )
        }
        unparsed_parents_ls = Day21.parse_monkey(
            parsed_monkey_dict,
            unparsed_monkey_dict,
            unparsed_monkey_dict["sjmn"],
        )

        new_parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            ),
            "drzm": Day21.Monkey(
                value=7,
                name="drzm"
            ),
            "sjmn": Day21.Monkey(
                name="sjmn",
                value=35,
                parents=("dbpl", "drzm")
            )
        }
        new_unparsed_monkey_dict = {}
        self.assertEqual(
            [],
            unparsed_parents_ls
        )
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_parsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in parsed_monkey_dict.values()]
        )
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_unparsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in unparsed_monkey_dict.values()]
        )
    def test_parse_monkey_one_parents(self):
        parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            ),
        }
        unparsed_monkey_dict = {
            "sjmn": Day21.Monkey(
                name="sjmn",
                parents=("dbpl", "drzm"),
                value="drzm * dbpl",
            )
        }
        unparsed_parents_ls = Day21.parse_monkey(
            parsed_monkey_dict,
            unparsed_monkey_dict,
            unparsed_monkey_dict["sjmn"],
        )

        new_parsed_monkey_dict = {
            "dbpl": Day21.Monkey(
                value=5,
                name="dbpl",
            ),
        }
        new_unparsed_monkey_dict = {
            "sjmn": Day21.Monkey(
                name="sjmn",
                parents=("dbpl", "drzm"),
                value="drzm * dbpl",
            )
        }
        self.assertEqual(
            ["drzm"],
            unparsed_parents_ls
        )
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_parsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in parsed_monkey_dict.values()]
        )
        self.assertEqual(
            [(monkey.name, monkey.value) for monkey in new_unparsed_monkey_dict.values()],
            [(monkey.name, monkey.value) for monkey in unparsed_monkey_dict.values()]
        )

class TestMonkeyMath1(unittest.TestCase):
    def test_monkey_math(self):
        with open("Day21_test_input.txt", "r") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            152,
            Day21.monkey_math1(raw_data))

class TestMonkeyMath2(unittest.TestCase):
    def test_monkey_math2(self):
        with open("Day21_test_input.txt", "r") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            301,
            Day21.monkey_math2(raw_data))

if __name__ == '__main__':
    unittest.main()
