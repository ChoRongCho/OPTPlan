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
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            # Effects
            obj.is_in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.object_type != 'box' and obj.is_in_box and self.robot_handempty:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.object_type != 'box' and self.robot_handempty:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.object_type != 'box' and obj.is_in_box and self.robot_handempty:
            # Effects
            obj.is_in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False, is_fragile=False)
object1 = Object(index=1, name='black_3D_circle', color='black', shape='3D_circle', object_type='obj', is_rigid=True, is_in_box=False, is_fragile=False)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_rigid=False, is_in_box=True, is_fragile=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0: out_box
    # object1: out_box
    # object2: in_box

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object2  # white_box

    # Third, after making all actions, fill your reasons according to the rules
    # According to the rules:
    # 1. You should never pick and place a box.
    # 2. If there are objects in the box, pick out all objects from bin first, and do packing.

    # Since the goal state requires the objects to be out of the box, we need to ensure they are not in the box.
    # However, in the initial state, no objects are in the box except the box itself, which is already in the box.

    # No actions are needed as the initial state already satisfies the goal state.

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.is_in_box == False
    assert object1.is_in_box == False
    assert object2.is_in_box == True
    print("All task planning is done")
