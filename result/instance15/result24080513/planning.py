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
    is_foldable: bool
    
    # pre-conditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool




    def dummy(self):
        pass


 # Object Initial State
code
# don't include the object classes or robot class, make only objects and bin 
# example 
object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_elastic=False, is_foldable=True, in_box=False, out_box=True)
object3 = Object(index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_foldable=True, in_box=True, out_box=False)
object4 = Object(index=4, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=True, is_foldable=False, in_box=True, out_box=False)
object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_foldable=False, in_box=True, out_box=False)

### 3. Notes:
# The table and the Python code represent the initial state of the bin_packing domain.
# Each object has properties such as color, shape, type, and various predicates.
# The 'in_box' and 'out_box' fields indicate the initial position of the objects.
# The 'in_bin_objects' list is empty for all objects initially, as no objects are inside any bin at the start.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
    object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=True, is_elastic=True, is_foldable=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_soft=False, is_elastic=False, is_foldable=True, in_box=False, out_box=True)
    object3 = Object(index=3, name='green_3D_sphere', color='green', shape='3D_sphere', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_foldable=True, in_box=True, out_box=False)
    object4 = Object(index=4, name='white_2D_loop', color='white', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=True, is_foldable=False, in_box=True, out_box=False)
    object5 = Object(index=5, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_soft=False, is_elastic=False, is_foldable=False, in_box=True, out_box=False)

    # Goal state
    goal_state = {
        0: True,  # object0 in box
        1: True,  # object1 in box
        2: True,  # object2 in box
        3: True,  # object3 in box
        4: True,  # object4 in box
    }

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Place soft objects first (object0, object1)
    # 2. Fold foldable objects (object2)
    # 3. Place fragile and rigid objects (object2)
    # 4. Push soft objects if needed (not needed in this case)
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    # b) Define the box
    box = object5

    # Action sequence
    robot.place(object0, box)  # Place soft object0
    robot.place(object1, box)  # Place soft object1
    robot.fold(object2)        # Fold foldable object2
    robot.place(object2, box)  # Place fragile object2

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Placed soft objects (object0, object1) first as per the rule.
    # 2. Folded object2 because it is foldable.
    # 3. Placed fragile object2 after soft objects were placed.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    
    print("All task planning is done")
