from aocd import data


def parse_valve(valve_string):
    """
    converts a string into a dictionary for the string
    :param valve_string: string describing a single valve
    :return: dictionary describing the valve

    >>> parse_valve("Valve AA has flow rate=0; tunnels lead to valves DD, II, BB")
    {'AA': {'flow_rate': 0, 'child valves': ['DD', 'II', 'BB']}}
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


def take_action(valve_dict, curr_valve, curr_time, open_valves_ls, curr_total_pressure, path_ls):
    if curr_time == 30:  # out of time
        return curr_total_pressure

    if (valve_dict[curr_valve]['flow_rate'] != 0) and (curr_valve not in open_valves_ls):
        open_valves_ls.append(curr_valve)
        curr_time += 1  # takes a minute to open a valve
        path_ls.append(curr_valve)
    step_pressure = sum([valve_dict[valve]["flow_rate"] for valve in open_valves_ls])
    return max(
        [take_action(
            valve_dict,
            curr_child,
            curr_time + 1,
            open_valves_ls,
            curr_total_pressure + step_pressure,
            path_ls+[curr_child]
        ) for curr_child in valve_dict[curr_valve]['child_valves']])


def max_pressure_release(raw_data):
    """
    determines the maximum pressure you can release in 30 minutes
    :param raw_data: raw input
    :return: maximum pressure it's possible to release
    """
    valve_dict = parse_input(raw_data)
    curr_valve = "AA"
    curr_time = 0
    open_valves_ls = []

    curr_total_pressure = 0
    path_ls = ["AA"]

    return take_action(valve_dict, curr_valve, curr_time, open_valves_ls, curr_total_pressure, path_ls)


if __name__ == '__main__':
    print(f"{data[4]}")
