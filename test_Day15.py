import unittest
import Day15


class TestParseInput(unittest.TestCase):
    def test_parse_input(self):
        with open("Day15_test_input.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            (
                ((2, 18), (-2, 15)),
                ((9, 16), (10, 16)),
                ((13, 2), (15, 3)),
                ((12, 14), (10, 16)),
                ((10, 20), (10, 16)),
                ((14, 17), (10, 16)),
                ((8, 7), (2, 10)),
                ((2, 0), (2, 10)),
                ((0, 11), (2, 10)),
                ((20, 14), (25, 17)),
                ((17, 20), (21, 22)),
                ((16, 7), (15, 3)),
                ((14, 3), (15, 3)),
                ((20, 1), (15, 3)),
            ),
            Day15.parse_input(raw_input)
        )


class TestBeaconExclusion(unittest.TestCase):
    def test_beacon_exclusion(self):
        with open("Day15_test_input.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            26,
            Day15.beacon_exclusion(raw_input,10)
        )

if __name__ == '__main__':
    unittest.main()
