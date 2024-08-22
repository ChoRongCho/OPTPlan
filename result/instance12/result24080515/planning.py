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
    is_rigid: bool
    is_fragile: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packed: bool


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
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and (obj.is_elastic or all(o.is_elastic for o in bin.in_bin_objects)):
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.is_packed = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_elastic and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_elastic:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.is_packed = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_fragile=False, 
    is_elastic=False, 
    in_box=False, 
    is_packed=False
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
    is_rigid=True, 
    is_fragile=True, 
    is_elastic=False, 
    in_box=False, 
    is_packed=False
)

object2 = Object(
    index=2, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_fragile=False, 
    is_elastic=True, 
    in_box=False, 
    is_packed=False
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
    is_rigid=False, 
    is_fragile=False, 
    is_elastic=False, 
    in_box=True, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        "object0": object0,
        "object1": object1,
        "object2": object2,
        "object3": object3
    }
    
    # Goal State
    goal_state = {
        "object0": {"in_box": True, "is_packed": True},
        "object1": {"in_box": True, "is_packed": True},
        "object2": {"in_box": True, "is_packed": True},
        "object3": {"in_bin_objects": [object0, object1, object2], "is_packed": True}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the elastic object first (object2)
    # 2. Pick and place the rigid and fragile objects (object0 and object1)
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Action sequence
    # Pick and place the elastic object first
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Pick and place the rigid object
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Pick and place the fragile object
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. The elastic object (object2) is placed first to satisfy the rule that soft objects should be in the box before placing rigid or fragile objects.
    # 2. The rigid object (object0) is placed next.
    # 3. The fragile object (object1) is placed last.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [object2, object0, object1]
    assert object0.is_packed == True
    assert object1.is_packed == True
    assert object2.is_packed == True
    assert object3.is_packed == True
    
    print("All task planning is done")
