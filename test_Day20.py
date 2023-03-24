import unittest
import Day20


class TestShiftValue(unittest.TestCase):
    def test_shift_value_simple_1(self):
        """
        simple shift
        :return:
        """
        number_ls = [1, 2, -3, 3, -2, 0, 4]
        node_dict = Day20.make_dict(number_ls)

        shifted_node_dict = Day20.shift_value(
            0,
            node_dict
        )
        self.assertEqual(
            [2, 1, -3, 3, -2, 0, 4],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]
        )

    def test_shift_value_simple_2(self):
        """
        simple shift
        :return:
        """
        number_ls = [2, 1, -3, 3, -2, 0, 4]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            0,
            node_dict
        )
        self.assertEqual(
            [1, -3, 2, 3, -2, 0, 4],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]
        )

    def test_shift_value_simple_3(self):
        """
        simple shift
        :return:
        """
        number_ls = [2, 1, -3, 3, -2, 0, 4]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            4,
            node_dict
        )
        self.assertEqual(
            [2, 1, -2, -3, 3, 0, 4],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]

        )

    def test_shift_value_left_wrap_1(self):
        """
        wrap left
        """
        number_ls = [1, -3, 2, 3, -2, 0, 4]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            1,
            node_dict
        )
        self.assertEqual(
            [1, 2, 3, -2, -3, 0, 4],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]

        )

    def test_shift_value_left_wrap_2(self):
        """
        wrap left
        """
        number_ls = [1, 2, -2, -3, 0, 3, 4]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            2,
            node_dict
        )
        self.assertEqual(
            [1, 2, -3, 0, 3, 4, -2],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]

        )

    def test_shift_value_left_wrap_3(self):
        """
        wrap left longer than list
        """
        number_ls = [1, 2, -10, -3, 0, 3, 4]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            2,
            node_dict
        )
        self.assertEqual(
            [1, 2, -3, 0, -10, 3, 4],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]

        )

    def test_shift_value_left_wrap_4(self):
        """
        wrap left longer than list
        """
        number_ls = [1, 2, -20, -3, 0, 3, 4]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            2,
            node_dict
        )
        self.assertEqual(
            [1, 2, -3, 0, 3, 4, -20],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]

        )

    def test_shift_value_right_wrap_1(self):
        """
        wrap right
        """
        number_ls = [1, 2, -3, 0, 3, 4, -2]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            5,
            node_dict
        )
        self.assertEqual(
            [1, 2, -3, 4, 0, 3, -2],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]
        )

    def test_shift_value_right_wrap_2(self):
        """
        wrap right longer than length of list
        """
        number_ls = [1, 2, -3, 0, 3, 9, -2]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            5,
            node_dict
        )
        self.assertEqual(
            [1, 2, 9, -3, 0, 3, -2],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]

        )

    def test_shift_value_edited_dict_1(self):
        """
        present as a fresh dictionary
        :return:
        """
        number_ls = [2, 1, -3, 3, -2, 0, 4]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.shift_value(
            0,
            node_dict
        )
        self.assertEqual(
            [1, -3, 2, 3, -2, 0, 4],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]

        )

    def test_shift_value_edited_dict_2(self):
        """
        present as an edited dictionary
        :return:
        """
        number_ls = [1, 2, -3, 3, -2, 0, 4]
        node_dict = Day20.make_dict(number_ls)
        node_dict[0].current_index = 1
        node_dict[0].next_node = node_dict[2]
        node_dict[0].prev_node = node_dict[1]
        node_dict[1].current_index = 0
        node_dict[1].next_node = node_dict[0]
        node_dict[1].prev_node = node_dict[6]
        node_dict[2].prev_node = node_dict[0]
        Day20.shift_value(
            1,
            node_dict
        )
        self.assertEqual(
            [1, -3, 2, 3, -2, 0, 4],
            [node.value for node in sorted(node_dict.values(), key=lambda node: node.current_index)]

        )
        self.assertEqual(
            ['node:0, prev:6, next:2', 'node:2, prev:0, next:1', 'node:1, prev:2, next:3', 'node:3, prev:1, next:4', 'node:4, prev:3, next:5', 'node:5, prev:4, next:6', 'node:6, prev:5, next:0'],
            [f"node:{node.original_index}, prev:{node.prev_node.original_index}, next:{node.next_node.original_index}" for node in sorted(node_dict.values(), key=lambda node: node.current_index)]
        )


class TestMixFile(unittest.TestCase):
    def test_mix_file(self):
        number_ls = [1, 2, -3, 3, -2, 0, 4]
        node_dict = Day20.make_dict(number_ls)
        shifted_node_dict = Day20.mix_file(
            node_dict,
            1
        )
        self.assertEqual(
            [1, 2, -3, 4, 0, 3, -2],
            [node.value for node in sorted(shifted_node_dict.values(), key=lambda node: node.current_index)]

        )


class TestFindGroveCoordinates(unittest.TestCase):
    def test_find_grove_coordinates(self):
        with open("Day20_test_input.txt", "r") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            3,
            Day20.find_grove_coordinates(raw_input, 1)
        )


if __name__ == '__main__':
    unittest.main()
