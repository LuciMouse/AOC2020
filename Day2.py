import pandas as pd
import functools

from aocd import data

opponent_identiy_dict = {
    "A":"Rock",
    "B":"Paper",
    "C":"Scissors",
}

player_identiy_dict = {
    "X":"Rock",
    "Y":"Paper",
    "Z":"Scissors",
}

shape_score_dict = {
    "Rock":1,
    "Paper":2,
    "Scissors":3,
}

outcome_score_dict = {
    "X":0,
    "Y":3,
    "Z":6,
}

def total_score_calculator_outcome(guide_df):
    """
    given a dataframe where the first column is opponent choice and the second column is the desired outcome, calculates total score
    :param guide_df: dataframe
    :return: total score
    """
    return functools.reduce(lambda x, y: x + y, guide_df.apply(rps_round_score_calculator_outcome, axis=1))

def rps_round_score_calculator_outcome(round_tuple):
    """
    determines the score given the (opponent_choice, desired_outcome) tuple
    :param round_tuple: tuple of the opponents play and the desired outcome
    :return: resulting sum of shape and outcome scores

    usage examples

    >>> rps_round_score_calculator_outcome(("A","Y"))
    4

    >>> rps_round_score_calculator_outcome(("B","X"))
    1

    >>> rps_round_score_calculator_outcome(("C","Z"))
    7
    """
    opponent_shape = opponent_identiy_dict[round_tuple[0]]
    desired_outcome = round_tuple[1]
    player_shape = player_shape_calculator(opponent_shape, desired_outcome)
    player_shape_score = shape_score_dict[player_shape]
    round_outcome_score = outcome_score_dict[desired_outcome]
    return player_shape_score + round_outcome_score

def player_shape_calculator(opponent_shape, desired_outcome):
    """
    given the opponent's play and the desired outcome, returns what the player shape should be
    :param opponent_shape: one of "Rock", "Paper", "Scissors"
    :param desired_outcome: one of "X"(lose), "Y"(draw), "Z"(win)
    :return: one of "Rock", "Paper", "Scissors"

    usage examples

    >>> player_shape_calculator("Rock","Y")
    'Rock'

    >>> player_shape_calculator("Paper","X")
    'Rock'

    >>> player_shape_calculator("Scissors","Z")
    'Rock'
    """

    if desired_outcome == "Y": #tie
        return opponent_shape
    elif desired_outcome == "X": #lose
        if opponent_shape == "Rock":
            return "Scissors"
        elif opponent_shape == "Paper":
            return "Rock"
        elif opponent_shape == "Scissors":
            return "Paper"
        else:
            print(f"error: opponent played {opponent_shape}, desired_outcome {desired_outcome}")
    elif desired_outcome == "Z": #win
        if opponent_shape == "Rock":
            return "Paper"
        elif opponent_shape == "Paper":
            return "Scissors"
        elif opponent_shape == "Scissors":
            return "Rock"
        else:
            print(f"error: opponent played {opponent_shape}, desired_outcome {desired_outcome}")
    else:
        print(f"error: opponent played {opponent_shape}, desired_outcome {desired_outcome}")

def test_total_score_calculator_outcome():
    with open("Day2_test_input.txt") as input_csv:
        test_guide_df = pd.read_csv(input_csv, header = None, sep = ' ')
    assert total_score_calculator_outcome(test_guide_df) == 12

def total_score_calculator(guide_df):
    """
    given a dataframe of shape choices, iterates through each pair of shapes and calculates total score
    :param guide_df: dataframe of shape choices
    :return: total score
    """
    return functools.reduce(lambda x,y: x+y,guide_df.apply(rps_round_score_calculator, axis = 1))

def test_total_score_calculator():
    with open("Day2_test_input.txt") as input_csv:
        test_guide_df = pd.read_csv(input_csv, header = None, sep = ' ')
    assert total_score_calculator(test_guide_df) == 15

def rps_round_score_calculator(round_tuple):
    """
    determines the score given the two choices in the round_tuple
    :param round_tuple: tuple describing my play and the opponents play
    :return: resulting sum of shape and outcome scores

    usage examples

    >>> rps_round_score_calculator(("A","Y"))
    8

    >>> rps_round_score_calculator(("B","X"))
    1

    >>> rps_round_score_calculator(("C","Z"))
    6
    """
    opponent_shape = opponent_identiy_dict[round_tuple[0]]
    player_shape = player_identiy_dict[round_tuple[1]]
    player_shape_score = shape_score_dict[player_shape]
    round_outcome_score = round_outcome_score_calculator(opponent_shape,player_shape)
    return player_shape_score + round_outcome_score

def round_outcome_score_calculator(opponent_shape, player_shape):
    """
    determines the score of the outcome of the round
    :param opponent_shape: one of "Rock", "Paper", "Scissors"
    :param player_shape: one of "Rock", "Paper", "Scissors"
    :return: player score

    Usage examples:

    >>> round_outcome_score_calculator("Rock","Scissors")
    0

    >>> round_outcome_score_calculator("Scissors","Rock")
    6

    >>> round_outcome_score_calculator("Paper","Paper")
    3

    >>> round_outcome_score_calculator("Paper","Rock")
    0

    """
    if opponent_shape == player_shape: #tie
        return 3
    # Not a tie
    elif opponent_shape  == "Rock":
        if player_shape == "Paper":
            return 6 #win
        elif player_shape == "Scissors":
            return 0 #loss
        else:
            print(f"error: opponent played {opponent_shape}, player played {player_shape}")
    elif opponent_shape  == "Paper":
        if player_shape == "Rock":
            return 0 #loss
        elif player_shape == "Scissors":
            return 6 #win
        else:
            print(f"error: opponent played {opponent_shape}, player played {player_shape}")
    elif opponent_shape == "Scissors":
        if player_shape == "Paper":
            return 0  # loss
        elif player_shape == "Rock":
            return 6  # win
        else:
            print(f"error: opponent played {opponent_shape}, player played {player_shape}")
    else:
        print(f"error: opponent played {opponent_shape}, player played {player_shape}")

if __name__=="__main__":
    test_total_score_calculator()
    test_total_score_calculator_outcome()


    guide_df = pd.DataFrame([row.split(' ') for row in data.split('\n')])
    print(f"Part 1 total score: {total_score_calculator(guide_df)}")
    print(f"Part 2 total score: {total_score_calculator_outcome(guide_df)}")

