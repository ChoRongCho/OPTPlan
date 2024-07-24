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
    is_fragile: bool
    is_rigid: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
    is_out_box: bool


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
        if obj.object_type != 'bin' and obj.is_out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = True
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if obj.object_type != 'bin' and self.robot_now_holding == obj:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin.append(obj)
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and not obj.is_fragile and not obj.is_rigid:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_soft:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj in bin.in_bin and self.robot_handempty:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
        else:
            print(f"Cannot Pick_Out {obj.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=True, 
    is_fragile=False, 
    is_rigid=False, 
    is_in_box=False, 
    is_out_box=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_fragile=True, 
    is_rigid=True, 
    is_in_box=False, 
    is_out_box=True
)

object2 = Object(
    index=2, 
    name='brown_3D_cuboid', 
    color='brown', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=True, 
    is_fragile=False, 
    is_rigid=False, 
    is_in_box=True, 
    is_out_box=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='bin', 
    pushed=False, 
    folded=False, 
    in_bin=[], 
    is_soft=False, 
    is_fragile=False, 
    is_rigid=False, 
    is_in_box=False, 
    is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (red_3D_polyhedron) -> in white_box
    # object1 (green_3D_cylinder) -> in white_box
    # object2 (brown_3D_cuboid) -> in white_box
    # object3 (white_box) -> contains [object0, object1, object2]

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Don't pick and place a box called bin
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before
    # Rule 3: When folding an object, the object must be foldable
    # Rule 4: When pushing an object, neither fragile nor rigid objects are permitted, but only soft objects are permitted

    # Action sequence:
    # 1. Pick and place the red_3D_polyhedron (soft object)
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Pick and place the brown_3D_cuboid (soft object)
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # 3. Pick and place the green_3D_cylinder (rigid object, after soft objects are in the bin)
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.in_bin == [object0, object1, object2]
    print("All task planning is done")
