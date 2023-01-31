from aocd import data
"""
Part1: list represents calories carried by elves.  each elf's inventory is separated by a blank line.
Return the calories carried by the elsf with the most calories

"""

def food_list_by_elf(raw_input):
    """
    splits input string ny elf ('/n/n'), then by item per elf ('/n') then converts into int
    :param input_list: list of calories carried by all elves with individual elves separated by a blank line
    :return: array of list of items carried by each elf (each elf is an item in the array)
    """
    return list(map(lambda x: list(map(int,x.split("\n"))),raw_input.split("\n\n")))
def test_food_list_by_elf():
    with open("Day1_test_input.txt","r") as input_file:
        raw_input=input_file.read()
    assert food_list_by_elf(raw_input)==[
        [1000,2000,3000],
        [4000],
        [5000,6000],
        [7000,8000,9000],
        [10000]
    ]

def calories_by_elf(food_list_by_elf_ls):
    """

    :param food_list_by_elf_ls: list of each elf's inventory
    :return: the total amount of calories carried by each elf
    """
    return [sum(x) for x in food_list_by_elf_ls]

def test_calories_by_elf():
    assert calories_by_elf([
        [1000,2000,3000],
        [4000],
        [5000,6000],
        [7000,8000,9000],
        [10000]
    ])==[6000,4000,11000,24000,10000]

def  top_elf_calories(calories_by_elf_ls):
    return max(calories_by_elf_ls)

def test_top_elf_calories():
    assert top_elf_calories([6000,4000,11000,24000,10000])==24000

def top_thee_elf_calories(calories_by_elf_ls):
    calories_by_elf_ls.sort(reverse=True)
    return (sum(calories_by_elf_ls[:3]))

def test_top_thee_elf_calories():
    assert top_thee_elf_calories([6000,4000,11000,24000,10000])==45000

if __name__=="__main__":
    test_food_list_by_elf()
    test_calories_by_elf()
    food_by_elf_ls = food_list_by_elf(data)
    calories_by_elf_ls = calories_by_elf(food_by_elf_ls)

    print(f"The total calories carried by the top elf is {top_elf_calories(calories_by_elf_ls)}")
    print(f"The total calories carried by the top three elves is {top_thee_elf_calories(calories_by_elf_ls)}")

