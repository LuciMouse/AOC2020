from aocd import data


class TreeNode():
    def __init__(self, coord, elevation, IsEnd, min_dist, children=None):
        self.coord = coord
        self.children = children
        self.elevation = elevation
        self.IsEnd = IsEnd
        self.min_dist = min_dist


def create_node(coord, height_map_ls):
    """
    create a new map node.  children are only added when the node is processed
    :param coord: coordinate of node
    :param height_map_ls: map of all position heights
    :return: new map node
    """
    elevation_value = height_map_ls[coord[0]][coord[1]]
    IsEnd = False #is this the destination point?
    if elevation_value.isupper():  # overwrite the elevation
        if elevation_value == "S":
            elevation_value = 'a'
        elif elevation_value == 'E':
            elevation_value = 'z'
            IsEnd = True
    new_node = TreeNode(
        coord=coord,
        elevation=elevation_value,
        IsEnd = IsEnd,
    )
    return new_node


def is_acessible(curr_elevation, child_coord, height_map_ls,processsed_node_set):
    child_elevation = height_map_ls[child_coord[0]][child_coord[1]]
    if child_elevation == "E": #end node has elevation 'z'
        child_elevation= 'z'
    if( (not child_coord in processsed_node_set) and
            ((ord(child_elevation)) <= (ord(curr_elevation) + 1))):
        return create_node(
            coord=child_coord,
            height_map_ls=height_map_ls
        )
    else:
        return None


def check_children(map_node,processsed_node_set, height_map_ls):
    """
    checks the ordinal points out of map_node and creates children of possible path nodes
    :param map_node: current node
    :param height_map_ls: map of all elevations
    :return: list of viable child nodes
    """
    curr_y_coord, curr_x_coord = map_node.coord
    curr_elevation = map_node.elevation

    children_ls = []

    # check left
    if curr_x_coord != 0:  # if a left position exists
        child_coord = (curr_y_coord, curr_x_coord - 1)
        child_node = is_acessible(curr_elevation, child_coord, height_map_ls,processsed_node_set)
        if child_node:
            children_ls.append(child_node)
    # check_right
    if curr_x_coord != len(height_map_ls[0]) - 1:  # if a right position exists
        child_coord = (curr_y_coord, curr_x_coord + 1)
        child_node = is_acessible(curr_elevation, child_coord, height_map_ls,processsed_node_set)
        if child_node:
            children_ls.append(child_node)

    # check_up
    if curr_y_coord != 0:  # if a upper position exists
        child_coord = (curr_y_coord - 1, curr_x_coord)
        child_node = is_acessible(curr_elevation, child_coord, height_map_ls,processsed_node_set)
        if child_node:
            children_ls.append(child_node)

    # check_down
    if curr_y_coord != len(height_map_ls) - 1:  # if a right position exists
        child_coord = (curr_y_coord + 1, curr_x_coord)
        child_node = is_acessible(curr_elevation, child_coord, height_map_ls,processsed_node_set)
        if child_node:
            children_ls.append(child_node)

    return children_ls


def process_node(unprocessed_node_ls,processsed_node_set, height_map_ls, min_path_count):
    """
    looks at first unprocessed node, sees if there are any possible paths out of the node, and creates appropriate child nodes
    :param unprocessed_node_ls: list of unprocesed nodes
    :param height_map_ls: map of all elevations
    :return:
    """
    curr_node = unprocessed_node_ls[0][0]
    curr_path_ls = unprocessed_node_ls[0][1]
    unprocessed_node_ls = unprocessed_node_ls[1:]
    processsed_node_set.add(curr_node.coord)

    #is this an end node?
    if curr_node.IsEnd:
        curr_path_length = len(curr_path_ls)-1
        if curr_path_length< min_path_count:
            return unprocessed_node_ls, curr_path_length
        else:
            return unprocessed_node_ls, min_path_count
    else: #look for children
        children_ls = check_children(curr_node,processsed_node_set, height_map_ls)
        if children_ls: #if children exist
            curr_node.children = children_ls

            for curr_child in children_ls:
                unprocessed_node_ls.append(
                    (curr_child,curr_path_ls+[(curr_child.coord,curr_child.elevation)])
                )

    return unprocessed_node_ls, min_path_count


def min_steps_path_finder(raw_data):
    """
    takes raw data and finds the minimum path from S to E
    :param raw_data: raw input
    :return: number of steps in minimum path
    """
    # import data and turn into array
    height_map_ls = [[*row] for row in raw_data.split('\n')]

    # find the start coord
    y_coord = [height_map_ls.index(curr_list) for curr_list in height_map_ls if "S" in curr_list][0]
    x_coord = height_map_ls[y_coord].index("S")

    # make the start node
    curr_node = create_node((y_coord, x_coord), height_map_ls)
    curr_node_path_ls = [((0,0),'a')]  # series of nodes between this node and the start node

    unprocessed_node_ls = [(curr_node,curr_node_path_ls)] #list of nodes that need to be processed
    processed_node_dict ={curr_node.coord,curr_node}
    min_path_count = len(height_map_ls)*len(height_map_ls[0]) #inital count is all the nodes in the heightmap
    # process node

    while len(unprocessed_node_ls)>0:
        unprocessed_node_ls,min_path_count = process_node(unprocessed_node_ls,processsed_node_set, height_map_ls,min_path_count)

    return min_path_count


if __name__ == '__main__':
    print(f"length of minimum path: {min_steps_path_finder(data)}")
