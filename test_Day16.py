import unittest
import copy
import Day16


class TestParseInput(unittest.TestCase):
    def test_parse_input(self):
        with open("Day16_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            {
                'AA': {'flow_rate': 0, 'child_valves': ['DD', 'II', 'BB']},
                'BB': {'flow_rate': 13, 'child_valves': ['CC', 'AA']},
                'CC': {'flow_rate': 2, 'child_valves': ['DD', 'BB']},
                'DD': {'flow_rate': 20, 'child_valves': ['CC', 'AA', 'EE']},
                'EE': {'flow_rate': 3, 'child_valves': ['FF', 'DD']},
                'FF': {'flow_rate': 0, 'child_valves': ['EE', 'GG']},
                'GG': {'flow_rate': 0, 'child_valves': ['FF', 'HH']},
                'HH': {'flow_rate': 22, 'child_valves': ['GG']},
                'II': {'flow_rate': 0, 'child_valves': ['AA', 'JJ']},
                'JJ': {'flow_rate': 21, 'child_valves': ['II']},
            },
            Day16.parse_input(raw_data)
        )


class TestMakeValveDistDict(unittest.TestCase):
    def test_make_valvue_dist_dict(self):
        with open("Day16_test_input.txt") as input_file:
            raw_data = input_file.read()
        valve_dict = Day16.parse_input(raw_data)
        self.assertEqual(
            {
                'BB': {'CC': 3},
                'CC': {'DD': 3, 'BB': 3},
                'DD': {'CC': 3, 'EE': 3},
                'EE': {'DD': 3},
                'HH': {},
                'JJ': {}
            },
            Day16.make_valve_dist_dict(valve_dict)
        )


class TestTimeToOpenValve(unittest.TestCase):
    def test_time_to_open_valve(self):
        with open("Day16_test_input.txt") as input_file:
            raw_data = input_file.read()
        valve_dict = Day16.parse_input(raw_data)
        valve_dist_dict = Day16.make_valve_dist_dict(valve_dict)

        # need to use deepcopy since the dictionary can get edited
        self.assertEqual(
            [
                (3, {
                    'BB': {'CC': 3},
                    'CC': {'DD': 3, 'BB': 3},
                    'DD': {'CC': 3, 'EE': 3},
                    'EE': {'DD': 3},
                    'HH': {},
                    'JJ': {}
                }),
                (3, {
                    'BB': {'CC': 3},
                    'CC': {'DD': 3, 'BB': 3},
                    'DD': {'CC': 3, 'EE': 3},
                    'EE': {'DD': 3},
                    'HH': {},
                    'JJ': {}
                }),
                (4, {
                    'BB': {'CC': 3, 'DD': 4},
                    'CC': {'DD': 3, 'BB': 3},
                    'DD': {'CC': 3, 'EE': 3},
                    'EE': {'DD': 3},
                    'HH': {},
                    'JJ': {}
                }),
                (7, {
                    'BB': {'CC': 3},
                    'CC': {'DD': 3, 'BB': 3, 'HH': 7},
                    'DD': {'CC': 3, 'EE': 3},
                    'EE': {'DD': 3},
                    'HH': {},
                    'JJ': {}
                }),
            ],
            [
                Day16.time_to_open_valve("DD", "CC", valve_dict, copy.deepcopy(valve_dist_dict)),  # in dictionary
                Day16.time_to_open_valve("AA", "DD", valve_dict, copy.deepcopy(valve_dist_dict)),  # in child_valves
                Day16.time_to_open_valve("BB", "DD", valve_dict, copy.deepcopy(valve_dist_dict)),  # need to step
                Day16.time_to_open_valve("CC", "HH", valve_dict, copy.deepcopy(valve_dist_dict)),  # need to step
            ]
        )


class TestMaxPressureRelease(unittest.TestCase):
    def test_max_pressure_release(self):
        with open("Day16_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            1651,
            Day16.max_pressure_release(raw_data)
        )


if __name__ == '__main__':
    unittest.main()
