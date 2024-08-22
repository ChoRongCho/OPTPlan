import os

from scripts.robot.robot import Robot
from scripts.utils.utils import list_file, sort_files


class RobotProve(Robot):
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None,
                 gpt_interface: object = False):
        super().__init__(name, goal, actions)

        self.predicates = self.active_predicates_list
        self.gpt_interface = gpt_interface
        self.object_list = [
            "obj1",
            "obj2",
            "obj3",
            "obj4",
            "obj5",
            "obj6",
            "obj7",
        ]
        self.replace_color_yellow = ["orange", "brown"]
        self.replace_color_white = ["beige"]
        self.replace_color_blue = ["gray"]
        self.replace_shape = ["3D_circle", "2D_flat_rectangle"]

        self.data_path = "/home/changmin/PycharmProjects/OPTPlan/data/bin_packing/predicates_prove"

    def get_object_predicates(self, database: dict, info: dict) -> list:
        target_name: str = info['name']
        name_list = list(database.keys())

        """# replace a color of the objects
        for color in self.replace_color_yellow:
            if color in target_name:
                print(f"Replace {target_name} color {color} into yellow")
                target_name = target_name.replace(color, "yellow")
                break

        for color in self.replace_color_white:
            if color in target_name:
                print(f"Replace {target_name} color {color} into white")
                target_name = target_name.replace(color, "white")
                break

        for color in self.replace_color_blue:
            if color in target_name:
                print(f"Replace {target_name} color {color} into blue")
                target_name = target_name.replace(color, "blue")
                break

        for shape in self.replace_shape:
            if shape in target_name and shape == self.replace_shape[0]:
                print(f"Replace {target_name} shape {shape} into 3D_cylinder")
                target_name = target_name.replace(shape, "3D_cylinder")

                break
            elif shape in target_name and shape == self.replace_shape[1]:
                print(f"Replace {target_name} shape {shape} into 2D_rectangle")
                target_name = target_name.replace(shape, "2D_rectangle")
                break"""

        if target_name in name_list:
            predicates = database[target_name]["properties"]
            return predicates
        else:
            # random mode
            predicates = self.random_active_search(info)
            print(f"Can't find {target_name} in database. Random predicates are assigned. ")
            return predicates

    def gpt_prove_object(self, info, images):
        name = list(info.keys())[0]
        root = os.path.join(self.data_path, name)
        obj_data_path = list_file(root)
        obj_data_path = sort_files(obj_data_path)

        is_push, is_fold, is_pull = False, False, False
        for data_name in obj_data_path:
            if "push" in data_name:
                is_push = True
                continue
            if "fold" in data_name:
                is_fold = True
                continue
            if "pull" in data_name:
                is_pull = True
                continue

    def get_datapath(self, name):
        pass

    def identifying_properties(self, images: list or False = False):
        if not images:
            # self.database_path 내의 모든 이미지를 data로 불러오기
            pass
        skills = self.database.skill_predicates_pair.keys()
        # push
        push_image = []
        for image in images:
            if skills[0] in image:
                push_image.append(image)

        # fold
        fold_image = []
        for image in images:
            if skills[1] in image:
                fold_image.append(image)

        # pull
        pull_image = []
        for image in images:
            if skills[2] in image:
                pull_image.append(image)

        return push_image, fold_image, pull_image
