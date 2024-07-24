from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: list
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    is_rigid: bool
    is_fragile: bool
    is_elastic: bool
    in_box: bool


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
        # Preconditions
        if obj.object_type == 'box':
            print(f"Cannot pick {obj.name} because it is a bin.")
            return
        if obj.in_box:
            print(f"Cannot pick {obj.name} because it is already in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot pick {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        self.state_holding(obj)
        print(f"Picked {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_handempty:
            print(f"Cannot place {obj.name} because the robot hand is empty.")
            return
        if obj.object_type == 'box':
            print(f"Cannot place {obj.name} because it is a bin.")
            return
        
        # Effects
        self.state_handempty()
        obj.in_box = True
        if bin.in_bin_objects is None:
            bin.in_bin_objects = []
        bin.in_bin_objects.append(obj)
        print(f"Placed {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot push {obj.name} because the robot hand is not empty.")
            return
        if not obj.in_box:
            print(f"Cannot push {obj.name} because it is not in the bin.")
            return
        
        # Effects
        obj.pushed = True
        print(f"Pushed {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot fold {obj.name} because the robot hand is not empty.")
            return
        if not obj.is_elastic:
            print(f"Cannot fold {obj.name} because it is not foldable.")
            return
        if obj.is_fragile and not obj.in_box:
            print(f"Cannot fold {obj.name} because it is fragile and not in the bin.")
            return
        
        # Effects
        obj.folded = True
        print(f"Folded {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if not obj.in_box:
            print(f"Cannot take out {obj.name} because it is not in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot take out {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        self.state_holding(obj)
        obj.in_box = False
        bin.in_bin_objects.remove(obj)
        self.state_handempty()
        print(f"Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=True, 
    is_fragile=True, 
    is_elastic=False, 
    in_box=False
)

object1 = Object(
    index=1, 
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=True, 
    is_fragile=False, 
    is_elastic=False, 
    in_box=False
)

object2 = Object(
    index=2, 
    name='blue_1D_linear', 
    color='blue', 
    shape='1D_linear', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=True, 
    is_fragile=False, 
    is_elastic=False, 
    in_box=False
)

object3 = Object(
    index=3, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=None, 
    is_rigid=False, 
    is_fragile=False, 
    is_elastic=True, 
    in_box=True
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[object3], 
    is_rigid=False, 
    is_fragile=False, 
    is_elastic=False, 
    in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "green_3D_cylinder": {"in_box": False},
        "yellow_3D_cylinder": {"in_box": False},
        "blue_1D_linear": {"in_box": False},
        "white_2D_ring": {"in_box": True},
        "white_box": {"in_bin_objects": [object3]}
    }

    # Goal state
    goal_state = {
        "green_3D_cylinder": {"in_box": True},
        "yellow_3D_cylinder": {"in_box": False},
        "blue_1D_linear": {"in_box": True},
        "white_2D_ring": {"in_box": True},
        "white_box": {"in_bin_objects": [object0, object2, object3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick green_3D_cylinder and place it in white_box
    # 2. Pick blue_1D_linear and place it in white_box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    robot.pick(object0, box)  # Pick green_3D_cylinder
    robot.place(object0, box)  # Place green_3D_cylinder in white_box

    robot.pick(object2, box)  # Pick blue_1D_linear
    robot.place(object2, box)  # Place blue_1D_linear in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. green_3D_cylinder is not in the box initially and is not a box, so it can be picked and placed.
    # 2. blue_1D_linear is not in the box initially and is not a box, so it can be picked and placed.
    # 3. white_2D_ring is already in the box and is foldable, but no folding action is required as per the goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object3, object0, object2]
    print("All task planning is done")
