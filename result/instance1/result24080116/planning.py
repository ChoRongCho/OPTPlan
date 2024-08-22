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
    is_soft: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
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
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        if self.robot_handempty and obj.is_soft and obj.index in bin.in_bin_objects:
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
        if obj.index in bin.in_bin_objects:
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
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=True, 
    is_soft=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=True, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='blue_2D_loop', 
    color='blue', 
    shape='2D_loop', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_rigid=False, 
    is_elastic=False, 
    is_soft=False, 
    in_box=False, 
    out_box=True
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
    is_elastic=False, 
    is_soft=False, 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    # object0: out_box=True, in_box=False
    # object1: out_box=True, in_box=False
    # object2: out_box=True, in_box=False
    # object3: out_box=False, in_box=True, in_bin_objects=[]

    # Goal state
    # object0: out_box=False, in_box=True
    # object1: out_box=False, in_box=True
    # object2: out_box=False, in_box=True
    # object3: out_box=False, in_box=True, in_bin_objects=[0, 1, 2]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the rigid object (object1).
    # 3. Pick and place the non-rigid, non-soft object (object2).

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object0, box)  # Pick yellow_3D_cuboid
    robot.place(object0, box)  # Place yellow_3D_cuboid in white_box

    robot.pick(object1, box)  # Pick black_3D_cylinder
    robot.place(object1, box)  # Place black_3D_cylinder in white_box

    robot.pick(object2, box)  # Pick blue_2D_loop
    robot.place(object2, box)  # Place blue_2D_loop in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. Pick and place the soft object (object0) first to satisfy the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # 2. Pick and place the rigid object (object1) after the soft object is placed.
    # 3. Pick and place the non-rigid, non-soft object (object2) last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
