from aocd import data


class RobotBlueprint:
    def __init__(self, robot_dict):
        self.robot_dict = robot_dict


class Robot:
    def __init__(self, type, ore_cost, clay_cost=0, obsidian_cost=0):
        self.type = type
        self.ore_cost = ore_cost
        self.clay_cost = clay_cost
        self.obsidian_cost = obsidian_cost


def format_data(raw_input):
    """
    formats raw_input into blueprint objects
    :param raw_input: raw puzzle input
    :return: list of blueprint objects
    """
    blueprint_ls = []

    split_input = raw_input.split("\n")
    for blueprint in split_input:
        split_blueprint = blueprint.split(".")
        split_robots = [x.split(" ") for x in split_blueprint]
        blueprint_ls.append(
            RobotBlueprint(
                robot_dict={
                    "ore": Robot(
                        type="ore",
                        ore_cost=int(split_robots[0][6])
                    ),
                    "clay": Robot(
                        type="clay",
                        ore_cost=int(split_robots[1][5])
                    ),
                    "obsidian": Robot(
                        type='obsidian',
                        ore_cost=int(split_robots[2][5]),
                        clay_cost=int(split_robots[2][8]),
                    ),
                    "geode": Robot(
                        type='geode',
                        ore_cost=int(split_robots[3][5]),
                        obsidian_cost=int(split_robots[3][8])
                    )
                }
            )
        )
    return blueprint_ls


def resource_gen():
    for resource in ["geode", "obsidian", "clay", "ore"]:
        yield resource


def can_build_robot(num_resources_dict, blueprint, curr_robot_type):
    """
    determines if there are enough resources to build the specified robot
    :param blueprint: blueprint of robot requirements
    :param num_resources_dict: dictionary of available resources
    :param curr_robot_type: type of robot we're trying to build
    :return:
    """
    ore_cost = blueprint.robot_dict[curr_robot_type].ore_cost
    clay_cost = blueprint.robot_dict[curr_robot_type].clay_cost
    obsidian_cost = blueprint.robot_dict[curr_robot_type].obsidian_cost
    if (
            ore_cost <= num_resources_dict["ore"]
    ) & (
            clay_cost <= num_resources_dict["clay"]
    ) & (
            obsidian_cost <= num_resources_dict["obsidian"]
    ):
        num_resources_dict["ore"] -= ore_cost
        num_resources_dict["clay"] -= clay_cost
        num_resources_dict["obsidian"] -= obsidian_cost
        print(
            f"spend {ore_cost} ore, {clay_cost} clay, {obsidian_cost} obsidian to build a {curr_robot_type} robot"
        )
        return True, num_resources_dict
    else:
        return False, num_resources_dict


def update_build_order(build_order_ls, num_robots_dict, curr_robot,max_geodes):
    """

    :param num_robots_dict: dictionary of built robots
    :param curr_robot: current robot that's being built
    :param build_order_ls: order of robot types to build
    :return:
    """
    resource_ls = ["ore", "clay", "obsidian", "geode", ]
    new_build_orders = []
    for curr_resource in resource_ls[1:][::-1]:
        # only add if the dependant robots are already built
        resource_index = resource_ls.index(curr_resource)
        if all(
                [(num_robots_dict[dependant_robot] > 0 or dependant_robot == curr_robot) for dependant_robot in
                 resource_ls[:resource_index]]
        ):
            new_build_orders.append(build_order_ls + [curr_resource])
    new_build_orders.append(build_order_ls + ["ore"])
    return new_build_orders[0], new_build_orders[1:]

def calculate_num_geodes(build_order_ls,
                blueprint,
                num_minutes,
                         build_order_lists_ls,
                         max_geodes):
    """
    given the build order, calculates the number of geodes built in num_minutes
    :param build_order_ls:
    :param blueprint:
    :param num_minutes:
    :return: number of geodes
    """
    num_resources_dict = {
        "ore": 0,
        "clay": 0,
        "obsidian": 0,
        "geode": 0
    }

    num_robots_dict = {
        "ore": 1,
        "clay": 0,
        "obsidian": 0,
        "geode": 0
    }
    build_order_index = 0
    curr_time = 1
    while curr_time <= num_minutes:
        print(f"\nminute {curr_time}")
        # can we build a robot
        curr_robot_type = build_order_ls[build_order_index]
        new_robot, num_resources_dict = can_build_robot(
            num_resources_dict,
            blueprint,
            curr_robot_type
        )
        # mine
        resource_generator = resource_gen()
        for curr_resource in resource_generator:
            num_resources_dict[curr_resource] += num_robots_dict[curr_resource]
            print(
                f"{num_robots_dict[curr_resource]} active {curr_resource}-robots, total is {num_resources_dict[curr_resource]} {curr_resource}")
        if new_robot:
            num_robots_dict[curr_robot_type] += 1
            # update build_order
            if build_order_index == len(build_order_ls) - 1:
                build_order_ls, new_build_order = update_build_order(
                    build_order_ls,
                    num_robots_dict,
                    curr_robot_type,
                    max_geodes
                )
                build_order_lists_ls += new_build_order
            build_order_index += 1
        curr_time += 1
    return num_resources_dict["geode"]


def determine_max_geodes(blueprint, num_minutes):
    """
    calculates the maximum number of geodes we can mine using this blueprint

    :param blueprint: blueprint of robots
    :param num_minutes: number of minutes to mine geodes
    :return: maximum number of geodes
    """
    build_order_lists_ls = [
        ["ore"],
        ["clay"],
    ]

    max_geodes = 0

    while build_order_lists_ls:
        num_geodes = calculate_num_geodes(
            build_order_lists_ls[0],
            blueprint,
            num_minutes,
            build_order_lists_ls,
            max_geodes
        )
        if num_geodes > max_geodes:
            max_geodes = num_geodes
        build_order_lists_ls = build_order_lists_ls[1:]
    return max_geodes


def sum_quality_levels(raw_input, num_minutes):
    """
    determines the sum of all quality levels of all blueprints in raw_input
    :param raw_input: raw puzzle input
    :param num_minutes: number of minutes allowed for processing
    :return: sum of all quality levels of blueprints
    """
    blueprints_ls = format_data(raw_input)
    max_geodes_ls = [determine_max_geodes(blueprint, num_minutes) for blueprint in blueprints_ls]
    return sum


if __name__ == '__main__':
    print(f"{data[4]}")
