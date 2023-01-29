import unittest
from Day7 import TreeNode, _TreeGenerator, command_to_tree

class TestTreeNode(unittest.TestCase):
    #test creating the root
    def test_root(self):
        root = TreeNode(name = "root", type = "dir")
        self.assertEqual(
            [root.name, root.type, root.size, root.parent, root.children],
            ["root","dir",None,None,[]])

    #test creating a root and a child (with defined parent)
    def test_root_child_defined_parent(self):
        #define root node
        root = TreeNode(name="root", type="dir")
        #define node a as a child of root
        a = TreeNode(name='a', type='dir', parent=root)
        self.assertEqual(
            [a.parent.name,[x.name for x in root.children]],
            ['root',['a']]
        )
    #test creating two nodes and defining one as the child of the other
    def test_root_child_post_parent_definition(self):
        # define root node
        root = TreeNode(name="root", type="dir")
        # define node a
        a = TreeNode(name='a', type='dir')
        #define a as child to b
        root.AddChild(a)

        self.assertEqual(
            [a.parent.name, [x.name for x in root.children]],
            ['root', ['a']]
        )
    #test printing the tree structure

    def test_generate(self):
        root = TreeNode(name="root", type="dir")
        # define node a,b as children of root
        a = TreeNode(name='a', type='dir', parent=root)
        b = TreeNode(name='b', type='dir', parent=root)

        #define c as child of b
        c = TreeNode(name='c', type='dir', parent=b)

        d = TreeNode(name='d', type='dir',parent=c)

        e = TreeNode(name='e', type='dir',parent=d)
        f = TreeNode(name='f', type='dir',parent=d)
        tree_list = root.generate()

        self.assertEqual(tree_list,"a")

class test_command_to_tree(unittest.TestCase):
    def test_tree_maker(self):
        with open('Day7_test_input.txt') as input_file:
            raw_data = input_file.read()
        test_command_ls = raw_data.split('\n')
        command_to_tree(test_command_ls)
        self.assertEqual(
            [],
            []
        )
if __name__ == '__main__':
    unittest.main()
