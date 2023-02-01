from aocd import data
from functools import reduce

class monkey:
    def __init__(self, monkey_number, starting_items, operation, test_tuple=None):
        self.monkey_number = monkey_number
        self.starting_items = starting_items
        self.operation = operation
        self.test_tuple = test_tuple
        self.test = lambda value: test_tuple[1] if value % test_tuple[0]==0 else test_tuple[2]


def make_monkey(unformatted_data):
    """
    given a block of unformatted data, makes a monkey object
    :param unformatted_data: unformatted strings
    :return: monkey object
    """
    unformatted_data_ls = unformatted_data.split("\n")

    monkey_number = int(unformatted_data_ls[0].split(' ')[1][:-1])
    starting_items = [int(x) for x in unformatted_data_ls[1].split(': ')[1].split(", ")]
    operation = unformatted_data_ls[2].split('= ')[1]
    test_tuple = (
        int(unformatted_data_ls[3].split(' ')[-1]),
        int(unformatted_data_ls[4][-1]),
        int(unformatted_data_ls[5][-1])
    )
    new_monkey = monkey(monkey_number, starting_items, operation, test_tuple)
    return new_monkey

def monkey_turn(monkey_index,monkey_ls,test_product):
    """
    describes a single monkey's turn
    :param test_product: product of all monkey test values
    :param monkey_index: index of monkey that is inspecting and throwing
    :param monkey_ls: list of all monkey objects
    :return: updated monkey_ls
    """
    curr_monkey = monkey_ls[monkey_index]
    for curr_item in curr_monkey.starting_items:
        old = curr_item
        inspection_worry_level = eval(curr_monkey.operation)%test_product
        recipient_monkey = curr_monkey.test(inspection_worry_level)
        monkey_ls[recipient_monkey].starting_items.append(inspection_worry_level)
    curr_monkey.starting_items = []
    return monkey_ls

def round_implementer(monkey_ls, item_count_ls,test_product):
    """
    describes a round of monkey shenanigans
    :param item_count_ls: list of number of objects each monkey has examined
    :param test_product: product of all monkey test values
    :param monkey_ls: list of monkey objects
    :return: updated monkey list
    """
    for curr_index in range(len(monkey_ls)):
        item_count_ls[curr_index]+=len(monkey_ls[curr_index].starting_items)
        monkey_ls = monkey_turn(curr_index,monkey_ls,test_product)
    return monkey_ls, item_count_ls

def calculate_monkey_business(raw_input, num_rounds):
    """
    calculates the level of monkey business over num_rounds of shenanigans
    :param raw_input: raw data
    :param num_rounds: number of rounds to implement
    :return: total amount of monkey business
    """

    monkey_ls = []
    for unformatted_curr_monkey in raw_input.split('\n\n'):
        new_monkey = make_monkey(unformatted_curr_monkey)
        monkey_ls.append(new_monkey)

    #to simplify calculation, define a test_product (product of all the test values)
    test_product = reduce(lambda x,y: x*y,[curr_monkey.test_tuple[0] for curr_monkey in monkey_ls])

    item_count_ls = [0 for x in monkey_ls]
    for round_num in range(num_rounds):
        monkey_ls, item_count_ls = round_implementer(monkey_ls, item_count_ls,test_product )
        if (round_num+1)%100==0:
            print(f"{round_num}: {item_count_ls},{[x.starting_items for x in monkey_ls]}")
    most_active_monkeys_ls = item_count_ls.copy()
    most_active_monkeys_ls.sort(reverse=True)
    return (most_active_monkeys_ls[0]*most_active_monkeys_ls[1])


if __name__ == '__main__':
    print(f"level of monkey business: {calculate_monkey_business(data,1000)}")

