from aocd import data
from random import randrange

class TreeNode:
    def __init__(self, name, type, size=None, parent=None):
        self.children = []
        self.name = name
        self.type = type
        self.size = size
        self.parent = parent
        self._generator = _TreeGenerator(self)

        # if node has a defined parent, add the node as a child to that parent
        if self.parent is not None:
            self.parent.AddChild(self)

    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)
        return tree

    def AddChild(self, child_node):
        # creates parent-child relationships
        print(f"Adding {child_node.type} {child_node.name} as child of {self.name}")
        self.children.append(child_node)
        # if child's parent is not set, set to node
        if child_node.parent == None:
            child_node.parent = self


class _TreeGenerator:
    # for drawing the tree
    PIPE = "│"
    ELBOW = "└──"
    TEE = "├──"
    PIPE_PREFIX = "│   "
    SPACE_PREFIX = "    "

    def __init__(self, root_node):
        self._tree = []
        self._root_node = root_node

    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_node)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"\n\n{self._root_node.name}")
        self._tree.append(self.PIPE)

    def _tree_body(self, root_node, prefix=""):
        entries = root_node.children
        entries = sorted(entries, key=lambda entry: entry.type == 'dir')
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = self.ELBOW if index == entries_count - 1 else self.TEE
            if (entry.type == 'dir'):
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _add_directory(
            self, directory, index, entries_count, prefix, connector
    ):
        self._tree.append(f"{prefix}{connector} {directory.name}")
        if index != entries_count - 1:
            prefix += self.PIPE_PREFIX
        else:
            prefix += self.SPACE_PREFIX
        self._tree_body(
            root_node=directory,
            prefix=prefix
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")

def add_node(curr_node, node_set, curr_item):
    """
    checks if curr_item is file or directory and adds it to the set
   :param curr_node: current node in directory (for parentage)
   :param node_set: set of mapped nodes
   :param curr_item: item to check and add
   :return: node_set with the new node added
    """
    if curr_item[0] == "dir":
        dir_name = curr_item[1]

        node_set.add(TreeNode(
           name=dir_name,
           type='dir',
           parent=curr_node,
           ))

    else:  # it's a file
        file_name = curr_item[1]
        file_size = curr_item[0]

        node_set.add(TreeNode(
            name=file_name,
            type='file',
            parent=curr_node,
            size=file_size,
        ))
    return node_set

def move_folder(curr_node, curr_instruction):
    new_node_name = curr_instruction[2]
    if new_node_name == "..":
        curr_node = curr_node.parent

    elif new_node_name in {child_node.name for child_node in
                           curr_node.children}:  # move to child node. check to make sure new_node is a child of the current node
        curr_node = [child_node for child_node in curr_node.children if child_node.name == new_node_name][0]
    else:
        raise Exception(
            f"node {new_node_name} is not a child of node {curr_node.name}"
        )
    return curr_node

def command_to_tree(commands_ls):
    """
    from list of commands, makes the directory tree (set of nodes).
    :param input_filename: filename of command list
    :return: set of nodes
    """
    command_index = 1 #first command is "cd /" which sets the current node at the root node.
    curr_node = TreeNode(name="/", type="dir")
    node_set = {curr_node}

    while command_index < len(commands_ls):
        curr_row = commands_ls[command_index]
        if curr_row[0] == '$':  # instruction
            curr_instruction = curr_row.split(" ")
            if curr_instruction[1] == "cd":
                curr_node = move_folder(curr_node,curr_instruction)
                command_index += 1
            elif curr_instruction[1] == "ls":
                command_index += 1 #read next command
                curr_row = commands_ls[command_index]
                while curr_row[0] != "$":
                    curr_item = curr_row.split(" ")
                    node_dict = add_node(curr_node, node_set, curr_item)
                    command_index += 1
                    if command_index<len(commands_ls):
                        curr_row = commands_ls[command_index]
                    else:
                        curr_row="$" #in case the final command is in a "ls", breaks out of loop


    return node_set

def calculate_single_directory_size(curr_node):
    """
    given a directory node, calculates the size of the node
    :param curr_node: a Treenode of type= 'dir'
    :return: size of all contained nodes
    """
    if curr_node.type == 'file': #files have no children
        return int(curr_node.size)
    elif curr_node.children: #if it has children
        return sum([calculate_single_directory_size(curr_child) for curr_child in curr_node.children])
    else: #directory with no children
        return 0


def calculate_directory_sizes(node_set):
    """
    given a dictionary of nodes, calculates the total size of all the directories
    :param node_dict: dictionary of nodes
    :return: dictionary of directory names and node sizes
    """
    # filter to only the directories and calculate sizes
    directory_size_ls = [calculate_single_directory_size(node) for node in node_set if node.type =='dir']
    return directory_size_ls

def part1_calculator(raw_data):
    """
    takes the raw input data and finds the sum of all directories with size < 100000
    :param raw_data: raw input data
    :return: sum of file sizes
    """
    test_command_ls = raw_data.split('\n')
    node_set = command_to_tree(test_command_ls)
    directory_size_ls = calculate_directory_sizes(node_set)
    return sum([size for size in directory_size_ls if size < 100000])

def part2_calculator(raw_data):
    """
        takes the raw input data and finds the smallest directory that will free up the required space
        :param raw_data: raw input data
        :return: size of the smallest deletable directory
        """
    test_command_ls = raw_data.split('\n')
    node_set = command_to_tree(test_command_ls)
    directory_size_ls = calculate_directory_sizes(node_set)
    directory_size_ls.sort()

    #calculate room we need
    total_disk_size = 70000000
    min_disk_space = 30000000
    unused_space = total_disk_size-directory_size_ls[-1]
    min_dir_size = min_disk_space-unused_space

    big_dirs_ls = [size for size in directory_size_ls if size > min_dir_size]
    return big_dirs_ls[0]

if __name__ == "__main__":
    print(f"file sum is {part1_calculator(data)}")
    print(f"size of smallest deletable drive is {part2_calculator(data)}")
