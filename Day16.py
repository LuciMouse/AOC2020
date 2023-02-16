from aocd import data
from itertools import permutations


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
                    valve_dist_dict[key][curr_child] = 2 #takes an extra minute to open valve and a minute for it be effective

    # do permutations to determine distances between all valves
    perm = permutations(valve_dict.keys(), 2)
    for start_node_name, target_valve_name in perm:
        distance_to_valve(start_node_name, target_valve_name, valve_dict, valve_dist_dict)
        #edited in place so no need to return
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


def max_pressure_release(raw_data):
    """
    determines the maximum pressure you can release in 30 minutes
    :param raw_data: raw input
    :return: maximum pressure it's possible to release
    """
    valve_dict = parse_input(raw_data)

    # find highest value valves and visit them in order
    sorted_valves_by_flow_rate_ls = sorted(
        {key:value for key,value in valve_dict.items() if value["flow_rate"]>0}.items(),
        key=lambda x: x[1]["flow_rate"],
        reverse=True
    )

    # dictionary to store distances between working valves
    valve_dist_dict = make_valve_dist_dict(valve_dict)

    total_time = 30

    # move from AA to first node
    curr_node = "AA"
    next_node = sorted_valves_by_flow_rate_ls[0][0]
    time_left = total_time - distance_to_valve(curr_node, next_node, valve_dict, valve_dist_dict)[0]
    curr_node = next_node
    open_valves_ls = [curr_node]

    curr_total_pressure = 0

    for curr_valve in sorted_valves_by_flow_rate_ls[1:]:
        # can we get to the next valve in time?
        next_node = curr_valve[0]
        time_to_valve = distance_to_valve(curr_node, next_node, valve_dict, valve_dist_dict)[0]
        if time_to_valve < time_left:
            # release pressure
            step_pressure = sum([valve_dict[valve]["flow_rate"] for valve in open_valves_ls])
            curr_total_pressure = curr_total_pressure + (step_pressure * time_to_valve)
            #move to node
            curr_node = next_node
            open_valves_ls.append(curr_valve[0])
            time_left -= time_to_valve

    #if all valves are visited, purge for remaining time
    step_pressure = sum([valve_dict[valve]["flow_rate"] for valve in open_valves_ls])
    curr_total_pressure = curr_total_pressure + (step_pressure * time_left)


    return curr_total_pressure


if __name__ == '__main__':
    print(f"max pressure is {max_pressure_release(data)}")
