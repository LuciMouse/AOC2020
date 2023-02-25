import unittest
import Day18

class TestFindSurfaceArea(unittest.TestCase):
    def test_find_surface_area(self):
        with open("Day18_test_input.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            64,
            Day18.find_surface_area(raw_input, False)
        )

    def test_find_external_surface_area(self):
        with open("Day18_test_input.txt") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            58,
            Day18.find_surface_area(raw_input, True)
        )



if __name__ == '__main__':
    unittest.main()
