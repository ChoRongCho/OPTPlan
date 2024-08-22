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
    pushed: bool = False
    folded: bool = False
    
    # Predicates for box
    in_bin_objects: List[int] = None
    
    # Object physical properties 
    is_soft: bool = False
    is_elastic: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = False




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_elastic=True, out_box=True)
object2 = Object(index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box')

### 3. Notes:
# The 'in_bin_objects' field is set to None for all objects as there is no information provided about objects being inside the bin.
# The 'pushed' and 'folded' fields are set to False by default as there is no information provided about these states.
# The 'object_type' is determined based on the 'shape' and 'init_pose' fields.
# The 'in_box' and 'out_box' fields are set based on the 'init_pose' field.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, out_box=True)
    object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_elastic=True, out_box=True)
    object2 = Object(index=2, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box')

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': False, 'out_box': False}  # Box state is not relevant for goal
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Ensure the soft object (object2) is in the box (already in the box in initial state).
    # 2. Place the elastic objects (object0 and object1) into the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Action sequence
    # Place object0 (white_2D_loop) into the box
    robot.pick(object0)
    robot.place(object0, box)

    # Place object1 (black_2D_loop) into the box
    robot.pick(object1)
    robot.place(object1, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - The soft object (object2) is already in the box, satisfying the rule that soft objects should be placed first.
    # - The elastic objects (object0 and object1) are placed into the box after ensuring the soft object is already in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == False  # Box state is not relevant for goal

    print("All task planning is done")
