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
        print(f"Adding {child_node.name} as child of {self.name}")
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
        self._tree.append(f"{self._root_node.name}")
        self._tree.append(self.PIPE)

    def _tree_body(self, root_node, prefix=""):
        entries = root_node.children
        entries = sorted(entries, key=lambda entry: entry.type == 'dir')
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = self.ELBOW if index == entries_count - 1 else self.TEE
            if entry.type == 'dir':
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)
    def _add_directory(
            self, directory, index, entries_count, prefix, connector
    ):
        self._tree.append(f"{prefix}{connector} {directory.name}")
        if index != entries_count -1:
            prefix += self.PIPE_PREFIX
        else:
            prefix += self.SPACE_PREFIX
        self._tree_body(
            directory = directory,
            prefix=prefix
        )
        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")

def command_to_tree(commands_ls):
    """
    from list of commands, makes the directory tree.
    :param input_filename: filename of command list
    :return: None
    """
    print("foo")

if __name__ == "__main__":
    with open('Day7_test_input.txt') as input_file:
        print("foo")
