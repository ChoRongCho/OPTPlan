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
    is_fragile: bool
    is_rigid: bool
    
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
        if self.robot_handempty and obj not in bin.in_bin:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft for o in bin.in_bin):
                print(f"Cannot Place {obj.name} in {bin.name} due to rule 2")
            elif obj.is_fragile and not any(o.is_elastic for o in bin.in_bin):
                print(f"Cannot Place {obj.name} in {bin.name} due to rule 3")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and not (obj.is_fragile or obj.is_rigid):
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin and self.robot_handempty:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
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
    is_rigid=False, 
    is_heavy=False, 
    is_large=False
)

object1 = Object(
    index=1, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=True, 
    is_elastic=False, 
    is_fragile=False, 
    is_rigid=False, 
    is_heavy=False, 
    is_large=False
)

object2 = Object(
    index=2, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=True, 
    is_rigid=True, 
    is_heavy=False, 
    is_large=False
)

object3 = Object(
    index=3, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=False, 
    is_rigid=True, 
    is_heavy=False, 
    is_large=False
)

object4 = Object(
    index=4, 
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
    is_rigid=False, 
    is_heavy=False, 
    is_large=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (white_3D_cylinder) -> in_box
    # object1 (brown_3D_cuboid) -> in_box
    # object2 (green_3D_cylinder) -> in_box
    # object3 (yellow_3D_cylinder) -> in_box
    # object4 (white_box) -> box (already in box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Place soft objects first
    robot.pick(object0, bin)
    robot.place(object0, bin)  # Place white_3D_cylinder (soft, elastic) in the box

    robot.pick(object1, bin)
    robot.place(object1, bin)  # Place brown_3D_cuboid (soft) in the box

    # 2. Place rigid objects
    robot.pick(object3, bin)
    robot.place(object3, bin)  # Place yellow_3D_cylinder (rigid) in the box

    # 3. Place fragile object (requires elastic object in the bin)
    robot.pick(object2, bin)
    robot.place(object2, bin)  # Place green_3D_cylinder (rigid, fragile) in the box

    # Fourth, check if the goal state is satisfying goal state table. These are examples.
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin
    assert object2 in bin.in_bin
    assert object3 in bin.in_bin
    assert object4 == bin  # The box itself is the bin

    print("All task planning is done")
