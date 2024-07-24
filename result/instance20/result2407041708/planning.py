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
    is_soft: bool
    is_elastic: bool

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool
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
        # Preconditions
        if obj.object_type != 'box' and not obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and (bin.object_type == 'box' or not bin.is_in_box):
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_soft:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


# Define objects
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=False, is_in_box=False, is_fragile=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, is_in_box=False, is_fragile=False)
object2 = Object(index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=False, is_in_box=False, is_fragile=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_soft=False, is_elastic=False, is_in_box=True, is_fragile=False)

# Define robot
robot = Robot()

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) -> in_box
    # object1 (white_3D_cylinder) -> out_box
    # object2 (yellow_3D_cuboid) -> in_box
    # object3 (white_box) -> in_box (already in box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Never attempt to pick up and set down an object named box
    # Rule 2: Do not place a fragile object if there is no elastic object in the bin
    # Rule 3: When a rigid object in the bin at the initial state, out of the rigid object and replace it into the bin

    # Action sequence:
    # 1. Pick out the white_box (object3) and place it back to satisfy Rule 3
    robot.pick_out(object3, bin)
    robot.place(object3, bin)

    # 2. Pick yellow_3D_cuboid (object0) and place it in the box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 3. Pick yellow_3D_cuboid (object2) and place it in the box
    robot.pick(object2, bin)
    robot.place(object2, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.is_in_box == True
    assert object1.is_in_box == False
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    print("All task planning is done")
