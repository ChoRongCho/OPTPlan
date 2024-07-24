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
    fits_in_box: bool


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
            obj.in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and obj.in_box:
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
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, is_soft=True, is_elastic=False, is_rigid=False, in_box=False, fits_in_box=False)
object1 = Object(index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, is_soft=False, is_elastic=False, is_rigid=True, in_box=False, fits_in_box=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', pushed=False, folded=False, is_soft=False, is_elastic=True, is_rigid=False, in_box=False, fits_in_box=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, is_soft=False, is_elastic=False, is_rigid=False, in_box=True, fits_in_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) -> in_box: True, fits_in_box: True
    # object1 (black_3D_cylinder) -> in_box: True, fits_in_box: True
    # object2 (blue_1D_ring) -> in_box: False, fits_in_box: False
    # object3 (white_box) -> in_box: True, fits_in_box: False (already in box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Never attempt to pick up and set down an object named box
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before
    # Rule 3: Do not place a fragile object if there is no elastic object in the bin
    # Rule 4: You must push a soft object to make more space in the bin, however, if there is a fragile object on the soft object, you must not push the object

    # Action sequence:
    # 1. Pick yellow_3D_cuboid (soft object)
    robot.pick(object0, bin)
    # 2. Place yellow_3D_cuboid in the bin
    robot.place(object0, bin)
    # 3. Push yellow_3D_cuboid to make more space
    robot.push(object0, bin)
    # 4. Pick black_3D_cylinder (rigid object)
    robot.pick(object1, bin)
    # 5. Place black_3D_cylinder in the bin
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    print("All task planning is done")
