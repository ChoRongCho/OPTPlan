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
    
    # Object physical properties 
    is_soft: bool
    is_rigid: bool
    is_fragile: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    init_pose: str
    in_box: bool


class Robot:
    def __init__(self,
                 name: str = "OpenManipulator",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        if self.robot_handempty and not obj.in_box:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
    
    def place(self, obj, bin):
        if self.robot_now_holding == obj:
            if obj.is_soft or (not obj.is_soft and any(o.is_soft for o in bin.in_bin_objects)):
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot Place {obj.name} in {bin.name} due to soft object rule")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin):
        if self.robot_handempty and obj.is_soft:
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
    
    def out(self, obj, bin):
        if obj in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

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
    in_bin_objects=[], 
    is_soft=False, 
    is_rigid=True, 
    is_fragile=True, 
    init_pose='out_box', 
    in_box=False
)

object1 = Object(
    index=1, 
    name='red_3D_polyhedron', 
    color='red', 
    shape='3D_polyhedron', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=True, 
    is_rigid=False, 
    is_fragile=False, 
    init_pose='out_box', 
    in_box=False
)

object2 = Object(
    index=2, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_soft=False, 
    is_rigid=False, 
    is_fragile=False, 
    init_pose='box', 
    in_box=True
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        "object0": {"in_box": False, "init_pose": "out_box"},
        "object1": {"in_box": False, "init_pose": "out_box"},
        "object2": {"in_box": True, "init_pose": "box", "in_bin_objects": []}
    }
    
    # Goal state
    goal_state = {
        "object0": {"in_box": True, "init_pose": "in_box"},
        "object1": {"in_box": True, "init_pose": "in_box"},
        "object2": {"in_box": True, "init_pose": "box", "in_bin_objects": [0, 1]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick the soft object (object1) and place it in the box (object2).
    # 2. Pick the fragile object (object0) and place it in the box (object2).
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object2
    
    # Action sequence
    robot.pick(object1, box)  # Pick red_3D_polyhedron
    robot.place(object1, box)  # Place red_3D_polyhedron in white_box
    
    robot.pick(object0, box)  # Pick green_3D_cylinder
    robot.place(object0, box)  # Place green_3D_cylinder in white_box
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The soft object (object1) is placed first to satisfy the rule that a soft object should be in the box before placing a fragile or rigid object.
    # 2. The fragile object (object0) is placed after the soft object to ensure the rule is followed.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    # Don't include a box in the goal state. Only express objects.
    
    print("All task planning is done")
