from dataclasses import dataclass, field
from typing import List

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: List[int] = field(default_factory=list)
    
    # Object physical properties
    is_rigid: bool = False
    is_elastic: bool = False
    is_fragile: bool = False
    
    # Pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True


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
        if obj.out_box and self.robot_handempty:
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = True
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        if obj.in_box and self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.append(obj.index)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_elastic:
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        if self.robot_handempty and obj.is_elastic:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        if obj.in_box and obj.index in bin.in_bin_objects:
            self.state_holding(obj)
            bin.in_bin_objects.remove(obj.index)
            obj.in_box = False
            obj.out_box = True
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
    is_rigid=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='green_3D_cylinder', 
    color='green', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=True, 
    is_fragile=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0: out_box
    # object1: out_box
    # object2: out_box
    # object3: in_box (white_box)
    
    # Goal State:
    # object0: in_box
    # object1: in_box
    # object2: in_box
    # object3: in_box (white_box)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object2) first.
    # 2. Pick and place the rigid and fragile object (object1).
    # 3. Pick and place the rigid object (object0).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action Sequence:
    # 1. Pick and place the soft object (object2)
    robot.pick(object2, box)
    robot.place(object2, box)

    # 2. Pick and place the rigid and fragile object (object1)
    robot.pick(object1, box)
    robot.place(object1, box)

    # 3. Pick and place the rigid object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Placed the soft object (object2) first as per the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # 2. Placed the rigid and fragile object (object1) after the soft object.
    # 3. Placed the rigid object (object0) last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    # Don't include a box in the goal state. Only express objects.
    
    print("All task planning is done")
