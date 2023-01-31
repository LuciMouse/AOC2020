from aocd import data
def badge_priority_sum(raw_input):
    split_rucksack_ls = split_into_rucksacks(raw_input)
    badge_ls = badge_finder(split_rucksack_ls)
    return priority_sum(badge_ls)

def test_badge_priority_sum():
    with open("Day3_test_input.txt","r") as input_file:
        raw_test_input=input_file.read()
    assert badge_priority_sum(raw_test_input) == 70

def badge_finder(rucksack_ls):
    """
    given a list of all the rucksack contents, finds the common element in each group of three rucksacks
    :param split_rucksack_ls: list of rucksack contents
    :return: list of the common elements

    usage examples
    >>> badge_finder(["vJrwpWtwJgWrhcsFMMfFFhFp","jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL","PmmdzqPrVvPwwTWBwg","wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn","ttgJtRGJQctTZtZT","CrZsJsPPZsGzwwsLwLmpwMDw",])
    ['r', 'Z']
    """
    num_badges = len(rucksack_ls)//3

    return [next(iter(set([*rucksack_ls[index_multiplier*3]]).intersection(set([*rucksack_ls[index_multiplier*3+1]]),set([*rucksack_ls[index_multiplier*3+2]])))) for index_multiplier in range(num_badges)]

def rucksack_common_priority_sum(raw_input):
    """
    takes the list of contents for all the rucksacks,
    determines the common item between both compartments of each rucksack,
    and sums the priority of all these common items
    :param raw_input: list of contents of all rucksacks
    :return: summed priority of common items
    """
    split_rucksack_ls = split_into_rucksacks(raw_input)
    split_compartments_ls = [split_into_compartments(x) for x in split_rucksack_ls]
    common_items_ls = [compartment_compare(x) for x in split_compartments_ls]
    return priority_sum(common_items_ls)

def test_rucksack_common_priority_sum():
    with open("Day3_test_input.txt","r") as input_file:
        raw_test_input=input_file.read()
    assert rucksack_common_priority_sum(raw_test_input) == 157

def priority_sum(item_ls):
    """
    takes a list of single items, converts to priority, and sums
    :param item_ls: list of items
    :return: sum of the converted priority of all the items

    usage example

    >>> priority_sum(['p','L','P','v','t','s'])
    157
    """
    return sum([priority_convert(x) for x in item_ls])


def priority_convert(curr_item):
    """
    converts the item type into a priority
    :param curr_item: character of item
    :return: corresponding priority value of the item

    usage examples

    >>> priority_convert('p')
    16

    >>> priority_convert('L')
    38

    >>> priority_convert('P')
    42

    >>> priority_convert('v')
    22

    >>> priority_convert('t')
    20

    >>> priority_convert('s')
    19
    """
    if curr_item.isupper():
        return ord(curr_item)-38
    else:
        return ord(curr_item)-96

def compartment_compare(rucksack_ls):
    """
    compares the two compartments of the rucksack and returns the common item
    :param rucksack_ls: lis of the contents of the two compartments
    :return: item that is common

    usage examples:

    >>> compartment_compare(['vJrwpWtwJgWr', 'hcsFMMfFFhFp'])
    'p'

    >>> compartment_compare(['jqHRNqRjqzjGDLGL', 'rsFMfFZSrLrFZsSL'])
    'L'

    >>> compartment_compare(['PmmdzqPrV', 'vPwwTWBwg'])
    'P'

    >>> compartment_compare(split_into_compartments("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn"))
    'v'

    >>> compartment_compare(split_into_compartments("ttgJtRGJQctTZtZT"))
    't'

    >>> compartment_compare(split_into_compartments("CrZsJsPPZsGzwwsLwLmpwMDw"))
    's'
    """
    #make each list of items into a set, intesect, and unpack
    return next(iter(set([*rucksack_ls[0]]).intersection(set([*rucksack_ls[1]]))))



def split_into_compartments(rucksack_contents):
    """
    given the contents of a single rucksack, splits it into the contents of the two compartments
    :param rucksack_contents: string of rucksack contents
    :return:list of contents split into teo compartments

    usage examples

    >>> split_into_compartments("vJrwpWtwJgWrhcsFMMfFFhFp")
    ['vJrwpWtwJgWr', 'hcsFMMfFFhFp']

    >>> split_into_compartments("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL")
    ['jqHRNqRjqzjGDLGL', 'rsFMfFZSrLrFZsSL']

    >>> split_into_compartments("PmmdzqPrVvPwwTWBwg")
    ['PmmdzqPrV', 'vPwwTWBwg']

    """
    split_index = len(rucksack_contents)//2
    return [rucksack_contents[:split_index],rucksack_contents[split_index:]]

def split_into_rucksacks(raw_input):
    """
    takes the raw input and splits into a list of individual rucksack contents
    :param raw_data: puzzle input
    :return: list where each item is a single rucksack
    """
    return raw_input.split('\n')

def test_split_into_rucksacks():
    with open("Day3_test_input.txt","r") as input_file:
        raw_test_input=input_file.read()
    assert split_into_rucksacks(raw_test_input)==[
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]
if __name__=="__main__":
    test_split_into_rucksacks()
    test_rucksack_common_priority_sum()
    test_badge_priority_sum()

    print(f"the sum of all common items is:{rucksack_common_priority_sum(data)}")
    print(f"the sum of all badges is:{badge_priority_sum(data)}")