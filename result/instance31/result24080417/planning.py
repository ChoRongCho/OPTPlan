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
    is_foldable: bool = False
    is_elastic: bool = False
    is_fragile: bool = False
    is_rigid: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object3 = Object(index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', is_foldable=True, is_fragile=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the box in the bin_packing task.
# The 'in_box' and 'out_box' fields are mutually exclusive, indicating whether an object is inside or outside the box.
# The 'in_bin_objects' field is used for the box to list objects that are inside it, but it is initially empty.
# The predicates such as 'is_foldable', 'is_elastic', 'is_fragile', and 'is_rigid' are set based on the given input data.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    initial_state = {
        0: {'in_box': False, 'out_box': True, 'is_rigid': True},
        1: {'in_box': False, 'out_box': True, 'is_rigid': False},
        2: {'in_box': False, 'out_box': True, 'is_elastic': True},
        3: {'in_box': True, 'out_box': False, 'is_foldable': True, 'is_fragile': True},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': []}
    }

    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_box': True, 'out_box': False, 'in_bin_objects': [0, 1, 2, 3]}
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place soft objects before fragile or rigid objects.
    # 2. Fold objects only if they are foldable.
    # 3. Only push soft objects after placing items in the bin.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4

    # c) Action sequence
    # Place soft objects first
    robot.pick(object2)  # Pick white_2D_loop (elastic)
    robot.place(object2, box)  # Place white_2D_loop in the box

    # Place rigid and fragile objects
    robot.pick(object0)  # Pick yellow_3D_cylinder (rigid)
    robot.place(object0, box)  # Place yellow_3D_cylinder in the box

    robot.pick(object1)  # Pick blue_2D_loop
    robot.place(object1, box)  # Place blue_2D_loop in the box

    # The black_2D_circle is already in the box and folded, no need to move it

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Placed white_2D_loop (soft) first as per the rule.
    # - Placed yellow_3D_cylinder (rigid) after the soft object.
    # - Placed blue_2D_loop (non-rigid) after the soft object.
    # - black_2D_circle (fragile and foldable) was already in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")
