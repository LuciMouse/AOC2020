from aocd import data
import ast


def compare_pair(left, right):
    """
    compares the pair of packets and determines if they are in the right order
    :param left: left item list
    :param right: right item list
    :return: bool of if the pairs are in the right order

    >>> compare_pair([],[3])
    True
    >>> compare_pair([[[]]], [[]])
    False

    >>> compare_pair([[]],[])
    False

    >>> compare_pair([1,1,3,1,1],[1,1,5,1,1])
    True

    >>> compare_pair([3],[5])
    True

    >>> compare_pair([[1],[2,3,4]],[[1],4])
    True

    >>> compare_pair([2,3,4],[4])
    True

    >>> compare_pair([9],[[8,7,6]])
    False

    >>> compare_pair([[4,4],4,4], [[4,4],4,4,4])
    True

    >>> compare_pair([7,7,7,7], [7,7,7])
    False

    >>> compare_pair([1,[2,[3,[4,[5,6,7]]]],8,9], [1,[2,[3,[4,[5,6,0]]]],8,9])
    False
    """
    # left is empty and right is not
    if (not left) and (right):
        return True

    # right is empty and left is not
    if left and (not right):
        return False

    for curr_index in range(len(left)):
        if len(right) - 1 < curr_index:  # right side ran out of items
            return False
        left_value = left[curr_index]
        right_value = right[curr_index]
        if (isinstance(left_value, list)):  # left is a list
            if (isinstance(right_value, list)):
                # both are lists
                result = compare_pair(left_value, right_value)
                if result != None:  # if it's not None
                    return result
            elif (isinstance(right_value, int)):
                # left is list, right is int
                result = compare_pair(left_value, [right_value])
                if result != None:  # if it's not None
                    return result
        elif (isinstance(left_value, int)):  # left is an int
            if (isinstance(right_value, list)):
                # left is int, right is list
                result = compare_pair([left_value], right_value)
                if result != None:  # if it's not None
                    return result
            elif isinstance(right_value, int):
                # both are int
                if left_value < right_value:
                    return True
                elif left_value > right_value:
                    return False
        else:
            raise Exception("unexpected input")

    if len(right) > len(left):  # have gone through all of left and left ran out of items
        return True
    elif len(right) == len(left):  # have gone through all of left both lists are the same length
        return None  # so we can proceed to next item in parent list


def order_count(raw_data):
    """
    takes the raw data and determines how many pairs are in the right order
    :param raw_data:
    :return: sum of the indices of the pairs out of order
    """
    data_pair_ls = [[ast.literal_eval(y) for y in sublist.split('\n')] for sublist in raw_data.split('\n\n')]
    right_order_pairs_ls = list(map(lambda pair: compare_pair(pair[0], pair[1]), data_pair_ls))
    right_order_pair_index_ls = [i+1 for i,x in enumerate(right_order_pairs_ls) if x]
    return sum(right_order_pair_index_ls)

def sort_packets(packet_ls):
    """
    sorts packet list and returns sorted list
    :param packet_ls: list of packets to sort
    :return: sorted list

    >>> sort_packets([[[4,4],4,4],[7,7,7,7],[9],[[[]]],[7,7,7]])
    [[[[]]], [[4, 4], 4, 4], [7, 7, 7], [7, 7, 7, 7], [9]]
    """
    if len(packet_ls)<=1:
        return packet_ls
    partition = packet_ls[-1]

    small_ls = []
    large_ls = []

    for value in packet_ls[:-1]:
        if compare_pair(value, partition): #value is less than partition
            small_ls.append(value)
        else: #value is larger than partition
            large_ls.append(value)

    return sort_packets(small_ls)+[partition]+sort_packets(large_ls)

def find_decoder_key(raw_data):
    """
    finds the decoder key
    :param raw_data: raw input
    :return: decoder key
    """
    divider_packets = [
            [[2]],
            [[6]],
        ]

    packet_list = [ast.literal_eval(y) for y in raw_data.replace('\n\n','\n').split('\n')]
    sorted_packet_ls = sort_packets(
        packet_list+divider_packets
    )
    divider_packet_indicies = [sorted_packet_ls.index(divider_packet)+1 for divider_packet in divider_packets]
    decoder_key = divider_packet_indicies[0]*divider_packet_indicies[1]
    return decoder_key
if __name__ == '__main__':
    print(f"sum of indices {order_count(data)}")
    print(f"decoder key is {find_decoder_key(data)}")
