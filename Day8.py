import pandas as pd
from aocd import data

def is_visible(grid_df, curr_location):
    """
    determines if the value in the curr_location is visible from outside the grid
    :param grid_df: dataframe of all trees
    :param location: location to check
    :return: bool of whether the location is visible from outside the grid
    """
    x_coord = curr_location[0]
    y_coord = curr_location[1]

    location_value = grid_df.iloc[x_coord,y_coord]
    #check each side
    cardinal_series_ls = [
        grid_df.loc[x_coord, :y_coord - 1], #west of curr_position
        grid_df.loc[:x_coord-1, y_coord],  # north of curr_position
        grid_df.loc[x_coord, y_coord+1:],  # east of curr_position
        grid_df.loc[x_coord+1:, y_coord],  # south of curr_position
    ]
    for curr_position in cardinal_series_ls:
        if curr_position.max() < location_value: #if the maximum value is less than the tree in curr_location
            return True
    return False

def num_visible(raw_data):
    """
    takes the raw data, formats into dataframe, and counts number of visible trees
    :param raw_data: raw input
    :return: number of visible trees
    """
    split_data = [y for y in raw_data.split("\n")]
    grid_df = pd.DataFrame([[*x] for x in split_data]).applymap(lambda x: int(x))
    #outer ring of trees are all visible, only need to check inner trees
    coord_list = [(x, y) for x in range(1, grid_df.index.size - 1) for y in range(1, grid_df.columns.size - 1)]
    visible_tree_ls = list(map(lambda x: is_visible(grid_df,x),coord_list))

    #count visible trees

    #outer ring
    outer_trees = (grid_df.index.size *2)+(grid_df.columns.size*2)-4 #corners are all double counted
    inner_trees = sum(visible_tree_ls)
    return outer_trees + inner_trees

def calculate_scenic_score(grid_df,curr_location):
    """
    calculates the number of trees visible from the current location
    :param grid_df: dataframe of tree heighs
    :param curr_location: location to check
    :return: tree score of current location
    """


if __name__=="__main__":
    print(f"there are {num_visible(data)} trees visible from outside the grid")