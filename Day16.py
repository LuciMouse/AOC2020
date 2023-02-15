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


def max_pressure_release(raw_data):
    """
    determines the maximum pressure you can release in 30 minutes
    :param raw_data: raw input
    :return: maximum pressure it's possible to release
    """
    valve_dict = parse_input(raw_data)

    paths_ls = [{
        'curr_valve': 'AA',
        'curr_total_pressure': 0,
        'path_ls': ['AA'],
        'open_valves_ls': []
    }]

    for curr_time in range(30):
        new_paths_ls = []
        for curr_path in paths_ls:
            curr_valve = curr_path['curr_valve']
            if (valve_dict[curr_valve]['flow_rate'] != 0) and (curr_valve not in curr_path['open_valves_ls']): #if there's a valve to open
                step_pressure = sum([valve_dict[valve]["flow_rate"] for valve in curr_path['open_valves_ls']])
                total_pressure = curr_path['curr_total_pressure'] + step_pressure
                curr_open_valves_ls = curr_path['open_valves_ls']+[curr_valve]
                same_curr_valve_paths = [x for x in new_paths_ls if x["curr_valve"] == curr_valve]
                if same_curr_valve_paths: #if there are other paths that end at the same curr_valve
                    #keep the one with the highest curr_total_pressure
                    future_step_pressure = sum([valve_dict[valve]["flow_rate"] for valve in curr_open_valves_ls])
                    future_total_pressure = curr_path['curr_total_pressure'] + future_step_pressure
                    paths_to_remove_ls = [x for x in same_curr_valve_paths if x["curr_total_pressure"]<future_total_pressure]
                    if paths_to_remove_ls: #replace existing path with new path
                        new_paths_ls.remove(paths_to_remove_ls[0])
                        new_paths_ls.append(
                            {
                                'curr_valve': curr_valve,
                                'curr_total_pressure': total_pressure,
                                'path_ls': curr_path['path_ls']+[curr_valve],
                                'open_valves_ls': curr_open_valves_ls,
                            }
                        )
                else:
                    new_paths_ls.append(
                        {
                            'curr_valve': curr_valve,
                            'curr_total_pressure': curr_path['curr_total_pressure'] + step_pressure,
                            'path_ls': curr_path['path_ls']+[curr_valve],
                            'open_valves_ls': curr_path['open_valves_ls']+[curr_valve],
                        }
                    )
            # add child valves
            for curr_child in valve_dict[curr_valve]['child_valves']:
                step_pressure = sum([valve_dict[valve]["flow_rate"] for valve in curr_path['open_valves_ls']])
                total_pressure = curr_path['curr_total_pressure'] + step_pressure
                same_curr_valve_paths = [x for x in new_paths_ls if x["curr_valve"] == curr_child]
                if same_curr_valve_paths:  # if there are other paths that end at the same curr_child
                    # keep the one with the highest curr_total_pressure
                    paths_to_remove_ls = [x for x in same_curr_valve_paths if
                                          x["curr_total_pressure"] < total_pressure]
                    if paths_to_remove_ls: #replace existing path with new path
                        new_paths_ls.remove(paths_to_remove_ls[0])
                        new_paths_ls.append(
                            {
                                'curr_valve': curr_child,
                                'curr_total_pressure': total_pressure,
                                'path_ls': curr_path['path_ls']+[curr_child],
                                'open_valves_ls': curr_path['open_valves_ls'].copy()
                            }
                        )
                else:
                    new_paths_ls.append(
                        {
                            'curr_valve': curr_child,
                            'curr_total_pressure': total_pressure,
                            'path_ls': curr_path['path_ls']+[curr_child],
                            'open_valves_ls': curr_path['open_valves_ls']
                        }
                    )

        paths_ls = new_paths_ls

    pressure_ls = [x["curr_total_pressure"] for x in paths_ls]
    max_pressure = max(pressure_ls)

    return  max_pressure


if __name__ == '__main__':
    print(f"max pressure is {max_pressure_release(data)}")
