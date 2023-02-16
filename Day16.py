from aocd import data


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
    active_time = minutes_left - distance - 1 #takes a minute for valve to activate
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

    # what's the closest valve to move to?

    curr_node = "AA"
    time_left = total_time
    open_valves_ls = []
    curr_total_pressure = 0
    while time_left >0:
        # for each valve, determine the closest valve to move to, In the case of a tie, pick the one with the highest flow_rate

        sorted_valve_distances = sorted(
            [
                (node_name,
                 distance_to_valve(
                     curr_node,
                     node_name,
                     valve_dict,
                     valve_dist_dict
                 )[0]
                 ) for node_name in set(valve_dist_dict.keys()).difference(set(open_valves_ls))
            ],
            key=lambda x: x[1]
        )

        if sorted_valve_distances:  # there are still unvisited valves
            smallest_distance = sorted_valve_distances[0][1]
            if smallest_distance <= time_left: #can reach in time
                closest_nodes_sorted_by_flow_ls = sorted(
                    [x for x in sorted_valve_distances if x[1]==smallest_distance],
                    key = lambda x: valve_dict[x[0]]["flow_rate"],
                    reverse = True
                )
                next_node = closest_nodes_sorted_by_flow_ls[0]
                # release pressure
                step_pressure = sum([valve_dict[valve_name]["flow_rate"] for valve_name in open_valves_ls])
                curr_total_pressure += step_pressure * smallest_distance
                # move to node
                curr_node = next_node[0]
                open_valves_ls.append(next_node[0])
                time_left -= sorted_valve_distances[0][1]
            else:
                break #none of the remaining nodes can be reached in time
        else: #all valves have been opened
            break
    #purge for the rest of the time
    step_pressure = sum([valve_dict[valve_name]["flow_rate"] for valve_name in open_valves_ls])
    curr_total_pressure += step_pressure * time_left
    return curr_total_pressure


if __name__ == '__main__':
    print(f"max pressure is {max_pressure_release(data)}")
