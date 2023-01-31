import unittest
import Day10


class TestFindRegisterValueAtCycle(unittest.TestCase):
    def test_find_register_value_at_cycle(self):
        with open('Day10_test_input.txt') as input_file:
            raw_data = input_file.read()
        instruction_ls = raw_data.split('\n')
        cycle_register_ls = Day10.interpret_instruction_ls(instruction_ls)
        self.assertEqual(
            [
                21,
                19,
                18,
                21,
                16,
                18,
            ],
            [
                Day10.find_register_value_at_cycle(x,cycle_register_ls) for x in range(20,len(cycle_register_ls),40)
            ],
        )

class TestSignalStrengthAnalyzer(unittest.TestCase):
    def test_signal_strength_analyzer(self):
        with open('Day10_test_input.txt') as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            13140,
            Day10.signal_strength_analyzer(raw_data)
        )
class TestSpriteTracker(unittest.TestCase):
    def test_sprite_tracker(self):
        with open('Day10_test_input.txt') as input_file:
            raw_data = input_file.read()
        instruction_ls = raw_data.split('\n')
        cycle_register_ls = Day10.interpret_instruction_ls(instruction_ls)
        self.assertEqual(
            [
                [*"##..##..##..##..##..##..##..##..##..##.."],
                [*"###...###...###...###...###...###...###."],
                [*"####....####....####....####....####...."],
                [*"#####.....#####.....#####.....#####....."],
                [*"######......######......######......####"],
                [*"#######.......#######.......#######....."],
            ],
            Day10.sprite_tracker(cycle_register_ls)
        )

if __name__ == '__main__':
    unittest.main()
