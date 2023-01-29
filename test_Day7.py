import unittest
from Day7 import TreeNode, add_node, move_folder, command_to_tree, calculate_single_directory_size, calculate_directory_sizes,part1_calculator, part2_calculator


class TestTreeNode(unittest.TestCase):
    # test creating the root
    def test_root(self):
        root = TreeNode(name="root", type="dir")
        self.assertEqual(
            [root.name, root.type, root.size, root.parent, root.children],
            ["root", "dir", None, None, []])

    # test creating a root and a child (with defined parent)
    def test_root_child_defined_parent(self):
        # define root node
        root = TreeNode(name="root", type="dir")
        # define node a as a child of root
        a = TreeNode(name='a', type='dir', parent=root)
        self.assertEqual(
            [a.parent.name, [x.name for x in root.children]],
            ['root', ['a']]
        )

    # test creating two nodes and defining one as the child of the other
    def test_root_child_post_parent_definition(self):
        # define root node
        root = TreeNode(name="root", type="dir")
        # define node a
        a = TreeNode(name='a', type='dir')
        # define a as child to b
        root.AddChild(a)

        self.assertEqual(
            [a.parent.name, [x.name for x in root.children]],
            ['root', ['a']]
        )

    # test printing the tree structure

    def test_generate(self):
        root = TreeNode(name="root", type="dir")
        # define node a,b as children of root
        a = TreeNode(name='a', type='dir', parent=root)
        b = TreeNode(name='b', type='dir', parent=root)

        # define c as child of b
        c = TreeNode(name='c', type='dir', parent=b)

        d = TreeNode(name='d', type='dir', parent=c)

        e = TreeNode(name='e', type='dir', parent=d)
        f = TreeNode(name='f', type='dir', parent=d)

        g = TreeNode(name='g', type='dir', parent=f)
        tree_list = root.generate()

        self.assertEqual(tree_list, ['\n\nroot',
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


class test_add_node(unittest.TestCase):
    def test_add_node_dir(self):
        # add a directory node to the set
        curr_node = TreeNode(name="/", type="dir")
        node_set = {
            curr_node,
        }
        edited_set = node_set.copy()
        edited_set.add(TreeNode(
            name='a',
            type='dir',
            parent=curr_node,
        ))
        self.assertEqual(
            [(x.name, x.parent, x.size, x.type) for x in add_node(
                curr_node,
                node_set,
                ["dir", "a"]
            )],
            [(x.name, x.parent, x.size, x.type) for x in edited_set]
        )

    def test_add_node_file(self):
        curr_node = TreeNode(name="/", type="dir")
        node_set = {
            curr_node
        }
        edited_set = node_set.copy()
        edited_set.add(TreeNode(
            name='b',
            type='file',
            parent=curr_node,
            size=14848514,
        ))

        self.assertEqual(
            set([
                (x.name, x.parent, x.size, x.type) for x in add_node(
                    curr_node,
                    node_set,
                    [14848514, "b"]
                    )
                ]).difference(
            set([
                (x.name, x.parent, x.size, x.type) for x in edited_set
                ])
            ),
            set()
        )

class test_move_folder(unittest.TestCase):
    def test_cd_non_child_node_fail(self):
        # cd to a non-child node

        curr_node = TreeNode(name="/", type="dir")

        new_node = TreeNode(
            name='a',
            type='dir',
            parent=curr_node,
        )
        with self.assertRaises(Exception) as context:
            move_folder(curr_node, ['$', 'cd', 'b'])
        self.assertTrue(
            "node b is not a child of node /" in str(context.exception)
        )
    def test_cd_child_node(self):
        parent_node = TreeNode(name="/", type="dir")
        child_node = TreeNode(
            name='a',
            type='dir',
            parent=parent_node,
        )
        self.assertEqual(
            move_folder(parent_node,['$', 'cd', 'a']),
            child_node
        )
    def test_cd_parent_node(self):
        parent_node = TreeNode(name="/", type="dir")
        child_node = TreeNode(
            name='a',
            type='dir',
            parent=parent_node,
        )
        self.assertEqual(
            move_folder(child_node, ['$', 'cd', '..']),
            parent_node
        )

class test_command_to_tree(unittest.TestCase):

    def test_tree_maker(self):
        with open('Day7_test_input.txt') as input_file:
            raw_data = input_file.read()
        test_command_ls = raw_data.split('\n')
        node_set = command_to_tree(test_command_ls)
        self.assertEqual(
            set((
                (x.name, x.type, x.parent.name if x.parent != None else None,
                 tuple([y.name if y != None else None for y in x.children]), x.size) for x in node_set)).difference(
            set((('/', 'dir', None, ('a', 'b.txt', 'c.dat', 'd'), None),
             ('a', 'dir', '/', ('e', 'f', 'g', 'h.lst'), None),
             ('b.txt', 'file', '/', (), '14848514'),
             ('c.dat', 'file', '/', (), '8504156'),
             ('d', 'dir', '/', ('j', 'd.log', 'd.ext', 'k', 'y'), None),
             ('e', 'dir', 'a', ('i',), None),
             ('f', 'file', 'a', (), '29116'),
             ('g', 'file', 'a', (), '2557'),
             ('h.lst', 'file', 'a', (), '62596'),
             ('i', 'file', 'e', (), '584'),
             ('j', 'file', 'd', (), '4060174'),
             ('d.log', 'file', 'd', (), '8033020'),
             ('d.ext', 'file', 'd', (), '5626152'),
             ('k', 'file', 'd', (), '7214296'),
             ('y','dir','d',(),None)
                 ))),
            set()
        )
class test_calculate_single_directory_size(unittest.TestCase):
    def test_single_directory_size_1(self):

       root_node = TreeNode(
           name='/',
           type='dir',
       )

       node_a = TreeNode(
            name='a',
            type='dir',
            parent=root_node,
        )
       node_b_txt = TreeNode(
           name='b.txt',
           type='file',
           parent=root_node,
           size = 14848514,
       )
       node_c_dat = TreeNode(
           name='c.dat',
           type='file',
           parent=root_node,
           size = 8504156,
       )
       node_d = TreeNode(
           name='d',
           type='dir',
           parent=root_node,
       )
       node_e = TreeNode(
           name='e',
           type='dir',
           parent=node_a,
       )
       node_f = TreeNode(
           name='f',
           type='file',
           parent=node_a,
           size = 29116,
       )
       node_g = TreeNode(
           name='g',
           type='file',
           parent=node_a,
           size = 2557,
       )
       node_h_lst = TreeNode(
           name='h.lst',
           type='file',
           parent=node_a,
           size = 62596,
       )
       node_i = TreeNode(
           name='i',
           type='file',
           parent=node_e,
           size = 584,
       )
       node_j = TreeNode(
           name='j',
           type='file',
           parent=node_d,
           size = 4060174,
       )
       node_d_log = TreeNode(
           name='d.log',
           type='file',
           parent=node_d,
           size=8033020,
       )
       node_d_ext = TreeNode(
           name='d.ext',
           type='file',
           parent=node_d,
           size=5626152,
       )
       node_k = TreeNode(
           name='k',
           type='file',
           parent=node_d,
           size=7214296,
       )
       node_y = TreeNode(
           name='y',
           type='dir',
           parent=node_d,
       )
       self.assertEqual(
            [
                calculate_single_directory_size(node_e),
                calculate_single_directory_size(node_a),
                calculate_single_directory_size(node_d),
                calculate_single_directory_size(root_node),
                calculate_single_directory_size(node_y),
            ],
            [
                584,94853,24933642,48381165,0
            ]
       )

class test_calculate_directory_sizes(unittest.TestCase):
    def test_directory_size_1(self):
        with open('Day7_test_input.txt') as input_file:
            raw_data = input_file.read()
        test_command_ls = raw_data.split('\n')
        node_set = command_to_tree(test_command_ls)
        directory_size_set = set(calculate_directory_sizes(node_set))
        self.assertEqual(
            directory_size_set,
            {
                584,
                94853,
                24933642,
                48381165,
                0
            }
        )

class test_part_1_calculator(unittest.TestCase):
    def test_part_1(self):
        with open('Day7_test_input.txt') as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            part1_calculator(raw_data),
            95437
        )

class test_part_2_calculator(unittest.TestCase):
    def test_part_2(self):
        with open('Day7_test_input.txt') as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            part2_calculator(raw_data),
            24933642
        )
if __name__ == '__main__':
    unittest.main()
