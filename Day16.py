from aocd import data
from itertools import permutations, product


def parse_valve(valve_string):
    """
    converts a string into a dictionary for the string
    :param valve_string: string describing a single valve
    :return: dictionary describing the valve

    >>> parse_valve("Valve AA has flow rate=0; tunnels lead to valves DD, II, BB")
    {'AA': {'flow_rate': 0, 'child_valves': ['DD', 'II', 'BB']}}
    """
    split_ls = valve_string.split("; ")
    name_flow_rate = split_ls[0].split(" has flow rate=")
    name = name_flow_rate[0].split(" ")[1]
    flow_rate = int(name_flow_rate[1])
    child_valves_ls = split_ls[1].split("to ")[1].split(" ", 1)[1].split(", ")
    return {
        name: {
            'flow_rate': flow_rate,
            'child_valves': child_valves_ls
        }
    }


def parse_input(raw_data):
    """
    parses raw data into tree nodes.
    :param raw_data: raw input
    :return: formatted output
    """
    valve_dict = dict()
    split_ls = raw_data.split("\n")
    for curr_valve in split_ls:
        new_valve = parse_valve(curr_valve)
        valve_dict.update(new_valve)
    return valve_dict


def make_valve_dist_dict(valve_dict):
    """
    creates a dictionary  to store distances between working valves
    :param valve_dict: dictionary of valves
    :return: the dictionary containing edges with distance = 1
    """
    # dictionary to store distances between working valves
    valve_dist_dict = {}

    # only add working valves
    for key, value in valve_dict.items():
        if value['flow_rate'] > 0:
            valve_dist_dict[key] = {}
            for curr_child in value["child_valves"]:
                if valve_dict[curr_child]['flow_rate'] > 0:
                    valve_dist_dict[key][
                        curr_child] = 2  # takes an extra minute to open valve and a minute for it be effective

    return valve_dist_dict


def distance_to_valve(start_node_name, target_valve_name, valve_dict, valve_dist_dict):
    """
    determines the distance between valves

    passing back the dictionary value to allow for testing. Otherwise, would leave as global variable
    :param start_node_name: name of the start node
    :param target_valve_name: name of the target valve
    :return: number of steps in between the two nodes and updated dictionary (if start_node_name was a node with an active valve)
    """
    if start_node_name in valve_dist_dict:  # if the distance is in the dictionary, return it
        if target_valve_name in valve_dist_dict[start_node_name]:  # if it's already in the distance dictionary
            return valve_dist_dict[start_node_name][target_valve_name], valve_dist_dict

    # otherwise, calculate the distance and save it to the dictionary
    numsteps = 0
    nodes_ls = [start_node_name]
    node_found = False
    while not node_found:
        new_node_ls = []
        # walk through child nodes
        for node_name in nodes_ls:
            if target_valve_name in valve_dict[node_name]["child_valves"]:
                node_found = True
            else:
                new_node_ls += valve_dict[node_name]["child_valves"]
        numsteps += 1
        nodes_ls = new_node_ls
    # takes an extra minute to open valve
    time_count = numsteps + 1

    if start_node_name in valve_dist_dict:
        valve_dist_dict[start_node_name][target_valve_name] = time_count

    return time_count, valve_dist_dict


def calculate_valve_value(start_node_name, target_valve_name, minutes_left, valve_dict, valve_dist_dict):
    """
    calculates the value of the path between start_node_name and target_valve_name
    :param valve_dist_dict:
    :param valve_dict:
    :param minutes_left: minutes left
    :param start_node_name: start node to calculate distance
    :param target_valve_name: end node to calculate distance
    :return: calculated node value

    """

    distance = distance_to_valve(start_node_name, target_valve_name, valve_dict, valve_dist_dict)[0]
    active_time = minutes_left - (distance * 1.5) - 1  # takes a minute for valve to activate
    value = active_time * valve_dict[target_valve_name]["flow_rate"]
    return value, distance


def highest_accessible_node(sorted_valve_values, time_left):
    """
    returns the most value node accessible within time_left
    :param sorted_valve_values:
    :param time_left:
    :return: node name or None (of none of the nodes are accessible
    """

    # which is the highest value node we can get to in time?
    for curr_valve in sorted_valve_values:
        if curr_valve[1][1] <= time_left:
            return curr_valve
    return None


def calculate_path_pressure(path_ls, total_time, valve_dict, valve_dist_dict):
    """
    given a single path of valves, calculates the total pressure released by following the path
    :param path_ls:valve order
    :param total_time:maximum number of minutes to exhaust
    :param valve_dict:dictionary of valve parameters
    :param valve_dist_dict:dictionary of the distances between valves
    :return: total amount of pressure vented over total_time by following path_ls, and the valves that got opened
        (not all valves in valve_ls get opened if we run out of time)
    """
    total_pressure = 0
    time_left = total_time
    open_valves_ls = []
    curr_node = "AA"
    for valve in path_ls:
        valve_activation_time = distance_to_valve(curr_node, valve, valve_dict, valve_dist_dict)[0]
        if valve_activation_time <= time_left:
            # release pressure
            step_pressure = sum([valve_dict[valve_name]["flow_rate"] for valve_name in open_valves_ls])
            total_pressure += step_pressure * valve_activation_time
            # move to node
            curr_node = valve
            open_valves_ls.append(valve)
            time_left -= valve_activation_time
    # purge for the rest of the time
    step_pressure = sum([valve_dict[valve_name]["flow_rate"] for valve_name in open_valves_ls])
    total_pressure += step_pressure * time_left
    return total_pressure, open_valves_ls


def create_path_generator(high_flow_valves_set, low_flow_valves_set):
    """
    creates a generator of valve orders (a "path") where the high_flow_valves always preceed the low_flow_valves.
    within each valve set, generator creates the full permutation of possible orders
    :param high_flow_valves_set: set of valves that need to go first
    :param low_flow_valves_set: set of valves that need to be at the end of the list
    :return: generator that yields paths

    >>>
    """
    product_gen = product(permutations(high_flow_valves_set), permutations(low_flow_valves_set))
    for curr_product in product_gen:
        yield curr_product[0] + curr_product[1]


def max_pressure_release(raw_data):
    """
    determines the maximum pressure you can release in 30 minutes
    :param raw_data: raw input
    :return: maximum pressure it's possible to release
    """
    valve_dict = parse_input(raw_data)

    # dictionary to store distances between working valves
    valve_dist_dict = make_valve_dist_dict(valve_dict)

    total_time = 30

    valves_sorted_by_flow_rate_ls = sorted(valve_dist_dict, key=lambda x: valve_dict[x]["flow_rate"], reverse=True)
    max_flow_rate = valve_dict[valves_sorted_by_flow_rate_ls[0]]["flow_rate"]
    high_flow_valves_set = {x for x in valve_dist_dict if valve_dict[x]["flow_rate"] > max_flow_rate / 2}
    low_flow_valves_set = set(valve_dist_dict).difference(high_flow_valves_set)

    path_gen = create_path_generator(high_flow_valves_set, low_flow_valves_set)

    max_pressure = 0
    num_processed = 0
    for curr_path in path_gen:
        num_processed+=1
        if num_processed%1000:
            print (num_processed)
        curr_total_pressure, open_valves_ls = calculate_path_pressure(curr_path, total_time, valve_dict,
                                                                      valve_dist_dict)

        if curr_total_pressure > max_pressure:
            max_pressure = curr_total_pressure
            max_pressure_path = open_valves_ls
            print(max_pressure, max_pressure_path)

    return max_pressure


if __name__ == '__main__':
    print(f"max pressure is {max_pressure_release(data)}")
