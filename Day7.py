from aocd import data


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

def node_check(curr_node,node_dict,curr_item):
    """
    checks if curr_item is already a defined node.
    If it's defined, make sure it's consistent
    if it's a new node, add it
   :param curr_node: current node in directory (for parentage)
   :param node_dict: dictionary of mapped nodes
   :param curr_item: item to check and maybe add
   :return: node_dict with the new node added (if necessary)
    """
    if curr_item[0] == "dir":
        dir_name = curr_item[1]
        if dir_name in node_dict:  # if it's already defined
            # check to make sure parentage is correct
            if node_dict[dir_name].parent != curr_node:
                # raise error if it isn't
                raise Exception(f"error: {dir_name} is supposed to be a child of {curr_node.name} but its parent in the record is {node_dict[dir_name].parent.name}")
        else:  # define as new node
            node_dict[dir_name] = TreeNode(
               name=dir_name,
               type='dir',
               parent=curr_node,
           )

    else:  # it's a file
        file_name = curr_item[1]
        file_size = curr_item[0]

        if file_name in node_dict:  # if it's already defined
            # check to make sure parentage and size is correct
            if ((node_dict[file_name].parent != curr_node) or (node_dict[file_name].size != file_size)):
                # raise error if it isn't
                raise Exception(
                    f"error: {file_name} is supposed to be a child of {curr_node.name} and size {file_size} but its parent and size in the record is {node_dict[file_name].parent.name} and {node_dict[file_name].size}"
                    )
        else: #define as new node
            node_dict[file_name] = TreeNode(
                name=file_name,
                type='file',
                parent=curr_node,
                size=file_size,
            )
    return node_dict

def command_to_tree(commands_ls):
    """
    from list of commands, makes the directory tree (dictionary of nodes).
    :param input_filename: filename of command list
    :return: dictionary of nodes
    """
    command_index = 0
    node_dict = {'/': TreeNode(name="/", type="dir")}
    curr_node = node_dict['/']

    while command_index < len(commands_ls):
        curr_row = commands_ls[command_index]
        if curr_row[0] == '$':  # instruction
            curr_instruction = curr_row.split(" ")
            if curr_instruction[1] == "cd":
                new_node_name = curr_instruction[2]
                if new_node_name=="..":
                    curr_node = curr_node.parent
                    command_index += 1
                elif new_node_name in node_dict:
                    # new_node_name needs to be a child of curr_node unless it's root
                    if ((node_dict[new_node_name].parent == curr_node)|(curr_node.name=="/")):
                        curr_node = node_dict[new_node_name]
                        command_index += 1
                    else:
                        raise Exception(
                            f"node {new_node_name} is not a child of node {curr_node.name}"
                        )
                else:
                    raise Exception(
                        f"node {new_node_name} is not in the records"
                    )
            elif curr_instruction[1] == "ls":
                command_index += 1
                curr_row = commands_ls[command_index]
                while curr_row[0] != "$":
                    curr_item = curr_row.split(" ")
                    node_dict = node_check(curr_node,node_dict,curr_item)
                    command_index += 1
                    if command_index<len(commands_ls):
                        curr_row = commands_ls[command_index]
                    else:
                        curr_row="$" #in case the final command is in a "ls", breaks out of loop


    return node_dict

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


def calculate_directory_sizes(node_dict):
    """
    given a dictionary of nodes, calculates the total size of all the directories
    :param node_dict: dictionary of nodes
    :return: dictionary of directory names and node sizes
    """
    # filter to only the directories and calculate sizes
    directory_size_dict = {key:calculate_single_directory_size(value) for (key,value) in node_dict.items() if value.type =='dir'}
    return directory_size_dict

def part1_calculator(raw_data):
    """
    takes the raw input data and finds the sum of all directories with size < 100000
    :param raw_data: raw input data
    :return: sum of file sizes
    """
    test_command_ls = raw_data.split('\n')
    node_dict = command_to_tree(test_command_ls)
    directory_size_dict = calculate_directory_sizes(node_dict)
    return sum([size for size in directory_size_dict.values() if size < 100000])

if __name__ == "__main__":
    print(f"file sum is {part1_calculator(data)}")
