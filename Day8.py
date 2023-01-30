import pandas as pd
from aocd import data

def is_visible(grid_df, curr_location):
    """
    determines if the value in the curr_location is visible from outside the grid
    :param grid_df: dataframe of all trees
    :param location: location to check
    :return: bool of whether the location is visible from outside the grid
    """
    row_coord = curr_location[0]
    col_coord = curr_location[1]

    location_value = grid_df.iloc[row_coord,col_coord]
    #check each side
    cardinal_series_ls = [
        grid_df.loc[row_coord, :col_coord - 1], #west of curr_position
        grid_df.loc[:row_coord-1, col_coord],  # north of curr_position
        grid_df.loc[row_coord, col_coord+1:],  # east of curr_position
        grid_df.loc[row_coord+1:, col_coord],  # south of curr_position
    ]
    for curr_direction_s in cardinal_series_ls:
        if curr_direction_s.max() < location_value: #if the maximum value is less than the tree in curr_location
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
    row_coord = curr_location[0]
    col_coord = curr_location[1]

    location_value = grid_df.iloc[row_coord, col_coord]
    # check each side, front of list is closest to tree, empty series if edge tree
    cardinal_series_ls = [
        grid_df.loc[row_coord, :col_coord - 1][::-1] if col_coord>0 else pd.Series(),  # west of curr_position
        grid_df.loc[:row_coord - 1, col_coord][::-1] if row_coord>0 else pd.Series(),  # north of curr_position
        grid_df.loc[row_coord, col_coord + 1:] if col_coord<grid_df.index.size else pd.Series(),  # east of curr_position
        grid_df.loc[row_coord + 1:, col_coord] if row_coord<grid_df.columns.size else pd.Series(),  # south of curr_position
    ]
    product =1
    for curr_direction_s in cardinal_series_ls:
        taller_trees_bool_s = curr_direction_s.apply(lambda x: x>=location_value).reset_index(drop= True) #reset the index
        taller_trees_s = taller_trees_bool_s[taller_trees_bool_s]
        if taller_trees_s.empty:#all trees are shorter than current tree
            product*=len(curr_direction_s)
        else:
            closest_tree_index = taller_trees_s.index.values[0]
            product*=closest_tree_index+1
    return product

def max_scenic_score(raw_data):
    """
    calculates scenic score from each position and returns the highest one
    :param raw_data: raw_input
    :return: highest scenic_score
    """
    split_data = [y for y in raw_data.split("\n")]
    grid_df = pd.DataFrame([[*x] for x in split_data]).applymap(lambda x: int(x))
    coord_list = [(x,y) for x in range(1,grid_df.index.size-1) for y in range(1,grid_df.columns.size-1)] #it's caught in the code, but since all edge trees have one 0 view, don't bother to test them
    scenic_score_ls = list(map(lambda x: calculate_scenic_score(grid_df,x),coord_list))
    return max(scenic_score_ls)

if __name__=="__main__":
    print(f"there are {num_visible(data)} trees visible from outside the grid")
    print(f"the highest scenic score possible is {max_scenic_score(data)}")