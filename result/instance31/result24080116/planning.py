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
    is_foldable: bool = False
    
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
        if self.robot_now_holding == obj:
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
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
        if self.robot_handempty and obj.is_foldable:
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
    name='yellow_3D_cylinder', 
    color='yellow', 
    shape='3D_cylinder', 
    object_type='obj', 
    is_rigid=True, 
    in_box=False, 
    out_box=True
)

object1 = Object(
    index=1, 
    name='white_2D_loop', 
    color='white', 
    shape='2D_loop', 
    object_type='obj', 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object2 = Object(
    index=2, 
    name='black_2D_loop', 
    color='black', 
    shape='2D_loop', 
    object_type='obj', 
    is_elastic=True, 
    in_box=False, 
    out_box=True
)

object3 = Object(
    index=3, 
    name='black_2D_circle', 
    color='black', 
    shape='2D_circle', 
    object_type='obj', 
    is_foldable=True, 
    in_box=True, 
    out_box=False
)

object4 = Object(
    index=4, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    in_box_objects=[3], 
    in_box=True, 
    out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    # object0: out_box
    # object1: out_box
    # object2: out_box
    # object3: in_box
    # object4: box (contains object3)
    
    # Goal State
    # object0: in_box
    # object1: in_box
    # object2: in_box
    # object3: in_box
    # object4: box (contains object0, object1, object2, object3)

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Place soft objects (elastic) first
    # 2. Place rigid objects after soft objects are in the box
    # 3. Fold objects only if they are foldable
    # 4. Push soft objects after placing items in the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.pick(object1, box)  # Pick white_2D_loop
    robot.place(object1, box)  # Place white_2D_loop in white_box

    robot.pick(object2, box)  # Pick black_2D_loop
    robot.place(object2, box)  # Place black_2D_loop in white_box

    robot.pick(object0, box)  # Pick yellow_3D_cylinder
    robot.place(object0, box)  # Place yellow_3D_cylinder in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. Pick and place white_2D_loop (soft object) first as per the rule.
    # 2. Pick and place black_2D_loop (soft object) next as per the rule.
    # 3. Pick and place yellow_3D_cylinder (rigid object) after soft objects are in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True  # Already in the box
    # Don't include a box in the goal state. Only express objects.
    
    print("All task planning is done")
