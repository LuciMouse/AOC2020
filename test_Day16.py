import unittest
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
