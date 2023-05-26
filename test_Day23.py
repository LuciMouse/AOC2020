import unittest
import Day23

class TestParseInput(unittest.TestCase):
    def test_parse_input_small(self):
        with open("Day23_test_input_small.txt") as input_file:
            raw_data = input_file.read()
        elf_position_ls = [

        ]
        self.assertEqual(
            Day23.parse_input(raw_data),
            False)


if __name__ == '__main__':
    unittest.main()
