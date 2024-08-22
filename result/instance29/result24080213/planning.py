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
    is_elastic: bool
    is_foldable: bool
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
object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_foldable=False, is_rigid=True, in_box=False, out_box=True)
object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_foldable=True, is_rigid=False, in_box=False, out_box=True)
object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_elastic=True, is_foldable=False, is_rigid=False, in_box=False, out_box=True)
object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_foldable=False, is_rigid=False, in_box=True, out_box=False)

### 3. Notes:
# The initial state table and Python code represent the initial conditions of the objects and the box in the bin_packing domain.
# The 'in_bin_objects' list is empty for all objects initially, indicating that no objects are inside the box at the start.
# The 'pushed' and 'folded' predicates are set to False for all objects initially.
# The 'in_box' and 'out_box' predicates are mutually exclusive and indicate whether an object is inside or outside the box.
---template end--

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_foldable=False, is_rigid=True, in_box=False, out_box=True)
    object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_foldable=True, is_rigid=False, in_box=False, out_box=True)
    object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_elastic=True, is_foldable=False, is_rigid=False, in_box=False, out_box=True)
    object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_foldable=False, is_rigid=False, in_box=True, out_box=False)

    # Goal state
    goal_object0 = Object(index=0, name='red_3D_cuboid', color='red', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=False, is_foldable=False, is_rigid=True, in_box=True, out_box=False)
    goal_object1 = Object(index=1, name='black_2D_loop', color='black', shape='2D_loop', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=False, is_elastic=True, is_foldable=True, is_rigid=False, in_box=True, out_box=False)
    goal_object2 = Object(index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_fragile=True, is_elastic=True, is_foldable=False, is_rigid=False, in_box=True, out_box=False)
    goal_object3 = Object(index=3, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[0, 1, 2], is_fragile=False, is_elastic=False, is_foldable=False, is_rigid=False, in_box=True, out_box=False)

    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the black_2D_loop (object1) since it is foldable.
    # 2. Place the black_2D_loop (object1) in the box.
    # 3. Place the white_2D_circle (object2) in the box.
    # 4. Place the red_3D_cuboid (object0) in the box.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    robot.fold(object1)  # Fold the black_2D_loop
    robot.place(object1, box)  # Place the black_2D_loop in the box
    robot.place(object2, box)  # Place the white_2D_circle in the box
    robot.place(object0, box)  # Place the red_3D_cuboid in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Folded the black_2D_loop because it is foldable.
    # 2. Placed the black_2D_loop first because it is a soft object.
    # 3. Placed the white_2D_circle next because it is a fragile object.
    # 4. Placed the red_3D_cuboid last because it is a rigid object.

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_bin_objects == [0, 1, 2]

    print("All task planning is done")
