import unittest
import Day17

class TestMakeJetPatternGenerator(unittest.TestCase):
    def test_make_jet_pattern_generator(self):
        with open("Day17_test_input.txt") as input_file:
            raw_input = input_file.read()
        jet_pattern_gen = Day17.make_jet_pattern_generator(raw_input)
        #this is an infinite generator, so test just past the repeat point 43
        i = 0
        output_str =""
        while i<43:
            output_str+= next(jet_pattern_gen)
            i+=1
        self.assertEqual(
            ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>>>>",
            output_str
        )

class TestMakeRockGenerator(unittest.TestCase):
    def test_make_rock_generator(self):
        rock_gen = Day17.make_rock_generator()

        i = 0
        output_str = ""
        while i < 12:
            output_str += next(rock_gen).name
            i += 1
        self.assertEqual(
            "-+LI.-+LI.-+",
            output_str
        )
if __name__ == '__main__':
    unittest.main()
