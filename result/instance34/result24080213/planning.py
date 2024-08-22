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
    is_rigid: bool = False
    is_soft: bool = False
    is_elastic: bool = False
    is_foldable: bool = False
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool = False
    out_box: bool = False




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, out_box=True)
object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, out_box=True)
object2 = Object(index=2, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', is_foldable=True, is_fragile=True, in_box=True)
object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box')

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the bin for the bin_packing task.
# The predicates are translated into boolean attributes in the Object dataclass.
# The 'init_pose' attribute is translated into 'in_box' or 'out_box' boolean attributes.
# The 'object_type' attribute is used to distinguish between objects and the bin.

---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', is_soft=True, out_box=True)
    object1 = Object(index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, out_box=True)
    object2 = Object(index=2, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', is_foldable=True, is_fragile=True, in_box=True)
    object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', is_elastic=True, in_box=True)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box')

    # Second, using given rules and object's states, make a task planning strategy
    # Rules:
    # 1. Place: Before placing a fragile or rigid object, a soft object should be in the box if there is any soft object.
    # 2. Pick: None
    # 3. Fold: Fold objects only if they are foldable.
    # 4. Push: Only push soft objects after placing items in the bin.
    # 5. Out: None

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object4

    # Action sequence
    # 1. Place the soft object (object0) in the box
    robot.place(object0, box)
    object0.in_box = True
    object0.out_box = False

    # 2. Place the rigid object (object1) in the box
    robot.place(object1, box)
    object1.in_box = True
    object1.out_box = False

    # 3. No need to fold object2 as it is already in the box
    # 4. No need to fold object3 as it is already in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - Placed object0 (soft) first to satisfy the rule that soft objects should be in the box before placing fragile or rigid objects.
    # - Placed object1 (rigid) after the soft object was placed.
    # - No need to fold object2 and object3 as they are already in the box.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    
    print("All task planning is done")
