import unittest
import Day19


class TestFormatData(unittest.TestCase):
    def test_format_data(self):
        with open("Day19_test_input.txt", "r") as input_file:
            raw_input = input_file.read()
        blueprint_1 = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )

        blueprint_2 = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=2
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=3
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=8,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=3,
                    obsidian_cost=12
                )
            }
        )
        output_ls = [blueprint_1, blueprint_2]

        self.assertEqual(
            [
                [
                    [
                        robot.type,
                        robot.ore_cost,
                        robot.clay_cost,
                        robot.obsidian_cost
                    ] for robot in blueprint.robot_dict.values()
                ]
                for blueprint in output_ls
            ],
            [
                [
                    [
                        robot.type,
                        robot.ore_cost,
                        robot.clay_cost,
                        robot.obsidian_cost
                    ] for robot in blueprint.robot_dict.values()
                ]
                for blueprint in Day19.format_data(raw_input)
            ]
        )

class TestCanBuildRobots(unittest.TestCase):
    def test_can_build_robots_sufficient(self):
        """
        sufficient resources to build specified robot
        :return:
        """
        num_resources_dict = {
            "ore": 4,
            "clay": 0,
            "obsidian": 0,
            "geode": 0
        }
        blueprint_1 = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )
        curr_robot_type = "ore"

        updated_resources_dict = {
            "ore": 0,
            "clay": 0,
            "obsidian": 0,
            "geode": 0
        }
        self.assertEqual(
            (True, updated_resources_dict),
            Day19.can_build_robot(
                num_resources_dict,
                blueprint_1,
                curr_robot_type
            )
        )
    def test_can_build_robots_insufficient(self):
        """
        sufficient resources to build specified robot
        :return:
        """
        num_resources_dict = {
            "ore": 4,
            "clay": 13,
            "obsidian": 0,
            "geode": 0
        }
        blueprint_1 = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )
        curr_robot_type = "obsidian"

        self.assertEqual(
            (False, num_resources_dict),
            Day19.can_build_robot(
                num_resources_dict,
                blueprint_1,
                curr_robot_type
            )
        )
class TestUpdateBuildOrder(unittest.TestCase):
    def test_update_build_order_ore_add1(self):
        build_order_ls = ["ore"]
        num_robots_dict = {
            "ore": 1,
            "clay": 0,
            "obsidian": 0,
            "geode": 0
        }
        curr_robot_type = "ore"
        blueprint = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )
        self.assertEqual(
            (
                ["ore", "clay"],
                [
                    ["ore", "ore"],
                ]
            ),
            Day19.update_build_order(
                build_order_ls,
                num_robots_dict,
                curr_robot_type,
                blueprint,
                num_geodes=0,
                max_geodes=0,
                curr_time=1,
                num_minutes=24
            )
        )

    def test_update_build_order_ore_add3(self):
        build_order_ls = ["ore"]
        num_robots_dict = {
                              "ore": 1,
                              "clay": 1,
                              "obsidian": 1,
                              "geode": 0
                          }
        curr_robot_type = "ore"
        blueprint = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )
        self.assertEqual(
            (
                ["ore", "geode"],
                [
                    ["ore", "obsidian"],
                    ["ore", "clay"],
                    ["ore", "ore"],
                ]
            ),
            Day19.update_build_order(
                build_order_ls,
                num_robots_dict,
                curr_robot_type,
                blueprint,
                num_geodes=0,
                max_geodes=0,
                curr_time=1,
                num_minutes=24
            )
        )
    def test_update_build_order_ore_add3_curr_robot(self):
        build_order_ls = ["ore"]
        num_robots_dict = {
                              "ore": 1,
                              "clay": 1,
                              "obsidian": 0,
                              "geode": 0
                          }
        curr_robot_type = "obsidian"
        blueprint = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )
        self.assertEqual(
            (
                ["ore", "geode"],
                [
                    ["ore", "obsidian"],
                    ["ore", "clay"],
                    ["ore", "ore"]

                ]
            ),
            Day19.update_build_order(
                build_order_ls,
                num_robots_dict,
                curr_robot_type,
                blueprint,
                num_geodes=0,
                max_geodes=0,
                curr_time=1,
                num_minutes=24
            )
        )
class TestCalculateNumGeodes(unittest.TestCase):
    def test_calculate_num_geodes_defined_build_order(self):
        """
        given a known build list, does it return the correct number of geodes
        :return:
        """
        build_order_ls = [
            "clay",
            "clay",
            "clay",
            "obsidian",
            "clay",
            "obsidian",
            "geode",
            "geode",
        ]
        build_order_lists_ls = [build_order_ls,["ore"], ["ore", "clay"]]
        blueprint = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )
        num_minutes = 24

        self.assertEqual(
            9,
            Day19.calculate_num_geodes(
                build_order_ls,
                blueprint,
                num_minutes,
                build_order_lists_ls,
                max_geodes=0
            )
        )
    def test_calculate_num_geodes_edit_build_order_list_ls(self):
        """
        test mutation of build_order_list_ls
        :return:
        """

        build_order_lists_ls = [["ore"], ["clay"]]
        build_order_ls = build_order_lists_ls[0]
        blueprint = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )
        num_minutes = 24
        Day19.calculate_num_geodes(
            build_order_ls,
            blueprint,
            num_minutes,
            build_order_lists_ls,
            max_geodes=0
        )
        self.assertEqual(
            [
                ["ore"],
                ["clay"],
                ['ore', 'ore'],
                ['ore', 'clay', 'clay'],
                ['ore', 'clay', 'ore'],
                ['ore', 'clay', 'obsidian', 'obsidian'],
                ['ore', 'clay', 'obsidian', 'clay'],
                ['ore', 'clay', 'obsidian', 'ore'],
            ],
            build_order_lists_ls
        )

class TestDetermineMaxGeodes(unittest.TestCase):
    def test_determine_max_geodes_1(self):
        blueprint_1 = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=4
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=2
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=14,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=2,
                    obsidian_cost=7
                )
            }
        )
        self.assertEqual(
            9,
            Day19.determine_max_geodes(blueprint_1, 24)
        )
    def test_determine_max_geodes_2(self):
        blueprint_2 = Day19.RobotBlueprint(
            robot_dict={
                "ore": Day19.Robot(
                    type="ore",
                    ore_cost=2
                ),
                "clay": Day19.Robot(
                    type="clay",
                    ore_cost=3
                ),
                "obsidian": Day19.Robot(
                    type='obsidian',
                    ore_cost=3,
                    clay_cost=8,
                ),
                "geode": Day19.Robot(
                    type='geode',
                    ore_cost=3,
                    obsidian_cost=12
                )
            }
        )
        self.assertEqual(
            12,
            Day19.determine_max_geodes(blueprint_2, 24)
        )


class TestSumQualityLevels(unittest.TestCase):
    def test_sum_quality_levels(self):
        with open("Day19_test_input.txt", "r") as input_file:
            raw_input = input_file.read()
        self.assertEqual(
            33,
            Day19.sum_quality_levels(
                raw_input,
                24
            ))


if __name__ == '__main__':
    unittest.main()
