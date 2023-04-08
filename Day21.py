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
            value = eval(
                f"{parsed_monkey_dict[parents_tuple[0]].value}{operation}{parsed_monkey_dict[parents_tuple[1]].value}")
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
    unparsed_parents_ls = [parent for parent in parents_tuple if parent not in parsed_monkey_dict]
    if not unparsed_parents_ls:  # both parents are parsed
        value = eval(
            f"{parsed_monkey_dict[parents_tuple[0]].value}{operation}{parsed_monkey_dict[parents_tuple[1]].value}")

        curr_monkey.value = value

        parsed_monkey_dict[curr_monkey.name] = curr_monkey
        del unparsed_monkey_dict[curr_monkey.name]
    return unparsed_parents_ls


def parse_monkey_list(monkey_names_to_parse_ls, parsed_monkey_dict,
                      unparsed_monkey_dict, ):
    human_path_ls = []
    while len(monkey_names_to_parse_ls) > 0:
        curr_monkey = unparsed_monkey_dict[monkey_names_to_parse_ls[0]]
        if curr_monkey.name == "humn":
            child_path_ls = monkey_names_to_parse_ls[1:]
            curr_monkey_name = "humn"
            while child_path_ls:
                potential_child_monkey = unparsed_monkey_dict[child_path_ls[0]]
                if curr_monkey_name in potential_child_monkey.parents:
                    human_path_ls.append(potential_child_monkey)
                curr_monkey_name = child_path_ls[0]
                child_path_ls = child_path_ls[1:]
            parsed_monkey_dict[curr_monkey.name] = curr_monkey
            monkey_names_to_parse_ls = monkey_names_to_parse_ls[1:]
        else:
            new_unparsed_monkey_ls = parse_monkey(
                parsed_monkey_dict,
                unparsed_monkey_dict,
                curr_monkey
            )
            if new_unparsed_monkey_ls:
                monkey_names_to_parse_ls = new_unparsed_monkey_ls + monkey_names_to_parse_ls
            else:  # this monkey was parsed
                monkey_names_to_parse_ls = monkey_names_to_parse_ls[1:]
    return human_path_ls


def monkey_math1(raw_data):
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

    while len(monkey_names_to_parse_ls) > 0:
        curr_monkey = unparsed_monkey_dict[monkey_names_to_parse_ls[0]]
        new_unparsed_monkey_ls = parse_monkey(
            parsed_monkey_dict,
            unparsed_monkey_dict,
            curr_monkey
        )
        if new_unparsed_monkey_ls:
            monkey_names_to_parse_ls = new_unparsed_monkey_ls + monkey_names_to_parse_ls
        else:  # this monkey was parsed
            monkey_names_to_parse_ls = monkey_names_to_parse_ls[1:]

    return parsed_monkey_dict["root"].value


def monkey_math2(raw_data):
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
    # move humn from dict

    humn_monkey = parsed_monkey_dict["humn"]
    del parsed_monkey_dict["humn"]
    unparsed_monkey_dict["humn"] = humn_monkey

    # who are roots's parents?
    root_children = unparsed_monkey_dict["root"].parents

    first_parent = parse_monkey_list(
        [root_children[0]],
        parsed_monkey_dict,
        unparsed_monkey_dict
    )

    second_parent = parse_monkey_list(
        [root_children[1]],
        parsed_monkey_dict,
        unparsed_monkey_dict
    )
    return parsed_monkey_dict["root"].value


if __name__ == '__main__':
    print(f"part1:{monkey_math1(data)}")
