from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic Effect Robot Action Predicates
    pushed: bool
    folded: bool
    
    # Object physical properties predicates
    is_soft: bool
    is_elastic: bool
    is_rigid: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    in_box: bool
    is_fragile: bool


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
        if self.robot_handempty and not obj.in_box and obj.object_type != 'box':
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft and o.in_box for o in bin):
                print(f"Cannot Place {obj.name} in {bin.name} because no soft objects in the bin")
            elif obj.is_fragile and not any(o.is_elastic and o.in_box for o in bin):
                print(f"Cannot Place {obj.name} in {bin.name} because no elastic objects in the bin")
            else:
                obj.in_box = True
                self.state_handempty()
                print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and obj.in_box:
            if any(o.is_fragile and o.in_box for o in bin):
                print(f"Cannot Push {obj.name} because there is a fragile object in the bin")
            else:
                obj.pushed = True
                print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_soft:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        if obj.in_box and self.robot_handempty:
            obj.in_box = False
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Pick_Out {obj.name} from {bin.name}")

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
    is_soft=True, 
    is_elastic=False, 
    is_rigid=False, 
    in_box=False, 
    is_fragile=False
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    is_soft=False, 
    is_elastic=False, 
    is_rigid=True, 
    in_box=False, 
    is_fragile=False
)

object2 = Object(
    index=2, 
    name='blue_1D_ring', 
    color='blue', 
    shape='1D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    is_soft=False, 
    is_elastic=True, 
    is_rigid=False, 
    in_box=False, 
    is_fragile=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    is_soft=False, 
    is_elastic=False, 
    is_rigid=False, 
    in_box=True, 
    is_fragile=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid): in_box=True, pushed=True
    # object1 (black_3D_cylinder): in_box=True
    # object2 (blue_1D_ring): in_box=False
    # object3 (white_box): in_box=True (already in the box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # 1. Pick yellow_3D_cuboid (soft object) and place it in the box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Push yellow_3D_cuboid to make more space in the box
    robot.push(object0, bin)

    # 3. Pick black_3D_cylinder (rigid object) and place it in the box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object0.pushed == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    print("All task planning is done")
