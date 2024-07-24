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
    is_elastic: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_fragile: bool
    is_heavy: bool


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
        # Preconditions
        if obj.object_type == "box" or obj in bin.in_bin:
            print(f"Cannot Pick {obj.name}")
            return
        # Effects
        self.state_holding(obj)
        print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_handempty or obj.object_type == "box":
            print(f"Cannot Place {obj.name}")
            return
        if obj.is_fragile and not any(o.is_elastic for o in bin.in_bin):
            print(f"Cannot Place {obj.name} because it is fragile and no elastic object in bin")
            return
        # Effects
        self.state_handempty()
        bin.in_bin.append(obj)
        print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty or obj.object_type == "box":
            print(f"Cannot Push {obj.name}")
            return
        # Effects
        obj.pushed = True
        print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty or obj.object_type == "box":
            print(f"Cannot Fold {obj.name}")
            return
        # Effects
        obj.folded = True
        print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj not in bin.in_bin:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")
            return
        # Effects
        self.state_holding(obj)
        bin.in_bin.remove(obj)
        print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=True, 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False
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
    is_elastic=True, 
    is_fragile=False, 
    is_heavy=False
)

object2 = Object(
    index=2, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=True, 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=False, 
    is_heavy=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # object0 and object2 should be in the box (object3)
    # object1 should remain out of the box
    # object3 is the box itself and should remain as is

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Never attempt to pick up and set down an object named box
    # Rule 2: Do not place a fragile object if there is no elastic object in the bin
    # Rule 3: When a rigid object in the bin at the initial state, out of the rigid object and replace it into the bin

    # Action sequence to achieve the goal state
    robot.pick(object0, bin)  # Pick yellow_3D_cuboid
    robot.place(object0, bin)  # Place yellow_3D_cuboid in white_box

    robot.pick(object2, bin)  # Pick yellow_3D_cuboid
    robot.place(object2, bin)  # Place yellow_3D_cuboid in white_box

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin
    assert object1 not in bin.in_bin
    assert object2 in bin.in_bin
    assert object3.in_bin == []
    print("All task planning is done")