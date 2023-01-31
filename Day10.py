from aocd import data

def interpret_instruction(register_value, instruction):
    """
    given the instruction, updates the cycle num and register value accordingly
    :param register_value: value of register x
    :param instruction: instruction to implement
    :return: register_value for the next cycle (or two cycles) depending on circumstance

    example usage:

    >>> interpret_instruction(1,"noop")
    [1]

    >>> interpret_instruction(1,"addx 3")
    [1, 4]

    >>> interpret_instruction(4,"addx -5")
    [4, -1]
    """
    if instruction[:4]=="noop": #takes one cycle, does not affect register value
        return [register_value]
    elif instruction[:4]=="addx": #takes two cycles, changes register value after both cycles
        value = int(instruction.split(' ')[1])
        return [register_value, register_value+value]

def interpret_instruction_ls(instruction_ls):
    """
    takes list of instructions and returns resulting list of cycle_num,register_value pairs
    :param instruction_ls: list of instructions
    :return: list where index is the cycle number and value is the register value after the cycle completes

    example usage:
    >>> interpret_instruction_ls(["noop","addx 3","addx -5"])
    [1, 1, 1, 4, 4, -1]
    """
    register_value = 1
    cycle_register_ls = [1] #value is at the *end* of the cycle

    for instruction in instruction_ls:
        new_value = interpret_instruction(register_value, instruction)
        register_value = new_value[-1]
        cycle_register_ls+=new_value
    return cycle_register_ls


def find_register_value_at_cycle(target_cycle, cycle_register_ls):
    """
    finds the value of the register at the target cycle
    :param target_cycle: cycle we need to find
    :param cycle_register_ls: value of register during cycle target_cycle
    :return: register value at target_cycle

    >>> find_register_value_at_cycle(4,[1, 1, 1, 4, 4, -1])
    4

    >>> find_register_value_at_cycle(2,[1, 1, 1, 4, 4, -1])
    1
    """
    return cycle_register_ls[target_cycle-1]



def signal_strength_analyzer(raw_data):
    """
    takes the raw data, interprets the instruction, and returns the sum of all "interesting" signal strengths
    :param raw_data: raw input
    :return: sum of all interesting signal strengths
    """
    #interpret instructions into register value at each cycle
    instruction_ls = raw_data.split('\n')
    cycle_register_ls = interpret_instruction_ls(instruction_ls)

    # find signal strength at the 20th cycle and every 40 cycles past that

    initial_cycle = 20
    signal_strength_ls =[]

    for target_cycle_num in range(initial_cycle,221,40):
        register_value = find_register_value_at_cycle(target_cycle_num,cycle_register_ls)
        signal_strength_ls.append(target_cycle_num*register_value)
    return sum(signal_strength_ls)

def sprite_tracker(cycle_register_ls):
    """
    for each cycle (index), determines if the sprite overlaps the current pixel being drawn
    :param cycle_register_ls: list of register values at each cycle (note that cycle 0 is the first index, but the program starts at cycle 1)
    :return: list of lit (#) or unlit (.) pixels split into 40 pixel sublists
    """
    num_rows = len(cycle_register_ls)//40
    pixel_ls = []
    for curr_row_num in range(num_rows):
        crt_row = []
        cycle_register_sublist_ls = cycle_register_ls[curr_row_num*40:(curr_row_num+1)*40] #40 item blocks
        for cycle_num in range(40): #the actual cycle number is 1 more since it's 1-index not 0
            register_value = cycle_register_sublist_ls[cycle_num]
            sprite_set = {x for x in range(register_value-1,register_value+2)} #set of positions the sprite overlaps
            if cycle_num in sprite_set:
                crt_row.append('#')
            else:
                crt_row.append('.')
        pixel_ls.append(crt_row)

    return pixel_ls

def crt_printer(raw_data):
    """
    takes the raw data and prints the resulting image to the screen
    :param raw_data: raw input
    :return: none
    """
    # interpret instructions into register value at each cycle
    instruction_ls = raw_data.split('\n')
    cycle_register_ls = interpret_instruction_ls(instruction_ls)

    #for each cycle, determine if the sprite overlaps the x register
    crt_putput_ls = sprite_tracker(cycle_register_ls)
    for row in crt_putput_ls:
        print(f"{''.join(row)}")



if __name__=="__main__":
    print(f"sum of six signal strengths: {signal_strength_analyzer(data)}")
    crt_printer(data)