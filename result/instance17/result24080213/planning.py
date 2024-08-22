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
    is_fragile: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = True




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_fragile=True, in_box=False, out_box=True)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_fragile=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[])

### 3. Notes:
# The initial state table and Python code represent the initial configuration of objects for the bin_packing task.
# The 'object_type' field differentiates between regular objects and the box.
# The 'in_box' and 'out_box' fields are used to indicate the initial position of the objects.
# The 'in_bin_objects' list is used for the box to keep track of objects inside it, initially empty.
# The predicates 'is_soft', 'is_elastic', and 'is_fragile' are set based on the input data.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_fragile=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', is_fragile=True, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_bin_objects=[])

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object0) in the box first.
    # 2. Place the elastic object (object1) in the box.
    # 3. Place the fragile objects (object2 and object3) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    robot.pick(object0)
    robot.place(object0, box)
    robot.pick(object1)
    robot.place(object1, box)
    robot.pick(object2)
    robot.place(object2, box)
    robot.pick(object3)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed the soft object (object0) first as per the rule.
    # 2. Placed the elastic object (object1) next.
    # 3. Placed the fragile objects (object2 and object3) last.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    
    print("All task planning is done")
