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
    is_fragile: bool = False
    is_foldable: bool = False
    is_rigid: bool = False
    is_soft: bool = False

    # bin_packing Predicates (max 1)
    in_bin: bool = False


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

        # new state for bin_packing
        self.is_soft_in_bin = False
        self.is_fragile_in_bin = False

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
            obj.in_bin = False

    # bin_packing
    def place(self, obj, bins):
        if self.robot_now_holding != obj or obj.object_type == 'box':
            print(f"Cannot place a {obj.name} not in hand or a box.")
        elif bins:
            # place an object in the bin
            if obj.is_rigid and self.is_soft_in_bin:
                print(f"Cannot place a {obj.name} without the soft object in the box. ")
            elif obj.is_soft:
                self.is_soft_in_bin = True
                print(f"Place soft {obj.name} in {bins.name}")
                self.state_handempty()
                obj.in_bin = True
            elif obj.is_fragile:
                self.is_fragile_in_bin = True
                print(f"Place fragile {obj.name} in {bins.name}")
                self.state_handempty()
                obj.in_bin = True
            else:
                print(f"Place {obj.name} in {bins.name}")
                self.state_handempty()
                obj.in_bin = False
        else:
            # place an object out of the bin
            if obj.is_soft:
                self.is_soft_in_bin = False
            print(f"Place {obj.name} out of the box")
            self.state_handempty()
            obj.in_bin = False

    # bin_packing
    def push(self, obj):
        if not self.robot_handempty or obj.is_fragile or obj.is_rigid:
            print(
                f"Cannot push a {obj.name} when hand is not empty or the object is fragile or rigid or there is a fragile object on it.")
        elif obj.is_soft and obj.in_bin:
            if self.is_fragile_in_bin:
                print(f"Cannot push a {obj.name} when a fragile object in the bin")
            else:
                print(f"Push {obj.name}")
        else:
            print(f"Push {obj.name}")

    # bin_packing
    def fold(self, obj):
        if not self.robot_handempty or not obj.is_foldable:
            print(f"Cannot fold a {obj.name} when hand is not empty or the object is not foldable.")
        else:
            if not self.is_fragile_in_bin:
                print(f"Cannot fold a {obj.name} without the fragile object in the box. ")
            else:
                print(f"Fold {obj.name}")

    # bin_packing
    def out(self, obj, bins):
        if not obj.in_bin:
            print(f"Cannot pick a {obj.name} not in the bin.")
        else:
            print(f"Out {obj.name} from {bins.name}")
            self.state_holding(obj)
            obj.in_bin = False


# Object 1
object1 = Object(
    index=0,
    name='yellow sponge',
    location=(89, 136),
    size=(156, 154),
    color='yellow',
    object_type='object',
    is_rigid=True,
    in_bin=True
)

# Object 2
object2 = Object(
    index=1,
    name='blue paper towel',
    location=(203, 278),
    size=(156, 150),
    color='blue',
    object_type='object',
    is_foldable=True,
    is_soft=True,
)

# Bin
bin1 = Object(
    index=2,
    name='white box',
    location=(498, 218),
    size=(249, 353),
    color='white',
    object_type='bin',
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
    object_type='object',
    is_soft=True,
)

object4 = Object(
    index=4,
    name='black strips',
    location=(294, 150),
    size=(147, 123),
    color='black',
    object_type='object',
    is_fragile=True,
)

# if __name__ == '__main__':
# 	# packing all object in the box
# 	# make a plan
#
# You must follow the rule:
#
# {'pick': 'pick an {object} not in the {bin}', 'place': 'place an {object} on the {anywhere}', 'push': 'push an {object} downward in the bin, hand must be empty when pushing', 'fold': 'fold an {object}, hand must be empty when folding. you can fold the object in_bin or out_bin', 'out': 'pick an {object} in {bin}'}
# rule0: "don't pick and place a box called bin"
# rule1: "when place a rigid objects, the soft objects must be in the bin",
# rule2: "when fold a object, the fragile object must be in the bin ",
# rule3: "when a rigid object in the bin at the initial state, out the rigid object and replace it into the bin ",
# rule4: "you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object in the bin "
# Make a plan under the if __name__ == '__main__': and reflect the rules that are not considered at the robot action part.
# You must make a correct order.

# ------------------------------------------------------

if __name__ == '__main__':
    """
    bin
    rigid and foldable but we don't have to consider this predicates.
    rule0: "don't pick and place a box called bin"
    rule1: "when place a rigid objects, the soft objects must be in the bin",
    rule2: "when fold a object, the fragile object must be in the bin ",
    rule3: "when a rigid object in the bin at the initial state, out the rigid object and replace it into the bin ",
    rule4: "you must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object in the bin "
    objects
    1 foldable objects: object2
    1 fragile object: object4
    1 rigid object: object1
    2 soft object: object2, object3

    objects in the bin: object1
    objects out the bin: object2, object3, object4

    Available action
    object1: [rigid, in_bin]: out, place
    object2: [soft, foldable, out_bin]: pick, place, push, fold
    object3: [soft, out_bin]: pick, place, push
    object4: [fragile, out_bin]: pick, place

    """
    # Initialize robot
    robot = Robot()

    # Out and place a rigid object based on rule3
    robot.out(object1, bin1)
    robot.place(object1, False)
    robot.pick(object1)
    robot.place(object1, bin1)

    # Pick and place fragile object4 in the bin before fold the foldable object
    robot.pick(object4)
    robot.place(object4, bin1)

    # Fold, Push, Pick and place object2 in the bin based on the rule4
    robot.fold(object2)
    robot.push(object2)
    robot.pick(object2)
    robot.place(object2, bin1)

    # Push, Pick and place object3
    robot.push(object3)
    robot.pick(object3)
    robot.place(object3, bin1)

    # End the planning
    robot.state_base()
