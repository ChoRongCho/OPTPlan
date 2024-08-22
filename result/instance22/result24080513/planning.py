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
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_rigid=True, in_box=False, out_box=True)
object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state is defined based on the given input images.
# The 'object_type' is determined as 'obj' for non-box items and 'box' for the box item.
# The 'pushed' and 'folded' properties are set to False as default initial states.
# The 'in_bin_objects' list is empty initially for all objects.
# The 'in_box' and 'out_box' properties are set based on the 'init_pose' from the input.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_rigid=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_rigid=True, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_rigid=True, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1], is_fragile=False, is_rigid=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the yellow_3D_cylinder (rigid) into the white_box.
    # 2. Place the black_2D_loop (fragile) into the white_box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object2

    # c) Action sequence
    # Place yellow_3D_cylinder into the white_box
    robot.pick(object0)
    robot.place(object0, box)

    # Place black_2D_loop into the white_box
    robot.pick(object1)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The yellow_3D_cylinder is rigid and can be placed in the box first.
    # - The black_2D_loop is fragile and should be placed after the rigid object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_bin_objects == [0, 1]
    
    print("All task planning is done")
