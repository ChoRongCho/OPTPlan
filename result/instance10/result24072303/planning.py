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
    in_box: bool
    is_heavy: bool
    
    # Object physical properties 
    is_soft: bool
    is_foldable: bool
    is_elastic: bool
    is_fragile: bool
    is_rigid: bool


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
        # Preconditions: Robot hand must be empty, object must not be in the bin, object must not be a box
        if self.robot_handempty and not obj.in_box and obj.object_type != 'box':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions: Robot must be holding the object, object must not be a box
        if self.robot_now_holding == obj and obj.object_type != 'box':
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions: Robot hand must be empty, object must be in the bin
        if self.robot_handempty and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions: Robot hand must be empty, object must be foldable, fragile object must be in the bin
        if self.robot_handempty and obj.is_foldable and any(o.is_fragile for o in bin.in_bin_objects):
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions: Object must be in the bin
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

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
    in_bin_objects=[], 
    in_box=False, 
    is_heavy=False, 
    is_soft=True, 
    is_foldable=False, 
    is_elastic=True, 
    is_fragile=False, 
    is_rigid=False
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_heavy=False, 
    is_soft=False, 
    is_foldable=False, 
    is_elastic=False, 
    is_fragile=True, 
    is_rigid=True
)

object2 = Object(
    index=2, 
    name='transparent_3D_cuboid', 
    color='transparent', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_heavy=False, 
    is_soft=True, 
    is_foldable=True, 
    is_elastic=False, 
    is_fragile=False, 
    is_rigid=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    is_heavy=False, 
    is_soft=False, 
    is_foldable=False, 
    is_elastic=False, 
    is_fragile=False, 
    is_rigid=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": object0,
        "object1": object1,
        "object2": object2,
        "object3": object3
    }

    # Goal state
    goal_state = {
        "object0": {"in_box": False},
        "object1": {"in_box": True},
        "object2": {"in_box": True},
        "object3": {"in_box": True, "in_bin_objects": [object1, object2]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: You should never pick and place a box
    # Rule 2: When fold a foldable object, the fragile object must be in the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'.
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence to achieve the goal state
    # Pick and place green_3D_cylinder into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Pick and place transparent_3D_cuboid into the box
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fold transparent_3D_cuboid since green_3D_cylinder (a fragile object) is in the bin
    robot.fold(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for each action:
    # 1. Pick and place green_3D_cylinder into the box because it needs to be in the box as per the goal state.
    # 2. Pick and place transparent_3D_cuboid into the box because it needs to be in the box as per the goal state.
    # 3. Fold transparent_3D_cuboid because it is foldable and there is a fragile object (green_3D_cylinder) in the bin.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == goal_state["object0"]["in_box"]
    assert object1.in_box == goal_state["object1"]["in_box"]
    assert object2.in_box == goal_state["object2"]["in_box"]
    assert object3.in_box == goal_state["object3"]["in_box"]
    assert object1 in object3.in_bin_objects
    assert object2 in object3.in_bin_objects
    print("All task planning is done")
