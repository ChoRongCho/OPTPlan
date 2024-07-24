from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic Effect Robot Action Predicates for object_type = obj
    pushed: bool
    folded: bool
    
    # Bin Predicates for object_type = bin
    in_bin: list
    
    # Object physical properties predicates
    is_rigid: bool
    is_foldable: bool
    is_elastic: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_fragile: bool
    is_heavy: bool


class Robot:
    def __init__(self, name: str = "UR5", goal: str = None, actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False

    def state_base(self):
        self.robot_base_pose = True

    def pick(self, obj, bin):
        if self.robot_handempty and obj not in bin.in_bin:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj in bin.in_bin:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")

    def pick_out(self, obj, bin):
        if obj in bin.in_bin:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. Each action has preconditions that must be met before the action can be executed, ensuring that the robot operates within the constraints of the bin_packing task. For example, the 'pick' action requires the robot's hand to be empty and the object not to be in the bin, while the 'fold' action requires the object to be foldable. These preconditions and effects ensure that the robot's actions are logical and adhere to the specified rules, such as not lifting containers and ensuring fragile objects are handled correctly.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=True, is_foldable=False, is_elastic=False,
    is_fragile=False, is_heavy=False
)

object1 = Object(
    index=1, name='beige_1D_ring', color='beige', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_foldable=False, is_elastic=True,
    is_fragile=False, is_heavy=False
)

object2 = Object(
    index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_foldable=False, is_elastic=True,
    is_fragile=False, is_heavy=False
)

object3 = Object(
    index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_foldable=True, is_elastic=False,
    is_fragile=False, is_heavy=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='bin',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_foldable=False, is_elastic=False,
    is_fragile=False, is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cylinder) in white_box
    # object1 (beige_1D_ring) in white_box
    # object2 (blue_1D_ring) in white_box
    # object3 (black_2D_circle) in white_box
    # object4 (white_box) remains as bin

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # Step-by-step action sequence to achieve the goal state

    # 1. Pick beige_1D_ring and place it in the white_box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 2. Pick blue_1D_ring and place it in the white_box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # 3. Pick yellow_3D_cylinder and place it in the white_box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 4. Pick out black_2D_circle from the white_box
    robot.pick_out(object3, bin)

    # 5. Fold black_2D_circle (since it is foldable)
    robot.fold(object3, bin)

    # 6. Place black_2D_circle back in the white_box
    robot.place(object3, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 in bin.in_bin
    assert object3 in bin.in_bin
    assert object4.name == 'white_box'
    print("All task planning is done")
