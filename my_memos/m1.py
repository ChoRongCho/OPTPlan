from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    location: tuple
    size: tuple
    color: str or bool
    object_type: str

    # Object physical properties predicates
    is_rigid: bool = False
    is_foldable: bool = False
    is_elastic: bool = False
    is_soft: bool = False

    # bin_packing Predicates (max 4)
    in_bin: bool = False
    out_bin: bool = False
    is_folded: bool = False
    on_the_object: object or bool = False


class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions

        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True
        self.is_soft_object_in_bin = False

    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False

    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False

    # basic state
    def state_base(self):
        self.robot_base_pose = True

    # bin_packing
    def pick(self, obj):
        if obj.in_bin or obj.object_type == 'box':
            print(f"Cannot pick a {obj.name} in the bin or a box.")
        else:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_bin = True
            obj.in_bin = False

    # bin_packing
    def place(self, obj, bins):
        if self.robot_now_holding != obj or obj.object_type == 'box':
            print(f"Cannot place a {obj.name} not in hand or a box.")
        elif obj.is_rigid and not self.is_soft_object_in_bin:
            print(f"Cannot place a fragile {obj.name} when there is no soft object in the bin.")
        elif bins:
            print(f"Place {obj.name} in {bins.name}")
            self.state_handempty()
            obj.in_bin = True
            obj.out_bin = False
            if obj.is_soft:
                self.is_soft_object_in_bin = True
        else:
            print(f"Place {obj.name} out of the box")
            self.state_handempty()
            obj.in_bin = False
            obj.out_bin = True

    # bin_packing
    def push(self, obj):
        if not self.robot_handempty:
            print(f"Cannot push a {obj.name} when hand is not empty.")
        elif obj.is_rigid or obj.on_the_object:
            print(f"Cannot push a fragile or rigid {obj.name} or when there is an object on it.")
        else:
            print(f"Push {obj.name}")

    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty:
            print(f"Cannot fold a {obj.name} when hand is not empty.")
        elif not obj.is_foldable:
            print(f"Cannot fold a non-foldable {obj.name}.")
        else:
            print(f"Fold {obj.name}")
            obj.is_folded = True

    def out(self, obj, bins):
        if not obj.in_bin:
            print(f"Cannot pick a {obj.name} not in the bin.")
        else:
            print(f"Out {obj.name} from {bins.name}")
            self.state_holding(obj)
            obj.in_bin = False
            obj.out_bin = True

# Object 1
object1 = Object(
    index=0,
    name='yellow sponge',
    location=(89, 136),
    size=(156, 154),
    color='yellow',
    object_type='sponge',
    is_rigid=True,
    out_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='blue paper towel',
    location=(203, 278),
    size=(156, 150),
    color='blue',
    object_type='paper towel',
    is_elastic=True,
    is_soft=True,
    out_bin=True
)

# Bin
bin1 = Object(
    index=2,
    name='white box',
    location=(498, 218),
    size=(249, 353),
    color='white',
    object_type='box',
    is_rigid=True,
    is_foldable=True,
    in_bin=True
)

# Object 3
object3 = Object(
    index=3,
    name='black strips',
    location=(294, 150),
    size=(147, 123),
    color='black',
    object_type='strips',
    is_elastic=True,
    out_bin=True
)
"""
if __name__ == '__main__':
    # make a plan in right order here

You must follow the rule:

{'pick': 'pick an {object} not in the {bin}', 'place': 'place an {object} on the {anywhere}', 'push': 'push an {object} downward in the bin, hand must be empty when pushing', 'fold': 'fold an {object}, hand must be empty when folding. you can fold the object in_bin or out_bin', 'out': 'pick an {object} in {bin}'}
{'rule0': 'you should never pick and place a box', 'rule1': 'when place a fragile objects, the soft objects must be in the bin', 'rule2': 'when fold a object, the object must be flexible', 'rule3': 'when push a object, neither fragile and rigid objects are permitted, but only soft objects are permitted', 'rule4': 'you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object'}
Make a plan under the if __name__ == '__main__':.
You must make a correct order.

|-------------------------------------Init-State-----------------------------------|
| item    | name             | in_bin | out_bin | is_soft |  is_rigid | is_elastic |
|----------------------------------------------------------------------------------|
| object1 | yellow sponge    | False  | True    | False   |  True     | False      |
| object2 | blue paper towel | False  | True    | True    |  False    | True       |
| bin1    | white box        | None   | None    | None    |  None     | None       |
| object3 | black strips     | False  | True    | False   |  False    | True       |
|----------------------------------------------------------------------------------|

|------------------------Goal-State------------------------|
| item    | name          | in_bin | out_bin | soft_pushed |
|----------------------------------------------------------|
| object0 | yellow object | True   | False   | False       |
| bin1    | white box     | None   | None    | None        |
| object2 | black object  | False  | True    | True        |
| object3 | blue object   | True   | False   | False       |
|----------------------------------------------------------|
"""

# --------------------------------------

if __name__ == '__main__':
    """
    bin 
    rigid and foldable but we don't have to consider this predicates.

    objects
    2 elastic object: object2, object3
    1 rigid object: object1 
    1 soft object: object2
    
    objects in the bin: 
    objects out the bin: object1, object2, object3
    
    Available action
    object1: [rigid, out_bin]: pick, place
    object2: [soft, elastic, out_bin]: pick, place, push
    object3: [elastic, out_bin]: pick, place
    """
    # Initialize robot
    robot = Robot()

    # Pick and place object2 in the bin
    robot.pick(object2)
    robot.place(object2, bin1)
    robot.push(object2)

    # Pick and place object1 in the bin
    robot.pick(object1)
    robot.place(object1, bin1)

    # Pick and place object3
    robot.pick(object3)
    robot.place(object3, bin1)

    # End the planning
    robot.state_base()
