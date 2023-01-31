from aocd import data
def count_contained_ranges(raw_input):
    """
    counts the number of ranges that are fully contained
    :param raw_input:
    :return: count of fully contained ranges
    """
    assignment_ls = raw_input.split("\n")
    assignment_pair_ls = [convert_to_list(x) for x in assignment_ls]
    is_contained_ls = [is_fully_contained(x) for x in assignment_pair_ls]
    return sum(is_contained_ls)

def test_count_contained_ranges():
    with open("Day4_test_input.txt","r") as input_file:
        raw_test_input=input_file.read()
    assert count_contained_ranges(raw_test_input)== 2
def count_overlapped_ranges(raw_input):
    """
    counts the number of ranges that are overlapped
    :param raw_input:
    :return: count of overlapped ranges
    """
    assignment_ls = raw_input.split("\n")
    assignment_pair_ls = [convert_to_list(x) for x in assignment_ls]
    is_overlapped_ls = [is_overlapping(x) for x in assignment_pair_ls]
    return sum(is_overlapped_ls)

def test_count_overlapped_ranges():
    with open("Day4_test_input.txt","r") as input_file:
        raw_test_input=input_file.read()
    assert count_overlapped_ranges(raw_test_input)== 4

def convert_to_list(pair_string):
    """
    converts a string into a tuple of ranges
    :param pair_string: string of section assignment
    :return: tuple of section ranges

    usage examples:

    >>> convert_to_list("2-4,6-8")
    [[2, 4], [6, 8]]

    >>> convert_to_list("2-3,4-5")
    [[2, 3], [4, 5]]

    >>> convert_to_list("5-7,7-9")
    [[5, 7], [7, 9]]

    >>> convert_to_list('2-8,3-7')
    [[2, 8], [3, 7]]

    >>> convert_to_list("6-6,4-6")
    [[6, 6], [4, 6]]

    >>> convert_to_list('2-6,4-8')
    [[2, 6], [4, 8]]
    """
    pair_ls = pair_string.split(",")
    formatted_ls = list([int(y) for y in x.split("-")] for x in pair_ls)
    return formatted_ls

def is_fully_contained(range_ls):
    """
    returns if one range is fully contained inside the other
    :param range_tuple: tuple of two ranges to compare
    :return: boolean of whether one range is fully contained inside the other

    usage examples:

    >>> is_fully_contained([[2,4],[6,8]])
    False

    >>> is_fully_contained([[2,3],[4,5]])
    False

    >>> is_fully_contained([[5,7],[7,9]])
    False

    >>> is_fully_contained([[2,8],[3,7]])
    True

    >>> is_fully_contained([[6,6],[4,6]])
    True

    >>> is_fully_contained([[2,6],[4,8]])
    False
    """
    if ((range_ls[0][0]<=range_ls[1][0]) & (range_ls[0][1]>=range_ls[1][1])):
        return True #range 2 is contained within range 1
    elif ((range_ls[1][0]<=range_ls[0][0]) & (range_ls[1][1]>=range_ls[0][1])):
        return True #range 1 is contained within range 2
    else:
        return False
def is_overlapping(range_ls):
    """
    returns if one range overlapps the other
    :param range_tuple: tuple of two ranges to compare
    :return: boolean of whether one range overlaps the other

    usage examples:

    >>> is_overlapping([[2,4],[6,8]])
    False

    >>> is_overlapping([[2,3],[4,5]])
    False

    >>> is_overlapping([[5,7],[7,9]])
    True

    >>> is_overlapping([[2,8],[3,7]])
    True

    >>> is_overlapping([[6,6],[4,6]])
    True

    >>> is_overlapping([[2,6],[4,8]])
    True
    """
    if is_fully_contained(range_ls):
        return True
    elif ((range_ls[0][0]<=range_ls[1][1]) & (range_ls[0][0]>=range_ls[1][0])):
        return True
    elif ((range_ls[0][1]<=range_ls[1][1]) & (range_ls[0][1]>=range_ls[1][0])):
        return True
    else:
        return False
if __name__=="__main__":
    test_count_contained_ranges()
    test_count_overlapped_ranges()

    print(f"the number of contained ranges:{count_contained_ranges(data)}")
    print(f"the number of overlapped ranges:{count_overlapped_ranges(data)}")
