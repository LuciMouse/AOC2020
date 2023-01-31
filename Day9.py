from aocd import data


def is_touching(head_posn, tail_posn):
    """
    given the head and tail positions, returns if they are within a square of each other
    :param head_posn: TUPLE coordinates of head
    :param tail_posn: TUPLE coordinates of tail
    :return: BOOL if the head and tail are "touching"
    """
    if head_posn == tail_posn:  # overlapping is touching
        return True
    if ((head_posn[0] == tail_posn[0]) & (abs(head_posn[1] - tail_posn[1]) == 1)):  # vertically touching
        return True
    if ((head_posn[1] == tail_posn[1]) & (abs(head_posn[0] - tail_posn[0]) == 1)):  # horizontally touching
        return True
    if ((abs(head_posn[0] - tail_posn[0]) == 1) & (abs(head_posn[1] - tail_posn[1]) == 1)):  # diagonal touch
        return True
    else:
        return False


def move_head(head_posn, direction):
    """
    given a direction and a head_posn, return the new head posn
    :param head_posn: TUPLE coordinates of head
    :param direction: one of R U L D
    :return: new coordinates of head
    """
    if direction == "U":
        return head_posn[0], head_posn[1] + 1
    if direction == "D":
        return head_posn[0], head_posn[1] - 1
    if direction == "R":
        return head_posn[0] + 1, head_posn[1]
    if direction == "L":
        return head_posn[0] - 1, head_posn[1]
    else:
        raise Exception("unacceptable direction")


def move_tail(head_posn, tail_posn):
    """
    upadates the tail position closer to the head_posn
    :param head_posn: coordinates of head
    :param tail_posn: coordinates of tail
    :return: updated coordinates of tail
    """
    # adjust x posn
    if head_posn[0] > tail_posn[0]:
        new_tail_x = tail_posn[0] + 1
    elif head_posn[0] < tail_posn[0]:
        new_tail_x = tail_posn[0] - 1
    else:
        new_tail_x = tail_posn[0]

    # adjust y posn
    if head_posn[1] > tail_posn[1]:
        new_tail_y = tail_posn[1] + 1
    elif head_posn[1] < tail_posn[1]:
        new_tail_y = tail_posn[1] - 1
    else:
        new_tail_y = tail_posn[1]

    return (new_tail_x, new_tail_y)


def execute_motion(head_posn, tail_posn, visited_set, instruction):
    """
    executes a specific instuction by moving the head and tail and updates the set of visited positions
    :param head_posn: coordinate of head
    :param tail_posn: coordinate of tail
    :param visited_set: set of visited positons
    :param instruction: movement to execute
    :return: tuple of updated head_posn, tail_posn, visited_set
    """
    direction = instruction[0]
    num_steps = int(instruction[1])

    for step in range(num_steps):
        head_posn = move_head(head_posn, direction)
        if not is_touching(head_posn, tail_posn):
            tail_posn = move_tail(head_posn, tail_posn)
        visited_set.add(tail_posn)
    return head_posn, tail_posn, visited_set

def execute_motion_ten_knots(positions_ls, visited_set, instruction):
    """
    executes a specific instuction by moving the head and tail and updates the set of visited positions
    :param positions_ls: positions of all ten knots, [0] is the head, [9] is the tail
    :param visited_set: set of visited positons of the tail
    :param instruction: movement to execute
    :return: tuple of updated positions_ls and visited_set
    """
    direction = instruction[0]
    num_steps = int(instruction[1])


    for step in range(num_steps):
        positions_ls[0] = move_head(positions_ls[0], direction) #move the first knot
        #check the other knots in pairs
        head_index = 0
        while ((head_index<9) and (not is_touching(positions_ls[head_index],positions_ls[head_index+1]))):
            positions_ls[head_index+1] = move_tail(positions_ls[head_index],positions_ls[head_index+1])
            if head_index==8: #tail knot of rope
                visited_set.add(positions_ls[head_index+1])
                # break
            head_index+=1
    return positions_ls, visited_set

def find_tail_positions(raw_data):
    """
    parses the series of motions and determines the number of positions visited by the tail
    :param raw_data: raw input
    :return: number of postions visited by the tail
    """
    instruction_list = [x.split(" ") for x in raw_data.split("\n")]
    visited_set = {(0,0)}
    head_posn = (0,0)
    tail_posn = (0,0)

    for instruction in instruction_list:
        head_posn,tail_posn,visited_set = execute_motion(
            head_posn,
            tail_posn,
            visited_set,
            instruction
        )
    return len(visited_set)

def find_ten_tail_positions(raw_data):
    """
        parses the series of motions and determines the number of positions visited by the tail
        :param raw_data: raw input
        :return: number of postions visited by the tail
    """
    instruction_list = [x.split(" ") for x in raw_data.split("\n")]
    visited_set = {(0, 0)}
    #this time there are ten points to track instead of 2
    knot_positions = [(0,0) for x in range(10)]

    for instruction in instruction_list:
        execute_motion_ten_knots(knot_positions,visited_set,instruction)
    return len(visited_set)


if __name__ == "__main__":
    print(f"number of visited positions:{find_tail_positions(data)}")
    print(f"number of visited positions with ten knots:{find_ten_tail_positions(data)}")
