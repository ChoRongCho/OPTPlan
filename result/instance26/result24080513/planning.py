from dataclasses import dataclass
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
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: List[int]
    
    # Object physical properties
    is_fragile: bool
    is_elastic: bool
    is_rigid: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the box in the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects initially, indicating that no objects are inside the box at the start.
# The 'in_box' and 'out_box' boolean flags are used to indicate the initial position of each object relative to the box.
# The 'pushed' and 'folded' flags are set to False for all objects initially, as no actions have been performed on them yet.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_object0_in_box = True
    goal_object1_in_box = True
    goal_object2_in_box = True
    goal_object3_in_bin_objects = [0, 1, 2]

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft objects (object1 and object2) in the box first.
    # 2. Place the fragile and rigid object (object0) in the box.
    # 3. Ensure all objects are in the box and the box contains all objects.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object1)
    robot.place(object1, box)
    robot.pick(object2)
    robot.place(object2, box)
    robot.pick(object0)
    robot.place(object0, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed soft objects (object1 and object2) in the box first as per the rule.
    # - Placed the fragile and rigid object (object0) after the soft objects were in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == goal_object0_in_box
    assert object1.in_box == goal_object1_in_box
    assert object2.in_box == goal_object2_in_box
    assert box.in_bin_objects == goal_object3_in_bin_objects

    print("All task planning is done")
