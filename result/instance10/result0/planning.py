from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # Object physical properties predicates
    is_rigid: bool
    is_soft: bool
    is_elastic: bool
    is_fragile: bool

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
        # Preconditions
        if self.robot_handempty and obj.is_out_box and obj.object_type != 'box':
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_soft and obj.is_in_box:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(
    index=0, 
    name='white_3D_cylinder', 
    color='white', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=False, 
    is_soft=True, 
    is_elastic=True, 
    is_fragile=False, 
    is_in_box=False, 
    is_out_box=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=True, 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=True, 
    is_in_box=False, 
    is_out_box=True
)

object2 = Object(
    index=2, 
    name='transparent_3D_cylinder', 
    color='transparent', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=False, 
    is_soft=False, 
    is_elastic=True, 
    is_fragile=False, 
    is_in_box=False, 
    is_out_box=True
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    is_rigid=False, 
    is_soft=False, 
    is_elastic=False, 
    is_fragile=False, 
    is_in_box=True, 
    is_out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (white_3D_cylinder): is_out_box = True, is_in_box = False
    # object1 (green_3D_cylinder): is_out_box = False, is_in_box = True
    # object2 (transparent_3D_cylinder): is_out_box = False, is_in_box = True
    # object3 (white_box): is_out_box = False, is_in_box = True

    # Initialize the robot
    robot = Robot()

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Plan:
    # 1. Pick green_3D_cylinder
    robot.pick(object1, object3)
    # 2. Place green_3D_cylinder in white_box
    robot.place(object1, object3)
    # 3. Pick transparent_3D_cylinder
    robot.pick(object2, object3)
    # 4. Place transparent_3D_cylinder in white_box
    robot.place(object2, object3)

    # after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - We never pick and place a box (Rule 1).
    # - We did not fold any object, so Rule 2 does not apply.
    # - The fragile object (green_3D_cylinder) is placed in the box without folding any other object.

    # check if the goal state is satisfying goal state table
    assert object0.is_out_box == True and object0.is_in_box == False
    assert object1.is_out_box == False and object1.is_in_box == True
    assert object2.is_out_box == False and object2.is_in_box == True
    assert object3.is_out_box == False and object3.is_in_box == True

    print("All objects are in their goal states.")
