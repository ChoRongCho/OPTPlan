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
    is_foldable: bool
    is_elastic: bool
    is_soft: bool
    
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
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_soft and not any(o.is_elastic for o in bin.in_bin):
                print(f"Cannot Place {obj.name} because no elastic object in bin")
                return
            if not obj.is_soft and not any(o.is_soft for o in bin.in_bin):
                print(f"Cannot Place {obj.name} because no soft object in bin")
                return
            bin.in_bin.append(obj)
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj in bin.in_bin:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_foldable:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")

    def pick_out(self, obj, bin):
        if obj in bin.in_bin:
            bin.in_bin.remove(obj)
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules and constraints for bin packing. 
# Preconditions ensure that actions are only performed when the robot is in the correct state and the objects meet the necessary conditions.
# Effects update the state of the robot and objects to reflect the outcome of the actions.
# This approach ensures that the robot operates within the defined rules, such as avoiding handling boxes, ensuring elastic objects are in the bin before placing soft objects, and managing the order of placing rigid objects.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=True, 
    is_fragile=False, 
    is_heavy=False
)

object1 = Object(
    index=1, 
    name='black_2D_circle', 
    color='black', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=True, 
    is_elastic=True, 
    is_soft=False, 
    is_fragile=False, 
    is_heavy=False
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_foldable=False, 
    is_elastic=False, 
    is_soft=False, 
    is_fragile=False, 
    is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # object0 (brown_3D_cuboid) should be in the box
    # object1 (black_2D_circle) should be out of the box
    # object2 (white_box) should remain as it is (box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object2

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Pick out the black_2D_circle (object1) from the box
    robot.pick_out(object1, bin)
    
    # 2. Place the black_2D_circle (object1) outside the box
    robot.state_handempty()  # Robot is now hand empty after placing object1 outside the box

    # 3. Pick the black_2D_circle (object1) and fold it
    robot.pick(object1, bin)
    robot.fold(object1, bin)
    robot.state_handempty()  # Robot is now hand empty after folding object1

    # 4. Pick the brown_3D_cuboid (object0)
    robot.pick(object0, bin)

    # 5. Place the brown_3D_cuboid (object0) in the box
    robot.place(object0, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0 in bin.in_bin  # object0 should be in the box
    assert object1 not in bin.in_bin  # object1 should be out of the box
    assert object2.in_bin == []  # object2 should remain as it is (box)
    print("All task planning is done")
