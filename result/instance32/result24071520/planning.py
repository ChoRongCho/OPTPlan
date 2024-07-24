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
    is_elastic: bool
    is_fragile: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_heavy: bool
    is_large: bool


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
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        if obj.object_type != 'bin' and obj not in bin.in_bin and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.object_type != 'bin':
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_elastic and (not obj.is_fragile or obj in bin.in_bin):
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
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=True, is_elastic=False, is_fragile=True,
    is_heavy=False, is_large=False
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=True, is_elastic=False, is_fragile=False,
    is_heavy=False, is_large=False
)

object2 = Object(
    index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=True, is_fragile=False,
    is_heavy=False, is_large=False
)

object3 = Object(
    index=3, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=True, is_fragile=False,
    is_heavy=False, is_large=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='bin',
    pushed=False, folded=False, in_bin=[], is_rigid=False, is_elastic=False, is_fragile=False,
    is_heavy=False, is_large=False
)

# Initial state adjustments
object4.in_bin.append(object3)  # white_1D_ring is initially in the white_box

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # green_3D_cylinder: in white_box
    # yellow_3D_cylinder: out of any box
    # blue_1D_ring: in white_box
    # white_1D_ring: in white_box
    # white_box: contains green_3D_cylinder, blue_1D_ring, white_1D_ring

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # c) Action sequence to achieve the goal state
    # 1. Pick green_3D_cylinder and place it in white_box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Pick blue_1D_ring and place it in white_box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Don't pick and place a box called bin
    # - We never pick or place the white_box itself.
    # Rule 2: When fold an object, the object must be foldable
    # - We didn't fold any objects in this plan.
    # Rule 3: When fold a foldable object, the fragile object must be in the bin
    # - We didn't fold any objects in this plan.

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin  # green_3D_cylinder should be in white_box
    assert object1 not in bin.in_bin  # yellow_3D_cylinder should be out of any box
    assert object2 in bin.in_bin  # blue_1D_ring should be in white_box
    assert object3 in bin.in_bin  # white_1D_ring should be in white_box
    assert bin.in_bin == [object3, object0, object2]  # white_box should contain green_3D_cylinder, blue_1D_ring, white_1D_ring

    print("All task planning is done")