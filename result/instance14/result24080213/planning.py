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
    is_soft: bool = False
    is_elastic: bool = False
    is_fragile: bool = False
    is_rigid: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = False




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='black_3D_cuboid', color='black', shape='3D_cuboid', ...)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', ...)

object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, out_box=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, out_box=True)
object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_fragile=True, in_box=True)
object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True)

### 3. Notes:
# The table and Python code represent the initial state of the bin_packing domain.
# Each object has been initialized with its respective properties and predicates.
# The 'in_box' and 'out_box' predicates are mutually exclusive for each object.
# The 'white_box' is considered a box and has no additional predicates or objects inside it initially.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, out_box=True)
    object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, out_box=True)
    object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_fragile=True, in_box=True)
    object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=True)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True)

    # Goal State
    goal_object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=True)
    goal_object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', is_soft=True, is_elastic=True, in_box=True)
    goal_object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_fragile=True, in_box=True)
    goal_object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=True)
    goal_object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, in_bin_objects=[0, 1, 2, 3])

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place the soft object (object1) in the box first.
    # 2. Place the rigid object (object0) in the box.
    # 3. Ensure all objects are in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action Sequence
    # 1. Place the soft object (object1) in the box
    robot.place(object1, box)
    # 2. Place the rigid object (object0) in the box
    robot.place(object0, box)
    # 3. Ensure all objects are in the box
    robot.place(object2, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed the soft object (object1) first as per the rule.
    # - Placed the rigid object (object0) after the soft object.
    # - Ensured all objects are in the box to satisfy the goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    # assert final_object.is_in_box == True or False
    
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
