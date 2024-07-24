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
    is_soft: bool
    is_rigid: bool
    is_elastic: bool
    is_fragile: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_heavy: bool
    is_large: bool


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
        if self.robot_handempty and obj.object_type != 'box' and obj not in bin.in_bin:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft for o in bin.in_bin):
                print(f"Cannot Place {obj.name} in {bin.name} because no soft object in bin")
            else:
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
        if self.robot_handempty and obj not in bin.in_bin and obj.is_elastic:
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
# The robot actions are designed to follow the given rules strictly. The preconditions ensure that actions are only performed when the robot's state and the object's state meet the specified criteria. For example, the robot cannot pick up an object if it is already holding something or if the object is a box. The place action checks for the presence of a soft object in the bin before placing a rigid object, adhering to the rules. The push and fold actions require the robot's hand to be empty, ensuring that the robot is not holding anything while performing these actions. The pick_out action ensures that the object is in the bin before attempting to pick it out. These conditions and effects ensure that the robot's actions are consistent with the rules and the state of the objects and the bin.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_rigid=True, 
    is_elastic=False, 
    is_fragile=True, 
    is_heavy=False, 
    is_large=False
)

object1 = Object(
    index=1, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=True, 
    is_rigid=False, 
    is_elastic=True, 
    is_fragile=False, 
    is_heavy=False, 
    is_large=False
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
    is_soft=False, 
    is_rigid=False, 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False, 
    is_large=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (green_3D_cylinder) -> in_box
    # object1 (white_3D_cylinder) -> in_box
    # object2 (white_box) -> box (unchanged)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object2

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Never attempt to pick up and set down an object named box
    # Rule 2: When placing a rigid object in the bin, the soft object must be in the bin before
    # Rule 3: If there is a foldable object, fold the object not in the bin but on the platform
    # Rule 4: When a rigid object is in the bin at the initial state, take out the rigid object and replace it into the bin
    # Rule 5: If there are soft objects, pick, place, and push them into the bin

    # Step 1: Fold the white_3D_cylinder (soft and elastic)
    robot.fold(object1, bin)

    # Step 2: Pick and place the white_3D_cylinder (soft) into the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Step 3: Pick and place the green_3D_cylinder (rigid) into the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # Step 4: Push the white_3D_cylinder (soft) into the bin
    robot.push(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 not in bin.in_bin
    print("All task planning is done")
