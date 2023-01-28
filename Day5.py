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
    split_diagram = split_diagram[:-1][::-1]
    num_stacks = len(split_diagram)
    for curr_layer in split_diagram:
        for curr_index in range(num_stacks):

    substring_ls = [raw_diagram[x*num_stacks:(x+1)*num_stacks] for x in range(num_stacks)]
    del split_diagram[len(split_diagram)-1] #drop the 1,2,3 row
    itemized_diagram = [[y for y in list(x) if y not in {']','['}] for x in split_diagram]

    # transpose the lists (need to fill with None for unequal list size
    transposed_diagram = list(map(list,itertools.zip_longest(*itemized_diagram, fillvalue=None)))
    transposed_diagram = [[x for x in y if x not in {None,' '}] for y in transposed_diagram] #remove None and blanks


    #instructions
    split_instructions = [step.split(' ') for step in raw_instructions.split('\n')]
    split_instructions = [[int(x) for x in y if x not in {'move','from','to'}] for y in split_instructions]

    return ([transposed_diagram,split_instructions])

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

def step_implementer(stack_diagram, curr_instruction):
    """
    performs the current step on the stack as diagrammed and returns the edited diagram
    :param stack_diagram: list of current state of stack
    :param curr_instruction: list of instruction in form [move,from,to]
    :return: edited stack diagram

    usage examples:

    >>> step_implementer([['N', 'Z'],['D', 'C', 'M'],['P']],[1,2,1])
    [['D', 'N', 'Z'], ['C', 'M'], ['P']]

    >>> step_implementer([['D', 'N', 'Z'], ['C', 'M'], ['P']],[3,1,3])
    [[], ['C', 'M'], ['Z', 'N', 'D', 'P']]

    >>> step_implementer([[], ['C', 'M'], ['Z', 'N', 'D', 'P']],[2,2,1])
    [['M', 'C'], [], ['Z', 'N', 'D', 'P']]

    >>> step_implementer([['M', 'C'], [], ['Z', 'N', 'D', 'P']],[1,1,2])
    [['C'], ['M'], ['Z', 'N', 'D', 'P']]
    """
    for loop_index in range(curr_instruction[0]):
        if len(stack_diagram[curr_instruction[1]-1])>0:
            #remove item from the top of the "from stack"
            curr_item = stack_diagram[curr_instruction[1]-1].pop(0)
            #add to the top of the "to stack"
            stack_diagram[curr_instruction[2]-1].insert(0,curr_item)
        if len(stack_diagram)>9:
            print((curr_instruction,stack_diagram))
    return stack_diagram

def instruction_implementer(raw_input):
    """
    takes the raw input, splits into stack diagram and instruction list,
    implements the instructions, and returns the top crate in each stack
    :param raw_input: unformatted data
    :return: list of top crates in each stack
    """
    stack_diagram, instruction_list = data_formatter(raw_input)
    for curr_instruction in instruction_list:
        stack_diagram = step_implementer(stack_diagram,curr_instruction)
    return "".join([x[0] if len(x)>0 else " " for x in stack_diagram ])

def test_instruction_implementer():
    with open("Day5_test_input.txt","r") as input_file:
        raw_test_input = input_file.read()
    assert instruction_implementer(raw_test_input) == 'CMZ'

if __name__ == "__main__":
    test_data_formatter()
    test_instruction_implementer()

    with open("Day5_input.txt","r") as input_file:
        raw_input = input_file.read()
    elf_message_1 = instruction_implementer(raw_input)
    print(elf_message_1 )