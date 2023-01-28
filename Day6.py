from aocd import data

def sop_marker_finder(datastring):
    """
    given the datastring, finds the number of characters that need to be processed before the "start of packet" marker
    (first 4 distinct characters) is found
    :param datastring: string of characters to analyze
    :return: number of characters that needed to be processed to find the sop marker

    usage examples:
    >>> sop_marker_finder("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    7

    >>> sop_marker_finder("bvwbjplbgvbhsrlpgdmjqwftvncz")
    5

    >>> sop_marker_finder("nppdvjthqldpwncqszvftbrmjlhg")
    6

    >>> sop_marker_finder("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    10

    >>> sop_marker_finder("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    11
    """

    for index in range(len(datastring)):
       if len(set(datastring[index:index+4]))==4:
           return index+4

def som_marker_finder(datastring):
    """
    given the datastring, finds the number of characters that need to be processed before the "start of message" marker
    (first 14 distinct characters) is found
    :param datastring: string of characters to analyze
    :return: number of characters that needed to be processed to find the som marker

    usage examples:
    >>> som_marker_finder("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
    19

    >>> som_marker_finder("bvwbjplbgvbhsrlpgdmjqwftvncz")
    23

    >>> som_marker_finder("nppdvjthqldpwncqszvftbrmjlhg")
    23

    >>> som_marker_finder("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    29

    >>> som_marker_finder("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    26
    """

    for index in range(len(datastring)):
       if len(set(datastring[index:index+14]))==14:
           return index+14



if __name__ == "__main__":

    print(f"sop numchars = {sop_marker_finder(data)}")
    print(f"som numchars = {som_marker_finder(data)}")