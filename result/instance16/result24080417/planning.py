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
    is_elastic: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='beige_2D_loop', color='beige', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_elastic=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state is derived from the input images and includes three objects: two elastic objects and one box. The elastic objects are initially out of the box, while the box itself is considered to be in the box.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='beige_2D_loop', color='beige', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', is_elastic=False, in_box=True, out_box=False)

    # Goal state
    goal_object0_in_box = True
    goal_object1_in_box = True
    goal_object2_in_bin_objects = [0, 1]

    # Second, using given rules and object's states, make a task planning strategy
    # According to the rules:
    # 1. Place soft objects first before placing rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Place the soft objects in the box first
    robot.place(object0, box)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft objects (object0 and object1) in the box first as per the rule.
    # 2. No need to fold or push any objects as per the current goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == goal_object0_in_box
    assert object1.in_box == goal_object1_in_box
    assert object2.in_bin_objects == goal_object2_in_bin_objects
    
    print("All task planning is done")
