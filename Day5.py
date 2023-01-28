import itertools

def data_formatter(raw_input):
    """
    takes the raw input and splits it into the diagram of the starting stacks and the rearrangement procedure
    :param raw_input: input file
    :return: separated diagram and instructions
    """
    #spit on the blank line
    raw_diagram,raw_instructions = raw_input.split("\n\n")

    #diagram: llisted from top to bottom of each stack

    split_diagram = [stack for stack in raw_diagram.split('\n')]
    num_stacks = len(split_diagram[-1].replace(" ",""))
    split_diagram = split_diagram[:-1]

    itemized_diagram = [[] for x in range(num_stacks)]
    for curr_layer in split_diagram:
        for stack_index in range(num_stacks):
            # each "item" is 3 char wide and are separated by a space. The crate character is the middle one
            curr_index = 1 + stack_index*4
            if (curr_index) <len(curr_layer):
                curr_item = curr_layer[curr_index]
                if curr_item != ' ':
                    itemized_diagram[stack_index].append(curr_item)

    #instructions
    split_instructions = [step.split(' ') for step in raw_instructions.split('\n')]
    split_instructions = [[int(x) for x in y if x not in {'move','from','to'}] for y in split_instructions]

    return ([itemized_diagram,split_instructions])

def test_data_formatter():
    with open("Day5_test_input.txt","r") as input_file:
        raw_test_input = input_file.read()
    assert data_formatter(raw_test_input) == [
           [
               ['N','Z'],
               ['D', 'C', 'M'],
               ['P']
           ],
           [
               [1, 2, 1],
               [3, 1, 3],
               [2, 2, 1],
               [1, 1, 2]
           ]
    ]

def step_implementer_9000(stack_diagram, curr_instruction):
    """
    performs the current step on the stack as diagrammed and returns the edited diagram
    :param stack_diagram: list of current state of stack
    :param curr_instruction: list of instruction in form [move,from,to]
    :return: edited stack diagram

    usage examples:

    >>> step_implementer_9000([['N', 'Z'],['D', 'C', 'M'],['P']],[1,2,1])
    [['D', 'N', 'Z'], ['C', 'M'], ['P']]

    >>> step_implementer_9000([['D', 'N', 'Z'], ['C', 'M'], ['P']],[3,1,3])
    [[], ['C', 'M'], ['Z', 'N', 'D', 'P']]

    >>> step_implementer_9000([[], ['C', 'M'], ['Z', 'N', 'D', 'P']],[2,2,1])
    [['M', 'C'], [], ['Z', 'N', 'D', 'P']]

    >>> step_implementer_9000([['M', 'C'], [], ['Z', 'N', 'D', 'P']],[1,1,2])
    [['C'], ['M'], ['Z', 'N', 'D', 'P']]
    """
    for loop_index in range(curr_instruction[0]):
        if len(stack_diagram[curr_instruction[1]-1])>0:
            #remove item from the top of the "from stack"
            curr_item = stack_diagram[curr_instruction[1]-1].pop(0)
            #add to the top of the "to stack"
            stack_diagram[curr_instruction[2]-1].insert(0,curr_item)
    return stack_diagram

def step_implementer_9001(stack_diagram, curr_instruction):
    """
    performs the current step on the stack as diagrammed and returns the edited diagram
    :param stack_diagram: list of current state of stack
    :param curr_instruction: list of instruction in form [move,from,to]
    :return: edited stack diagram

    usage examples:

    >>> step_implementer_9001([['N', 'Z'],['D', 'C', 'M'],['P']],[1,2,1])
    [['D', 'N', 'Z'], ['C', 'M'], ['P']]

    >>> step_implementer_9001([['D', 'N', 'Z'], ['C', 'M'], ['P']],[3,1,3])
    [[], ['C', 'M'], ['D', 'N', 'Z', 'P']]

    >>> step_implementer_9001([[], ['C', 'M'], ['D', 'N', 'Z', 'P']],[2,2,1])
    [['C', 'M'], [], ['D', 'N', 'Z', 'P']]

    >>> step_implementer_9001([['C', 'M'], [], ['D', 'N', 'Z', 'P']],[1,1,2])
    [['M'], ['C'], ['D', 'N', 'Z', 'P']]
    """
    num_crates = curr_instruction[0]
    from_stack_index = curr_instruction[1]-1
    to_stack_index = curr_instruction[2]-1

    # remove items from the top of the "from stack"
    if len(stack_diagram[from_stack_index])>0:
        crates_to_move = stack_diagram[from_stack_index][0:num_crates]
        stack_diagram[from_stack_index] = stack_diagram[from_stack_index][num_crates:]

        #add add to the front of the "to stack"
        stack_diagram[to_stack_index] = crates_to_move + stack_diagram[to_stack_index]
    return stack_diagram

def instruction_implementer(raw_input, crane_version):
    """
    takes the raw input, splits into stack diagram and instruction list,
    implements the instructions, and returns the top crate in each stack
    :param raw_input: unformatted data
    :return: list of top crates in each stack
    """
    stack_diagram, instruction_list = data_formatter(raw_input)
    if crane_version == "9000":
        for curr_instruction in instruction_list:
            stack_diagram = step_implementer_9000(stack_diagram, curr_instruction)
    elif crane_version == "9001":
        for curr_instruction in instruction_list:
            stack_diagram = step_implementer_9001(stack_diagram, curr_instruction)
    return "".join([x[0] if len(x)>0 else " " for x in stack_diagram ])

def test_instruction_implementer():
    with open("Day5_test_input.txt","r") as input_file:
        raw_test_input = input_file.read()
    assert instruction_implementer(raw_test_input, '9000') == 'CMZ'

if __name__ == "__main__":
    test_data_formatter()
    test_instruction_implementer()

    with open("Day5_input.txt","r") as input_file:
        raw_input = input_file.read()
    elf_message_1 = instruction_implementer(raw_input, '9000')
    elf_message_2 = instruction_implementer(raw_input, '9001')
    print(elf_message_1, elf_message_2 )