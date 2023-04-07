from aocd import data


class Monkey:
    def __init__(self, name, value, parents=None):
        self.name = name
        self.parents = parents
        self.value = value


def make_raw_monkey_dict(raw_data):
    split_data = [monkey.split(": ") for monkey in raw_data.split("\n")]
    return {monkey[0]: monkey[1] for monkey in split_data}


def parse_raw_monkey(raw_monkey_dict, parsed_monkey_dict, unparsed_monkey_dict, monkey_name):
    raw_monkey = raw_monkey_dict[monkey_name]
    try:
        int(raw_monkey)
    except ValueError:
        split_monkey = raw_monkey.split(" ")
        parents_tuple = (split_monkey[0], split_monkey[2])
        operation = split_monkey[1]

        if all([parent in parsed_monkey_dict for parent in parents_tuple]):
            value = eval(f"{parsed_monkey_dict[parents_tuple[0]].value}{operation}{parsed_monkey_dict[parents_tuple[1]].value}")
            parsed_monkey_dict[monkey_name] = Monkey(
                name=monkey_name,
                value=value,
                parents=parents_tuple
            )
        else:
            unparsed_monkey_dict[monkey_name] = Monkey(
                name=monkey_name,
                parents=parents_tuple,
                value=raw_monkey
            )
    else:
        parsed_monkey_dict[monkey_name] = Monkey(
            name=monkey_name,
            value=int(raw_monkey)
            )

def parse_monkey(parsed_monkey_dict, unparsed_monkey_dict, curr_monkey):
    parents_tuple = curr_monkey.parents
    operation = curr_monkey.value.split(" ")[1]
    unparsed_parents_ls = [parent for parent in parents_tuple if parent not in parsed_monkey_dict ]
    if not unparsed_parents_ls: #both parents are parsed
        value = eval(
            f"{parsed_monkey_dict[parents_tuple[0]].value}{operation}{parsed_monkey_dict[parents_tuple[1]].value}")

        curr_monkey.value = value

        parsed_monkey_dict[curr_monkey.name] = curr_monkey
        del unparsed_monkey_dict[curr_monkey.name]
    return unparsed_parents_ls



def monkey_math(raw_data):

    raw_monkey_dict = make_raw_monkey_dict(raw_data)
    parsed_monkey_dict = {}
    unparsed_monkey_dict = {}

    for monkey_name in raw_monkey_dict:
        parse_raw_monkey(
            raw_monkey_dict,
            parsed_monkey_dict,
            unparsed_monkey_dict,
            monkey_name
        )
    monkey_names_to_parse_ls = ["root"]

    while len(monkey_names_to_parse_ls)>0:
        curr_monkey = unparsed_monkey_dict[monkey_names_to_parse_ls[0]]
        new_unparsed_monkey_ls = parse_monkey(
            parsed_monkey_dict,
            unparsed_monkey_dict,
            curr_monkey
        )
        if new_unparsed_monkey_ls:
            monkey_names_to_parse_ls = new_unparsed_monkey_ls + monkey_names_to_parse_ls
        else: #this monkey was parsed
            monkey_names_to_parse_ls = monkey_names_to_parse_ls[1:]

    return parsed_monkey_dict["root"].value


if __name__ == '__main__':
    print(f"{data[4]}")
