import unittest
import Day14


class TestFindDecoderKey(unittest.TestCase):
    def test_sand_counter(self):
        with open("Day14_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            24,
            Day14.sand_counter(raw_data)
        )

if __name__ == '__main__':
    unittest.main()
