import unittest
from Day7 import TreeNode, node_check, command_to_tree

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

        g = TreeNode(name='g', type='dir', parent=f)
        tree_list = root.generate()

        self.assertEqual(tree_list,['\n\nroot',
                                     '│',
                                     '├── a',
                                     '│',
                                     '└── b',
                                     '    └── c',
                                     '        └── d',
                                     '            ├── e',
                                     '            │',
                                     '            └── f',
                                     '                └── g',
                                     '',
                                     '',
                                     '',
                                     '',
                                     ''
                                    ]
                         )

class test_node_check(unittest.TestCase):
    def test_node_check_existing_dir_pass(self):
        #if the curr_item alredy exists in node_dict with matching parameters
        node_dict = {
            "/":TreeNode(name = "/", type = "dir"),
        }
        node_dict["a"]= TreeNode(
            name='a',
            type='dir',
            parent=node_dict["/"],
        )
        self.assertEqual(
            node_check(
                node_dict["/"],
                node_dict,
                ["dir","a"]
            ),
            node_dict
        )

    def test_node_check_existing_dir_fail(self):
        #if the curr_item alredy exists in node_dict with differing parameters
        node_dict = {
            "/":TreeNode(name = "/", type = "dir"),
        }
        node_dict["a"]= TreeNode(
            name='a',
            type='dir',
            parent=node_dict["/"],
        )
        node_dict["b"] = TreeNode(
            name='b',
            type='dir',
            parent=node_dict["a"],
        )
        with self.assertRaises(Exception) as context:
            node_check(
                node_dict["/"],
                node_dict,
                ["dir","b"]
            )
        self.assertTrue(
            "error: b is supposed to be a child of / but its parent in the record is a" in str(context.exception))
    def test_node_check_new_dir(self):
        node_dict = {
            "/": TreeNode(name="/", type="dir"),
        }
        node_dict["a"] = TreeNode(
            name='a',
            type='dir',
            parent=node_dict["/"],
        )

        edited_dict = node_dict.copy()
        edited_dict["d"] = TreeNode(
            name='d',
            type='dir',
            parent=node_dict["/"],
        )

        self.assertEqual(
            [(x.name,x.parent,x.type) for x in node_check(
                node_dict["/"],
                node_dict,
                ["dir", "d"]
            ).values()],

            [(x.name,x.parent,x.type) for x in edited_dict.values()]
        )
    def test_node_check_existing_file_pass(self):
        #if the curr_item alredy exists in node_dict with matching parameters
        node_dict = {
            "/":TreeNode(name = "/", type = "dir"),
        }
        node_dict["b"]= TreeNode(
            name='b',
            type='file',
            parent=node_dict["/"],
            size = 14848514,
        )
        self.assertEqual(
            node_check(
                node_dict["/"],
                node_dict,
                [14848514,"b"]
            ),
            node_dict
        )

    def test_node_check_existing_file_fail(self):
        # if the curr_item alredy exists in node_dict with differing parameters
        node_dict = {
            "/": TreeNode(name="/", type="dir"),
        }
        node_dict["b"] = TreeNode(
            name='b',
            type='file',
            parent=node_dict["/"],
            size = 8504156,
        )
        with self.assertRaises(Exception) as context:
            node_check(
                node_dict["/"],
                node_dict,
                [14848514, "b"]
            )
        self.assertTrue(
            "error: b is supposed to be a child of / and size 14848514 but its parent and size in the record is / and 8504156" in str(context.exception))

    def test_node_check_new_file(self):
        node_dict = {
            "/": TreeNode(name="/", type="dir"),
        }
        node_dict["b"] = TreeNode(
            name='b',
            type='file',
            parent=node_dict["/"],
            size=14848514,
        )

        edited_dict = node_dict.copy()
        edited_dict["c"] = TreeNode(
            name='c',
            type='file',
            parent=node_dict["/"],
            size=8504156,
        )

        self.assertEqual(
            [(x.name,x.parent,x.size,x.type) for x in node_check(
                node_dict["/"],
                node_dict,
                [8504156, "c"]
            ).values()],

            [(x.name,x.parent,x.size,x.type) for x in edited_dict.values()]
        )
class test_command_to_tree(unittest.TestCase):

    def test_cd_non_existing_node(self):
        with self.assertRaises(Exception) as context:
            command_to_tree(['$ cd a'])
        self.assertTrue(
            "node a is not in the records" in str(context.exception)
        )


    def test_tree_maker(self):
        with open('Day7_test_input.txt') as input_file:
            raw_data = input_file.read()
        test_command_ls = raw_data.split('\n')
        root = command_to_tree(test_command_ls)
        self.assertEqual(
            root.generate(),
            ['\n\n/',
             '│',
             '├── b.txt',
             '├── c.dat',
             '├── a',
             '│   ├── f',
             '│   ├── g',
             '│   ├── h.lst',
             '│   └── e',
             '│       └── i',
             '│',
             '│',
             '└── d',
             '    ├── j',
             '    ├── d.log',
             '    ├── d.ext',
             '    └── k',
             '']
 )

if __name__ == '__main__':
    unittest.main()