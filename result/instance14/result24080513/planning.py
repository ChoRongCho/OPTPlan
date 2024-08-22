from dataclasses import dataclass

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
    in_bin_objects: list
    
    # Object physical properties 
    is_fragile: bool
    is_soft: bool
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
object0 = Object(index=0, name='black_3D_cuboid', color='black', shape='3D_cuboid', ...)
object1 = Object(index=1, name='white_2D_circle', color='white', shape='2D_circle', ...)

object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)
object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=True, is_rigid=False, in_box=True, out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The table and the Python code represent the initial state of the bin_packing domain.
# Each object has been initialized with its respective properties and predicates.
# The 'in_bin_objects' list is empty for all objects as no objects are inside any bin initially.
# The 'pushed' and 'folded' properties are set to False for all objects as no actions have been performed yet.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_rigid=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)
    object3 = Object(index=3, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=True, is_rigid=False, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: {'in_box': True, 'out_box': False},
        1: {'in_box': True, 'out_box': False},
        2: {'in_box': True, 'out_box': False},
        3: {'in_box': True, 'out_box': False},
        4: {'in_bin_objects': [0, 1, 2, 3]}
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
    # Place soft object first
    robot.place(object1, box)
    # Place rigid object
    robot.place(object0, box)
    # Place fragile object
    robot.place(object2, box)
    # Place elastic object
    robot.place(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed soft object (object1) first to satisfy the rule of placing soft objects before fragile or rigid objects.
    # 2. Placed rigid object (object0) after the soft object.
    # 3. Placed fragile object (object2) after the soft object.
    # 4. Placed elastic object (object3) after the soft object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert box.in_bin_objects == [0, 1, 2, 3]

    print("All task planning is done")
