from aocd import data


class NumberNode:
    def __init__(self, value, original_index, current_index, prev_node, next_node=None):
        self.value = value
        self.original_index = original_index
        self.current_index = current_index
        self.prev_node = prev_node
        self.next_node = next_node


def new_index(curr_index, num_shifts, max_index):
    """
    determines new index of a node
    :param num_shifts: number of indicies to shift
    :param curr_index: current index
    :param max_index: maximum possible value of the index
    :return: new index
    """
    new_index = curr_index + num_shifts
    if new_index >= 0:
        if new_index <= max_index:
            return new_index
        else:  # right wrap
            return new_index % max_index
    else:  # left wrap
        return max_index + (-(-new_index % max_index))


def shift_value(index, node_dict):
    """
    shifts number number positions in number_ls.  wraps if needed
    :param number: number to move
    :param number_ls: list to move in
    :return:shifted list
    """
    print([node.value for node in sorted(node_dict.values(), key=lambda node: node.current_index)]
          )
    print([f"node:{node.original_index}, prev:{node.prev_node.original_index}, next:{node.next_node.original_index}" for
           node in sorted(node_dict.values(), key=lambda node: node.current_index)]
          )
    start_node = node_dict[index]
    # excise start_node

    prev_node = start_node.prev_node
    next_node = start_node.next_node

    prev_node.next_node = next_node
    next_node.prev_node = prev_node

    # find new position for start_node

    value = start_node.value
    if value == 0:
        return node_dict

    max_index = len(node_dict) - 1
    target_index = new_index(start_node.current_index, value, max_index)
    if target_index == 0:
        target_index = max_index  # wraps

    num_shifts = abs(target_index - index)
    curr_node = start_node
    if target_index > index:  # shift right
        for i in range(num_shifts):
            next_node = curr_node.next_node
            next_node.current_index = new_index(next_node.current_index, -1, max_index)
            curr_node = next_node
    elif target_index < index:  # shift left
        for i in range(num_shifts):
            prev_node = curr_node.prev_node
            prev_node.current_index = new_index(prev_node.current_index, 1, max_index)
            curr_node = prev_node
        # shift to right position for insertion
        curr_node = curr_node.prev_node
    # insert node here
    next_node = curr_node.next_node

    curr_node.next_node = start_node
    next_node.prev_node = start_node

    start_node.prev_node = curr_node
    start_node.next_node = next_node
    start_node.current_index = new_index(curr_node.current_index, 1, max_index)

    return node_dict


def mix_file(node_dict, num_times):
    """
    performs all the shifts in numbers_ls num_times
    :param node_dict: dictionary of nodes
    :param num_times: number of times to mix file
    :return: mixed file
    """

    for i in range(num_times):
        for index in range(len(node_dict)):
            node_dict = shift_value(index, node_dict)
    return node_dict


def make_dict(number_ls):
    """
    makes a dictionary of nodes from the number list
    :param number_ls:
    :return: dictionary
    """
    node_dict = {}
    last_node_index = len(number_ls) - 1
    for index in range(len(number_ls)):
        value = number_ls[index]
        node_dict[index] = NumberNode(
            value=value,
            original_index=index,
            current_index=index,
            prev_node=node_dict[index - 1] if index > 0 else None,
        )
        if index > 0:
            node_dict[index - 1].next_node = node_dict[index]
    node_dict[0].prev_node = node_dict[last_node_index]
    node_dict[last_node_index].next_node = node_dict[0]
    return node_dict


def find_grove_coordinates(raw_input, num_times):
    """

    :param num_times: number of times to mix file
    :param raw_input: raw puzzle input
    :return: sum of 1000th, 2000th, 3000th numbers
    """
    number_ls = [int(x) for x in raw_input.split("\n")]
    node_dict = make_dict(number_ls)
    mixed_file = mix_file(node_dict, num_times)

    zero_index = mixed_file.index(0)
    grove_coords = [mixed_file[(x + zero_index) % len(number_ls)] for x in [1000, 2000, 3000]]
    return sum(grove_coords)


if __name__ == '__main__':
    print(f"part1: {find_grove_coordinates(data, 1)}")  # 253 too low
