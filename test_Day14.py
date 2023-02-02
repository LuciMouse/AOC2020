import unittest
import Day14


class TestFindDecoderKey(unittest.TestCase):
    def test_decoder_key(self):
        with open("Day13_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            140,
            Day13.find_decoder_key(raw_data)
        )

if __name__ == '__main__':
    unittest.main()
