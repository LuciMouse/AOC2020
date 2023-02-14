import unittest
import Day16

class TestParseInput(unittest.TestCase):
    def test_parse_input(self):
        with open("Day16_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            {
                'AA': {'flow_rate': 0, 'child valves': ['DD', 'II', 'BB']},
                'BB': {'flow_rate': 13, 'child valves': ['CC', 'AA']},
                'CC': {'flow_rate': 2, 'child valves': ['DD', 'BB']},
                'DD': {'flow_rate': 20, 'child valves': ['CC', 'AA', 'EE']},
                'EE': {'flow_rate': 3, 'child valves': ['FF', 'DD']},
                'FF': {'flow_rate': 0, 'child valves': ['EE', 'GG']},
                'GG': {'flow_rate': 0, 'child valves': ['FF', 'HH']},
                'HH': {'flow_rate': 22, 'child valves': ['GG']},
                'II': {'flow_rate': 0, 'child valves': ['AA', 'JJ']},
                'JJ': {'flow_rate': 21, 'child valves': ['II']},
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
