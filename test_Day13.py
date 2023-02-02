import unittest
import Day13


class TestOrderCount(unittest.TestCase):
    def test_order_count(self):
        with open("Day13_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            13,
            Day13.order_count(raw_data)
        )

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
