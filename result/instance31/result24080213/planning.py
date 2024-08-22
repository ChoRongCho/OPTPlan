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
    is_fragile: bool = False
    is_elastic: bool = False
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
object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', in_box=False, out_box=True)
object3 = Object(index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', is_fragile=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the box for the bin_packing task.
# The 'object_type' field differentiates between objects and the box.
# The 'in_box' and 'out_box' fields indicate the initial positions of the objects.
# The predicates such as 'is_rigid', 'is_elastic', and 'is_fragile' are set based on the input data.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='blue_2D_loop', color='blue', shape='2D_loop', object_type='obj', in_box=False, out_box=True)
    object3 = Object(index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', is_fragile=True, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # - Place soft objects (elastic) before rigid or fragile objects
    # - Fold objects if they are foldable
    # - Push soft objects after placing items in the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    # 1. Place white_2D_loop (soft object) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False
    box.in_bin_objects.append(object1.index)

    # 2. Place blue_2D_loop (soft object) in the box
    robot.place(object2, box)
    object2.in_box = True
    object2.out_box = False
    box.in_bin_objects.append(object2.index)

    # 3. Place yellow_3D_cylinder (rigid object) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False
    box.in_bin_objects.append(object0.index)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Placed white_2D_loop first because it is a soft object
    # - Placed blue_2D_loop next because it is also a soft object
    # - Placed yellow_3D_cylinder last because it is a rigid object and all soft objects are already in the box

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True  # Already in the box initially
    # assert final_object.is_in_box == True or False
    
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
