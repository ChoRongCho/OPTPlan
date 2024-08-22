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
    is_foldable: bool = False
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
object1 = Object(index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
object2 = Object(index=2, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
object3 = Object(index=3, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_foldable=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code reflect the properties and initial positions of the objects as described in the input.
# The 'in_bin_objects' list is initialized as empty for all objects since no objects are inside the box initially.
# The 'in_box' and 'out_box' flags are set according to the 'init_pose' provided in the input.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', is_soft=True, is_elastic=True, in_box=False, out_box=True)
    object2 = Object(index=2, name='green_2D_circle', color='green', shape='2D_circle', object_type='obj', is_foldable=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', is_foldable=True, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', in_box=True, out_box=False)

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
    # 1. Fold the foldable objects
    robot.fold(object2)
    robot.fold(object3)

    # 2. Place the soft object in the box first
    robot.place(object1, box)

    # 3. Place the rigid object in the box
    robot.place(object0, box)

    # 4. Place the foldable objects in the box
    robot.place(object2, box)
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # - Folded foldable objects (object2, object3) as per the 'fold' rule.
    # - Placed the soft object (object1) before placing the rigid object (object0) as per the 'place' rule.
    # - Placed all objects in the box as per the goal state.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    # assert final_object.is_in_box == True or False
    
    # Don't include a box in the goal state. Only express objects.
    print("All task planning is done")
