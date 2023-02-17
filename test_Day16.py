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
                'BB': {'CC': 2},
                'CC': {'DD': 2, 'BB': 2},
                'DD': {'CC': 2, 'EE': 2},
                'EE': {'DD': 2}, 'HH': {},
                'JJ': {}
            },
            Day16.make_valve_dist_dict(valve_dict)
        )


class TestDistanceToValve(unittest.TestCase):
    def test_distance_to_valve(self):
        with open("Day16_test_input.txt") as input_file:
            raw_data = input_file.read()
        valve_dict = Day16.parse_input(raw_data)
        valve_dist_dict = Day16.make_valve_dist_dict(valve_dict)

        # need to use deepcopy since the dictionary can get edited
        self.assertEqual(
            [
                (2, {
                    'BB': {'CC': 2},
                    'CC': {'DD': 2, 'BB': 2},
                    'DD': {'CC': 2, 'EE': 2},
                    'EE': {'DD': 2},
                    'HH': {},
                    'JJ': {}
                }),
                (2, {
                    'BB': {'CC': 2},
                    'CC': {'DD': 2, 'BB': 2},
                    'DD': {'CC': 2, 'EE': 2},
                    'EE': {'DD': 2},
                    'HH': {},
                    'JJ': {}
                }),
                (3, {
                    'BB': {'CC': 2, 'DD': 3},
                    'CC': {'DD': 2, 'BB': 2},
                    'DD': {'CC': 2, 'EE': 2},
                    'EE': {'DD': 2},
                    'HH': {},
                    'JJ': {}
                }),
                (6, {
                    'BB': {'CC': 2},
                    'CC': {'DD': 2, 'BB': 2, 'HH': 6},
                    'DD': {'CC': 2, 'EE': 2},
                    'EE': {'DD': 2},
                    'HH': {},
                    'JJ': {}
                }),
            ],
            [
                Day16.distance_to_valve("DD", "CC", valve_dict, copy.deepcopy(valve_dist_dict)),  # in dictionary
                Day16.distance_to_valve("AA", "DD", valve_dict, copy.deepcopy(valve_dist_dict)),  # in child_valves
                Day16.distance_to_valve("BB", "DD", valve_dict, copy.deepcopy(valve_dist_dict)),  # need to step
                Day16.distance_to_valve("CC", "HH", valve_dict, copy.deepcopy(valve_dist_dict)),  # need to step
            ]
        )
class TestHighestAccessibeNode(unittest.TestCase):
    def test_highest_accessible_node(self):
        sorted_valve_values = [
            ('JJ', (546, 3)),
            ('DD', (540, 2)),
            ('HH', (506, 6)),
            ('BB', (351, 2)),
            ('EE', (78, 3)),
            ('CC', (52, 3))
        ]
        self.assertEqual(
            [
                ('JJ', (567, 3)),
                ('DD', (560, 2)),
                None,
            ],
            [
                Day16.highest_accessible_node(sorted_valve_values, 30),
                Day16.highest_accessible_node(sorted_valve_values, 2),
                Day16.highest_accessible_node(sorted_valve_values, 1),
            ]
        )

class TestCalculateValveValue(unittest.TestCase):
    def test_calculate_valve_value(self):
        with open("Day16_test_input.txt") as input_file:
            raw_data = input_file.read()
        valve_dict = Day16.parse_input(raw_data)
        valve_dist_dict = Day16.make_valve_dist_dict(valve_dict)
        self.assertEqual(
            [
                (540, 2),
                (338, 3),
            ],
            [
                Day16.calculate_valve_value("AA", "DD", 30, valve_dict, valve_dist_dict),
                Day16.calculate_valve_value("DD", "BB", 30, valve_dict, valve_dist_dict)
            ]
        )
class TestCalculatePathPressure(unittest.TestCase):
    def test_calculate_path_pressure(self):
        with open("Day16_test_input.txt") as input_file:
            raw_data = input_file.read()
        valve_dict = Day16.parse_input(raw_data)
        valve_dist_dict = Day16.make_valve_dist_dict(valve_dict)
        self.assertEqual(
            [
                1533,
                1651,
            ],
            [
                Day16.calculate_path_pressure(
                    ['DD', 'JJ', 'HH', 'BB'],
                    30,
                    valve_dict,
                    valve_dist_dict,
                ),
                Day16.calculate_path_pressure(
                    ['DD', 'BB', 'JJ', 'HH','EE','CC'],
                    30,
                    valve_dict,
                    valve_dist_dict,
                )
            ]
        )
class TestCreatePathGenerator(unittest.TestCase):
    def test_create_path_generator(self):
        self.assertEqual(
            set(Day16.create_path_generator({'BB', 'HH', 'DD'}, {'CC', 'EE'})),
            {
                ('BB', 'HH', 'DD', 'CC', 'EE'),
                ('BB', 'HH', 'DD', 'EE', 'CC'),
                ('HH', 'DD', 'BB', 'CC', 'EE'),
                ('HH', 'DD', 'BB', 'EE', 'CC'),
                ('DD', 'BB', 'HH', 'CC', 'EE'),
                ('DD', 'BB', 'HH', 'EE', 'CC'),
                ('DD', 'HH', 'BB', 'CC', 'EE'),
                ('DD', 'HH', 'BB', 'EE', 'CC'),
                ('HH', 'BB', 'DD', 'CC', 'EE'),
                ('HH', 'BB', 'DD', 'EE', 'CC'),
                ('BB', 'DD', 'HH', 'CC', 'EE'),
                ('BB', 'DD', 'HH', 'EE', 'CC'),
            }
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
