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
    is_elastic: bool
    is_soft: bool

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
        if self.robot_handempty and not obj.is_in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
    
    def place(self, obj, bin):
        # Preconditions
        if not self.robot_handempty and self.robot_now_holding == obj:
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
        if self.robot_handempty and obj.is_elastic:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='beige_1D_ring', color='beige', shape='1D_ring', object_type='obj', is_elastic=True, is_soft=False, is_in_box=False, is_fragile=False)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, is_soft=False, is_in_box=False, is_fragile=False)
object2 = Object(index=2, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_elastic=True, is_soft=True, is_in_box=True, is_fragile=False)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', is_elastic=False, is_soft=False, is_in_box=False, is_fragile=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (beige_1D_ring) -> in_box
    # object1 (transparent_3D_cylinder) -> in_box
    # object2 (white_3D_cylinder) -> in_box (already in box)
    # object3 (white_box) -> remains as is (not in box)

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object3

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: It is prohibited to lift and relocate a container
    # Rule 2: When placing a rigid object in the bin, the soft objects must be in the bin before
    # Rule 3: When placing a fragile object, the soft objects must be in the bin

    # Action sequence:
    # 1. Pick beige_1D_ring and place it in the box
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 2. Pick transparent_3D_cylinder and place it in the box
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True  # Already in the box
    assert object3.is_in_box == False  # The box itself should not be in another box

    print("All task planning is done")
